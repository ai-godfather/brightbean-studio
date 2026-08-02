#!/usr/bin/env python3
"""Build the upload-ready YouTube/Google compliance PDFs from tracked sources."""

from __future__ import annotations

import html
import re
from pathlib import Path

from lxml import html as lxml_html
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SOURCE_DIR / "pdf"
TEMPLATE_DIR = ROOT / "templates" / "legal"

PUBLIC_URLS = {
    "privacy_policy": "https://studio.shopauth.cloud/privacy/",
    "terms_of_service": "https://studio.shopauth.cloud/terms/",
    "data_deletion": "https://studio.shopauth.cloud/data-deletion/",
    "youtube_integration": "https://studio.shopauth.cloud/youtube-integration/",
}


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Arial", "/System/Library/Fonts/Supplemental/Arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))


def styles():
    sample = getSampleStyleSheet()
    brand = colors.HexColor("#657026")
    ink = colors.HexColor("#24251f")
    muted = colors.HexColor("#686b60")
    return {
        "title": ParagraphStyle(
            "Title",
            parent=sample["Title"],
            fontName="Arial-Bold",
            fontSize=23,
            leading=28,
            alignment=TA_CENTER,
            textColor=ink,
            spaceAfter=8 * mm,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=sample["Heading1"],
            fontName="Arial-Bold",
            fontSize=17,
            leading=21,
            textColor=brand,
            spaceBefore=5 * mm,
            spaceAfter=3 * mm,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=sample["Heading2"],
            fontName="Arial-Bold",
            fontSize=13,
            leading=16,
            textColor=ink,
            spaceBefore=4 * mm,
            spaceAfter=2 * mm,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=sample["Heading3"],
            fontName="Arial-Bold",
            fontSize=11,
            leading=14,
            textColor=ink,
            spaceBefore=3 * mm,
            spaceAfter=1.5 * mm,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=sample["BodyText"],
            fontName="Arial",
            fontSize=9.2,
            leading=13.2,
            textColor=ink,
            spaceAfter=2.3 * mm,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=sample["BodyText"],
            fontName="Arial",
            fontSize=7.6,
            leading=10,
            textColor=muted,
        ),
        "table": ParagraphStyle(
            "Table",
            parent=sample["BodyText"],
            fontName="Arial",
            fontSize=6.6,
            leading=8.4,
            textColor=ink,
        ),
    }


def inline_markup(value: str) -> str:
    value = html.escape(value.strip())
    value = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"\[([^]]+)]\((https?://[^)]+)\)", r"<a href='\2'>\1</a>", value)
    value = re.sub(r"(?<!['\"])(https?://[^\s&lt;]+)", r"<a href='\1'>\1</a>", value)
    return value


def markdown_story(path: Path, pdf_styles: dict) -> list:
    lines = path.read_text(encoding="utf-8").splitlines()
    story: list = []
    paragraph: list[str] = []
    bullets: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            story.append(Paragraph(inline_markup(" ".join(paragraph)), pdf_styles["body"]))
            paragraph.clear()

    def flush_bullets() -> None:
        if bullets:
            items = [
                ListItem(Paragraph(inline_markup(item), pdf_styles["body"]), leftIndent=4 * mm) for item in bullets
            ]
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=6 * mm, bulletFontName="Arial"))
            story.append(Spacer(1, 1.5 * mm))
            bullets.clear()

    index = 0
    while index < len(lines):
        line = lines[index].rstrip()
        if line.startswith("|") and index + 1 < len(lines) and re.match(r"^\|[\s|:-]+\|$", lines[index + 1]):
            flush_paragraph()
            flush_bullets()
            table_lines = [line]
            index += 2
            while index < len(lines) and lines[index].startswith("|"):
                table_lines.append(lines[index])
                index += 1
            rows = []
            for row in table_lines:
                cells = [cell.strip() for cell in row.strip("|").split("|")]
                rows.append([Paragraph(inline_markup(cell), pdf_styles["table"]) for cell in cells])
            col_count = max(len(row) for row in rows)
            table = Table(rows, repeatRows=1, colWidths=[(180 * mm) / col_count] * col_count)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef1d9")),
                        ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#c8cabf")),
                        ("LEFTPADDING", (0, 0), (-1, -1), 3),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ]
                )
            )
            story.append(table)
            story.append(Spacer(1, 2 * mm))
            continue
        if line.startswith("# "):
            flush_paragraph()
            flush_bullets()
            story.append(Paragraph(inline_markup(line[2:]), pdf_styles["h1"]))
        elif line.startswith("## "):
            flush_paragraph()
            flush_bullets()
            story.append(Paragraph(inline_markup(line[3:]), pdf_styles["h2"]))
        elif line.startswith("### "):
            flush_paragraph()
            flush_bullets()
            story.append(Paragraph(inline_markup(line[4:]), pdf_styles["h3"]))
        elif re.match(r"^[-*] ", line):
            flush_paragraph()
            bullets.append(line[2:])
        elif re.match(r"^\d+\. ", line):
            flush_paragraph()
            bullets.append(re.sub(r"^\d+\. ", "", line))
        elif not line:
            flush_paragraph()
            flush_bullets()
        else:
            flush_bullets()
            paragraph.append(line)
        index += 1

    flush_paragraph()
    flush_bullets()
    return story


