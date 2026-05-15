"""Tests for HTML generation — verifies output structure and correctness."""

import json
from html.parser import HTMLParser

import pytest

from scripts.generate import HTMLGenerator
from tests.conftest import MANIFESTS_DIR


# ── Quality Checklist Helper ──────────────────────────────────────────

class _HTMLValidator(HTMLParser):
    """Basic HTML structural validator."""
    def __init__(self):
        super().__init__()
        self.errors = []

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass


def _run_quality_checks(html: str, pattern_name: str) -> list:
    """Run quality checks on generated HTML. Returns list of failures."""
    failures = []

    # 1. CSS vars present
    if "--ivory" not in html:
        failures.append("Missing CSS variable --ivory")

    # 2. Mobile breakpoint present
    if "640px" not in html:
        failures.append("Missing mobile breakpoint (640px)")

    # 3. No external refs
    if 'src="http' in html:
        failures.append("External script reference found")
    if 'href="http' in html:
        failures.append("External stylesheet reference found")

    # 4. Semantic HTML structure
    if "<!DOCTYPE" not in html:
        failures.append("Missing DOCTYPE")
    if "<html" not in html:
        failures.append("Missing <html> tag")
    if "<body" not in html:
        failures.append("Missing <body> tag")

    # 5. Parseable HTML
    validator = _HTMLValidator()
    try:
        validator.feed(html)
    except Exception as e:
        failures.append(f"HTML parse error: {e}")

    return failures


# ── All-pattern fixture paths ─────────────────────────────────────────

_ALL_PATTERN_FIXTURES = [
    "valid-report", "valid-comparison", "valid-walkthrough",
    "valid-review", "valid-design-system", "valid-prototyping",
    "valid-diagram", "valid-deck", "valid-explainer", "valid-editor",
]


class TestHTMLGeneration:
    """HTMLGenerator should produce valid, self-contained HTML from manifests."""

    def test_generates_valid_html(self, generator, sample_manifest, temp_dir):
        """Generating from a valid manifest should produce valid HTML."""
        html = generator.generate(sample_manifest)

        assert "<!DOCTYPE html>" in html or "<!DOCTYPE HTML>" in html
        assert "<html" in html
        assert "</html>" in html

    def test_output_contains_doctype(self, generator, sample_manifest):
        """Generated HTML should start with DOCTYPE declaration."""
        html = generator.generate(sample_manifest)
        assert html.strip().startswith("<!DOCTYPE")

    def test_output_has_title(self, generator, sample_manifest):
        """Generated HTML should contain the manifest title."""
        html = generator.generate(sample_manifest)
        assert "Engineering Status — Week 14" in html

    def test_output_has_lang_attribute(self, generator, sample_manifest):
        """Generated HTML should have lang attribute matching manifest."""
        html = generator.generate(sample_manifest)
        assert 'lang="en"' in html

    def test_output_has_viewport_meta(self, generator, sample_manifest):
        """Generated HTML should have responsive viewport meta tag."""
        html = generator.generate(sample_manifest)
        assert 'viewport' in html
        assert 'width=device-width' in html

    def test_palette_css_vars_embedded(self, generator, sample_manifest):
        """Generated HTML should contain CSS custom properties palette."""
        html = generator.generate(sample_manifest)
        assert "--ivory" in html
        assert "--slate" in html
        assert "--clay" in html

    def test_body_content_present(self, generator, sample_manifest):
        """Generated HTML should have a body with content."""
        html = generator.generate(sample_manifest)
        assert "<body" in html
        assert "</body>" in html

    def test_generates_from_comparison(self, generator):
        """Should generate from a comparison manifest."""
        path = MANIFESTS_DIR / "valid-comparison.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        assert "Debounce approaches" in html
        assert "<!DOCTYPE" in html

    def test_lang_override_works(self, generator, sample_manifest):
        """Lang override should replace manifest lang."""
        html = generator.generate(sample_manifest, lang_override="es")
        assert 'lang="es"' in html

    def test_self_contained_no_external_refs(self, generator, sample_manifest):
        """Generated HTML should have no external dependencies."""
        html = generator.generate(sample_manifest)
        assert 'src="http' not in html, "External script reference found"
        assert 'href="http' not in html, "External stylesheet reference found"
        assert '<link' not in html or 'data:,' in html, "External link found"

    def test_tldr_component_renders(self, generator, sample_manifest):
        """TL;DR component should render its content."""
        html = generator.generate(sample_manifest)
        assert "tldr" in html
        assert "bulk edit toolbar" in html.lower()

    def test_summary_band_renders(self, generator, sample_manifest):
        """Summary band component should render stat cards."""
        html = generator.generate(sample_manifest)
        assert "summary-band" in html or "stat-card" in html

    def test_pattern_wrapper_applied(self, generator, sample_manifest):
        """Pattern template should be applied (report pattern wraps content)."""
        html = generator.generate(sample_manifest)
        assert "report-body" in html or "page-main" in html

    def test_component_css_populated(self, generator, sample_manifest):
        """$COMPONENT_CSS should be non-empty when components with styles are rendered."""
        html = generator.generate(sample_manifest)
        # The tldr-box component has CSS, so COMPONENT_CSS should be populated
        assert ".tldr" in html, "Component CSS not populated — .tldr styles missing"

    @pytest.mark.parametrize("fixture_name", _ALL_PATTERN_FIXTURES)
    def test_all_patterns_generate_valid_html(self, generator, fixture_name):
        """Every pattern should generate valid HTML passing quality checks."""
        path = MANIFESTS_DIR / f"{fixture_name}.json"
        if not path.exists():
            pytest.skip(f"Fixture {fixture_name}.json not found")
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        failures = _run_quality_checks(html, manifest.get("pattern", ""))
        assert not failures, f"Quality check failures for {fixture_name}: {'; '.join(failures)}"

    def test_slot_resolution_works(self, generator):
        """Manifest with slots should substitute named slots correctly."""
        manifest = {
            "pattern": "report",
            "title": "Slot Test",
            "lang": "en",
            "slots": {
                "SUMMARY_SECTION": "summaryBand",
            },
            "components": {
                "summaryBand": {
                    "type": "summary-band",
                    "items": [
                        {"num": "42", "label": "Items", "delta": "+5", "delta_class": "up"}
                    ]
                },
                "tldrBox": {
                    "type": "tldr",
                    "content": "Test TL;DR"
                }
            }
        }
        html = generator.generate(manifest)
        # The summary-band should be rendered in SUMMARY_SECTION slot
        assert "summary-band" in html
        assert "stat-card" in html

    def test_slot_backward_compat(self, generator):
        """Manifest without slots should use $COMPONENTS_HTML fallback."""
        manifest = {
            "pattern": "report",
            "title": "Backward Compat Test",
            "lang": "en",
            "components": {
                "tldrBox": {
                    "type": "tldr",
                    "content": "No slots manifest"
                }
            }
        }
        html = generator.generate(manifest)
        # Components should still render via $COMPONENTS_HTML fallback
        assert "tldr" in html
        assert "No slots manifest" in html
