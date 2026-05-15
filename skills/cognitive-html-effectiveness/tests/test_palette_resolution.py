"""Tests for palette resolution — verifies default and override behavior."""

import json
from pathlib import Path
from typing import Any, Dict

import pytest

from scripts.generate import DEFAULT_PALETTE, HTMLGenerator
from tests.conftest import MANIFESTS_DIR


class TestPaletteResolution:
    """Palette resolution should merge defaults with AGENTS.md and manifest overrides."""

    def test_default_palette_has_all_keys(self, default_palette):
        """Default palette should contain all essential design tokens."""
        essential_keys = [
            "--ivory", "--slate", "--clay", "--oat", "--olive", "--rust",
            "--font-display", "--font-body", "--font-mono",
            "--text-display", "--text-h1", "--text-h2", "--text-body",
            "--space-1", "--space-4", "--space-8",
            "--container-reading", "--container-page",
            "--radius-panel", "--radius-row",
        ]
        for key in essential_keys:
            assert key in default_palette, f"Missing default token: {key}"

    def test_generated_html_has_default_css_vars(self, generator):
        """Generated HTML should contain default palette CSS variables."""
        path = MANIFESTS_DIR / "valid-report.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        # Check a few key default vars are in the output
        assert "#FAF9F5" in html  # default ivory
        assert "#141413" in html  # default slate
        assert "#D97757" in html  # default clay

    def test_palette_override_merges_in_html(self, generator):
        """Manifest palette override should appear in output CSS."""
        path = MANIFESTS_DIR / "palette-override.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        # Check overridden values appear
        assert "#FEFEFE" in html  # overridden ivory
        assert "#1A1A2E" in html  # overridden slate
        assert "#E94560" in html  # overridden clay
        # And some defaults should still be there
        assert "#788C5D" in html  # default olive (not overridden)

    def test_partial_override_keeps_rest_default(self, generator):
        """Partial palette override should keep unset keys at defaults."""
        html = generator.generate({
            "pattern": "report",
            "title": "Partial Override Test",
            "lang": "en",
            "palette": {"clay": "#FF0000"},
            "components": {
                "tldrBox": {
                    "type": "tldr",
                    "content": "Test"
                }
            }
        })
        assert "#FF0000" in html, "Override value not found"
        assert "#FAF9F5" in html, "Default value missing after override"

    def test_palette_css_block_format(self, generator, sample_manifest):
        """Palette should be rendered as :root CSS variable block."""
        palette = generator.resolve_palette({})
        css = generator.palette_to_css(palette)
        assert css.strip().startswith(":root {")
        assert css.strip().endswith("}")
        assert "--ivory" in css
        assert "--slate" in css

    def test_agents_md_override(self, generator, temp_dir, monkeypatch):
        """AGENTS.md palette block should be parsed and merged."""
        agents_content = """<!-- cognitive-html:palette -->
```yaml
ivory: "#EEEEEE"
olive: "#112233"
```
<!-- /cognitive-html:palette -->
"""
        agents_path = temp_dir / "AGENTS.md"
        agents_path.write_text(agents_content, encoding="utf-8")

        # Monkeypatch the generator's skill_dir lookup
        original_parse = generator._parse_agents_palette

        def mock_parse(path: Path) -> Dict[str, str]:
            return original_parse(agents_path)

        monkeypatch.setattr(generator, '_parse_agents_palette', mock_parse)

        palette = generator.resolve_palette({"clay": "#AABBCC"})
        assert palette.get("--ivory") == "#EEEEEE"
        assert palette.get("--olive") == "#112233"
        assert palette.get("--clay") == "#AABBCC"  # manifest overrides agents