def render_django_template(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    source = re.sub(r"{%\s*extends[^%]+%}", "", source)
    source = re.sub(r"{%\s*(?:end)?block[^%]*%}", "", source)
    for route, url in PUBLIC_URLS.items():
        source = source.replace("{% url '" + route + "' %}", url)
    source = re.sub(r"{%[^%]+%}", "", source)
    return source


def html_story(path: Path, pdf_styles: dict) -> list:
    root = lxml_html.fromstring(render_django_template(path))
    story: list = []
    for node in root.iter():
        tag = node.tag.lower() if isinstance(node.tag, str) else ""
        if tag in {"h2", "h3", "p"}:
            content = lxml_html.tostring(node, encoding="unicode", method="html", with_tail=False)
            content = re.sub(r"^<[^>]+>|</[^>]+>$", "", content).strip()
            content = content.replace("<strong>", "<b>").replace("</strong>", "</b>")
            content = re.sub(r"\srel=(?:\"[^\"]*\"|'[^']*')", "", content)
            content = re.sub(r"\sclass=(?:\"[^\"]*\"|'[^']*')", "", content)
            content = re.sub(r"<a ([^>]*?)>", r"<a \1 color='#657026'>", content)
            style = pdf_styles["h2"] if tag == "h2" else pdf_styles["h3"] if tag == "h3" else pdf_styles["body"]
            if content:
                story.append(Paragraph(content, style))
        elif tag in {"ul", "ol"}:
            direct_items = node.xpath("./li")
            items = []
            for item in direct_items:
                content = " ".join(item.itertext()).strip()
                items.append(ListItem(Paragraph(html.escape(content), pdf_styles["body"]), leftIndent=4 * mm))
            if items:
                story.append(
                    ListFlowable(
                        items,
                        bulletType="1" if tag == "ol" else "bullet",
                        leftIndent=7 * mm,
                        bulletFontName="Arial",
                    )
                )
                story.append(Spacer(1, 1.5 * mm))
    return story


def page_decor(canvas, document) -> None:
    canvas.saveState()
    width, _height = A4
    canvas.setStrokeColor(colors.HexColor("#d7d9ce"))
    canvas.line(16 * mm, 14 * mm, width - 16 * mm, 14 * mm)
    canvas.setFont("Arial", 7)
    canvas.setFillColor(colors.HexColor("#686b60"))
    canvas.drawString(16 * mm, 9 * mm, "BrightBean Social Studio · Google/YouTube compliance package · 2026-08-02")
    canvas.drawRightString(width - 16 * mm, 9 * mm, f"Page {document.page}")
    canvas.restoreState()


def build_pdf(filename: str, title: str, story: list, pdf_styles: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(OUTPUT_DIR / filename),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=16 * mm,
        bottomMargin=19 * mm,
        title=title,
        author="ShopAuth Cloud",
        subject="BrightBean Social Studio Google and YouTube compliance",
    )
    cover = [
        Spacer(1, 18 * mm),
        Paragraph(title, pdf_styles["title"]),
        Paragraph(
            "Prepared for Google OAuth verification and YouTube API Services compliance review", pdf_styles["body"]
        ),
        Spacer(1, 5 * mm),
        Paragraph("Application: BrightBean Social Studio", pdf_styles["body"]),
        Paragraph("Production domain: studio.shopauth.cloud", pdf_styles["body"]),
        Paragraph("Prepared: August 2, 2026", pdf_styles["body"]),
        Spacer(1, 10 * mm),
        Paragraph(
            "This supporting PDF is a point-in-time snapshot. The live public policies and the deployed application are authoritative for the review.",
            pdf_styles["small"],
        ),
        PageBreak(),
    ]
    document.build(cover + story, onFirstPage=page_decor, onLaterPages=page_decor)


def main() -> None:
    register_fonts()
    pdf_styles = styles()

    dossier_sources = [
        "oauth_verification_submission.md",
        "youtube_api_audit_responses.md",
        "scope_justifications.md",
        "data_handling_matrix.md",
        "security_and_retention_controls.md",
        "evidence_checklist.md",
    ]
    dossier_story: list = []
    for position, filename in enumerate(dossier_sources):
        if position:
            dossier_story.append(PageBreak())
        dossier_story.extend(markdown_story(SOURCE_DIR / filename, pdf_styles))
    build_pdf(
        "BrightBean_YouTube_API_Audit_Dossier.pdf",
        "BrightBean YouTube API Audit Dossier",
        dossier_story,
        pdf_styles,
    )

    build_pdf(
        "BrightBean_OAuth_Scope_Justifications.pdf",
        "BrightBean OAuth Scope Justifications",
        markdown_story(SOURCE_DIR / "scope_justifications.md", pdf_styles),
        pdf_styles,
    )

    for template_name, output_name, title in (
        ("privacy_policy.html", "BrightBean_Privacy_Policy_2026-08-02.pdf", "BrightBean Privacy Policy"),
        ("terms_of_service.html", "BrightBean_Terms_of_Service_2026-08-02.pdf", "BrightBean Terms of Service"),
        ("data_deletion.html", "BrightBean_Data_Deletion_2026-08-02.pdf", "BrightBean Data Deletion Instructions"),
    ):
        build_pdf(output_name, title, html_story(TEMPLATE_DIR / template_name, pdf_styles), pdf_styles)


if __name__ == "__main__":
    main()
