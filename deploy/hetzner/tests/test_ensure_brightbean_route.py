from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "ensure_brightbean_route.py"
SPEC = importlib.util.spec_from_file_location("ensure_brightbean_route", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


BASE = """{
  auto_https off
}

api.shopauth.cloud {
  reverse_proxy admin-api:3001
}

# ── HTTP fallback (IP / pre-DNS smoke) ───────────────────────────────────────
:80 {
  @api host api.shopauth.cloud
  handle @api {
    reverse_proxy admin-api:3001
  }
  handle {
    respond "ShopAuth Cloud production — set DNS A record to this host." 200
  }
}
"""


class RouteRenderTests(unittest.TestCase):
    def test_adds_named_site_and_fallback_handler(self) -> None:
        rendered = MODULE.render(BASE)
        self.assertIn("studio.shopauth.cloud {", rendered)
        self.assertIn("@brightbean host studio.shopauth.cloud", rendered)
        self.assertLess(
            rendered.index("studio.shopauth.cloud {"),
            rendered.index("# ── HTTP fallback"),
        )
        self.assertLess(
            rendered.index("@brightbean host studio.shopauth.cloud"),
            rendered.rindex("ShopAuth Cloud production"),
        )

    def test_is_idempotent(self) -> None:
        rendered = MODULE.render(BASE)
        self.assertEqual(MODULE.render(rendered), rendered)

    def test_fails_closed_when_named_site_anchor_is_missing(self) -> None:
        with self.assertRaisesRegex(MODULE.RouteAnchorError, "HTTP fallback"):
            MODULE.render("api.shopauth.cloud {}\n")

    def test_cli_check_does_not_modify_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "Caddyfile"
            path.write_text(BASE, encoding="utf-8")
            before = path.read_bytes()
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--caddyfile", str(path)],
                capture_output=True,
                check=False,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout.strip(), "repair-required")
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
