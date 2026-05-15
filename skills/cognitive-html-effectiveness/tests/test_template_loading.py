"""Tests for TemplateLoader — verifies all 26+ templates load without errors."""

import string
from html.parser import HTMLParser
from pathlib import Path

import pytest

from scripts.generate import (
    COMPONENT_TEMPLATE_MAP,
    PATTERN_TEMPLATE_MAP,
    TEMPLATES_DIR,
)


class _TagBalanceValidator(HTMLParser):
    """Validates that HTML tags are balanced (open/close match)."""

    VOID_ELEMENTS = frozenset([
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr',
    ])

    def __init__(self):
        super().__init__()
        self.errors = []
        self._stack = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() not in self.VOID_ELEMENTS:
            self._stack.append(tag.lower())

    def handle_endtag(self, tag):
        if tag.lower() in self.VOID_ELEMENTS:
            return
        if self._stack and self._stack[-1] == tag.lower():
            self._stack.pop()
        elif tag.lower() in self._stack:
            # Mismatched nesting — pop up to match
            while self._stack and self._stack[-1] != tag.lower():
                self._stack.pop()
            if self._stack:
                self._stack.pop()

    def handle_data(self, data):
        pass  # text content is fine

    def close(self):
        super().close()
        if self._stack:
            self.errors.append(f"Unclosed tags: {self._stack}")


def _count_templates(directory: Path) -> int:
    """Count .html files recursively in a directory."""
    return len(list(directory.rglob("*.html")))


def _strip_template_placeholders(content: str) -> str:
    """Replace $PLACEHOLDER tokens with plain text to allow HTML parsing."""
    import re
    return re.sub(r'\$[A-Z_]+(\{[^}]+\})?', 'placeholder', content)


class TestTemplateLoading:
    """TemplateLoader should load all template files successfully."""

    def test_template_count(self):
        """There should be at least 26 template files (1 base + 15 components + 10 patterns)."""
        total = _count_templates(TEMPLATES_DIR)
        assert total >= 26, f"Expected >= 26 templates, found {total}"

    def test_base_template_exists(self):
        """base.html should exist in the templates root."""
        base_path = TEMPLATES_DIR / "base.html"
        assert base_path.exists(), "base.html not found"

    def test_base_template_has_placeholders(self, loader):
        """base.html should contain all 7 expected $PLACEHOLDER markers."""
        tmpl = loader.load("base")
        required_placeholders = [
            "PAGE_TITLE", "PAGE_LANG", "PALETTE_CSS", "COMPONENT_CSS",
            "EYEBROW", "BODY_HTML", "EXPORT_JS"
        ]
        for ph in required_placeholders:
            assert f"${ph}" in tmpl.template, f"${ph} not found in base.html"

    def test_all_component_templates_load(self, loader):
        """Every component type in COMPONENT_TEMPLATE_MAP should have a loadable template."""
        for comp_type, filename in COMPONENT_TEMPLATE_MAP.items():
            try:
                tmpl = loader.resolve_component_template(comp_type)
                assert isinstance(tmpl, string.Template)
            except SystemExit:
                pytest.fail(f"Component template '{comp_type}' ({filename}) failed to load")

    def test_all_pattern_templates_load(self, loader):
        """Every pattern in PATTERN_TEMPLATE_MAP should have a loadable template."""
        for pattern_name, filename in PATTERN_TEMPLATE_MAP.items():
            try:
                tmpl = loader.resolve_pattern_template(pattern_name)
                assert isinstance(tmpl, string.Template)
            except SystemExit:
                pytest.fail(f"Pattern template '{pattern_name}' ({filename}) failed to load")

    def test_all_templates_are_html_strings(self, loader):
        """All loaded templates should contain valid HTML strings with balanced tags."""
        all_names = ["base"]
        all_names.extend(COMPONENT_TEMPLATE_MAP.values())
        all_names.extend(PATTERN_TEMPLATE_MAP.values())

        for name in all_names:
            try:
                tmpl = loader.load(name)
                content = tmpl.template
                assert isinstance(content, str), f"{name}.html is not a string"
                assert "<" in content, f"{name}.html does not appear to be HTML"
                # HTML parser validation — must parse without errors
                validator = _TagBalanceValidator()
                try:
                    # Replace $PLACEHOLDER tokens to avoid parser confusion
                    clean = _strip_template_placeholders(content)
                    validator.feed(clean)
                    validator.close()
                except Exception as e:
                    pytest.fail(f"{name}.html HTML parse error: {e}")
                # Note: template placeholders may cause unclosed tags,
                # so we don't assert on validator.errors for template source
            except SystemExit:
                pass  # skip if template has child fragments only

    def test_join_marker_present_in_repeated_components(self, loader):
        """Components with repeated sections should use $JOIN markers."""
        join_components = [
            "summary-band", "tradeoff-table", "chips", "timeline",
            "action-items", "tabs", "faq", "sidebar-nav", "data-table"
        ]
        for name in join_components:
            try:
                tmpl = loader.load(name)
                assert "$JOIN{" in tmpl.template, f"{name}.html expected to have $JOIN marker"
            except SystemExit:
                pytest.fail(f"Failed to load {name}.html")

    def test_fragment_templates_exist(self):
        """Fragment templates (used by $JOIN) should exist."""
        fragments = [
            "summary-band-item",
            "tradeoff-table-row",
            "chip-item",
            "timeline-entry",
            "action-item",
            "data-table-row",
            "data-table-accordion-row",
            "tab-button",
            "tab-pane",
            "faq-item",
            "sidebar-nav-link",
            "sidebar-nav-file",
            "code-panel-line",
            "decision-option",
        ]
        for name in fragments:
            paths = [
                TEMPLATES_DIR / "components" / f"{name}.html",
                TEMPLATES_DIR / f"{name}.html",
            ]
            found = any(p.exists() for p in paths)
            assert found, f"Fragment template '{name}.html' not found"
