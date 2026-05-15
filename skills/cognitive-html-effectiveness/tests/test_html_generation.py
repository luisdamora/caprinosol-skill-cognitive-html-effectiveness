"""Tests for HTML generation — verifies output structure and correctness."""

import json

import pytest

from tests.conftest import MANIFESTS_DIR


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
