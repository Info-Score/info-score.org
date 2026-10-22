"""SDF (I-22) : GitHub Pages ne pose aucun en-tête ; chaque page porte donc sa politique en balise meta,
et tout script tiers est épinglé par une empreinte d'intégrité (SRI)."""

import re
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
PAGES = sorted(RACINE.glob("*.html"))


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_la_page_porte_sa_politique(page: Path) -> None:
    html = page.read_text(encoding="utf-8")
    csp = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]+)"', html)
    assert csp, "CSP absente"
    for directive in ("default-src 'self'", "object-src 'none'", "base-uri 'self'", "form-action 'none'"):
        assert directive in csp.group(1), directive
    assert '<meta name="referrer" content="strict-origin-when-cross-origin">' in html


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_tout_script_tiers_est_epingle(page: Path) -> None:
    for balise in re.findall(r"<script[^>]*\bsrc=\"https?://[^>]*>", page.read_text(encoding="utf-8")):
        assert 'integrity="sha384-' in balise and 'crossorigin="anonymous"' in balise, balise
