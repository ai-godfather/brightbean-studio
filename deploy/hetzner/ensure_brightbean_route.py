#!/usr/bin/env python3
"""Fail-closed Caddy route repair owned by the BrightBean deployment."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path

NAMED_SITE = """# ── BrightBean Studio ─────────────────────────────────────────────────────────
studio.shopauth.cloud {
  encode gzip zstd
  reverse_proxy brightbean-app:8000 {
    header_up X-Forwarded-Proto https
  }
}

"""

FALLBACK_HANDLER = """  @brightbean host studio.shopauth.cloud
  handle @brightbean {
    reverse_proxy brightbean-app:8000 {
      header_up X-Forwarded-Proto https
    }
  }
"""

HTTP_FALLBACK_MARKER = "# ── HTTP fallback"
FINAL_FALLBACK = """  handle {
    respond "ShopAuth Cloud production — set DNS A record to this host." 200
  }
"""


class RouteAnchorError(ValueError):
    """The shared ingress file no longer has the expected safe anchors."""


def render(source: str) -> str:
    """Return source with both BrightBean routes present, or fail closed."""

    rendered = source
    if "studio.shopauth.cloud {" not in rendered:
        marker_index = rendered.find(HTTP_FALLBACK_MARKER)
        if marker_index < 0:
            raise RouteAnchorError("HTTP fallback marker is missing")
        rendered = rendered[:marker_index] + NAMED_SITE + rendered[marker_index:]

    if "@brightbean host studio.shopauth.cloud" not in rendered:
        fallback_index = rendered.rfind(FINAL_FALLBACK)
        if fallback_index < 0:
            raise RouteAnchorError("final ShopAuth fallback handler is missing")
        rendered = rendered[:fallback_index] + FALLBACK_HANDLER + rendered[fallback_index:]

    return rendered


def atomic_write(path: Path, content: str) -> None:
    """Replace a file atomically while preserving its current mode."""

    mode = path.stat().st_mode
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.chmod(temporary, mode)
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--caddyfile", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    source = args.caddyfile.read_text(encoding="utf-8")
    rendered = render(source)
    if rendered == source:
        print("unchanged")
        return 0
    if not args.apply:
        print("repair-required")
        return 2

    atomic_write(args.caddyfile, rendered)
    print("updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
