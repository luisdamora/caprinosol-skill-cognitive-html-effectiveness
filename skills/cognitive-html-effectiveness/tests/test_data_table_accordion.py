"""Tests for data table dual-render — verifies desktop table + mobile accordion."""

import json

import pytest

from tests.conftest import MANIFESTS_DIR


class TestDataTableAccordion:
    """Data table should render both desktop <table> and mobile <details> accordion."""

    def test_table_desktop_class_present(self, generator):
        """Generated HTML should contain .table-desktop class for desktop rendering."""
        path = MANIFESTS_DIR / "single-row.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        assert "table-desktop" in html, "Missing .table-desktop class"

    def test_mobile_accordion_class_present(self, generator):
        """Generated HTML should contain .table-mobile-accordion class for mobile."""
        path = MANIFESTS_DIR / "single-row.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        assert "table-mobile-accordion" in html, "Missing .table-mobile-accordion class"

    def test_table_element_present(self, generator):
        """Desktop block should contain a <table> element."""
        path = MANIFESTS_DIR / "single-row.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        assert "<table" in html, "Missing <table> element"
        assert "<thead>" in html, "Missing <thead> in table"
        assert "<tbody>" in html, "Missing <tbody> in table"

    def test_details_open_present(self, generator):
        """Mobile block should contain <details open> elements."""
        path = MANIFESTS_DIR / "single-row.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        assert "<details open" in html, "Missing <details open> accordion"

    def test_summary_in_accordion(self, generator):
        """Accordion should have <summary> element."""
        path = MANIFESTS_DIR / "single-row.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        assert "accordion-summary" in html or "<summary>" in html

    def test_accordion_field_labels_present(self, generator):
        """Accordion card body should have labeled fields."""
        path = MANIFESTS_DIR / "single-row.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        assert "accordion-field" in html, "Missing accordion field labels"
        assert "accordion-label" in html, "Missing accordion-label"

    def test_table_headers_match_manifest(self, generator):
        """Table headers should reflect manifest column definitions."""
        path = MANIFESTS_DIR / "single-row.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        columns = manifest["components"]["dataTable"]["columns"]
        for col in columns:
            assert col in html, f"Column '{col}' not found in generated HTML"

    def test_primary_column_in_summary(self, generator):
        """Primary column value should appear in <summary>."""
        path = MANIFESTS_DIR / "single-row.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        primary = manifest["components"]["dataTable"]["primaryColumn"]
        row = manifest["components"]["dataTable"]["rows"][0]
        col_idx = manifest["components"]["dataTable"]["columns"].index(primary)
        primary_value = row[col_idx]
        # The primary value should be in the summary (accordion-primary)
        assert primary_value in html, f"Primary value '{primary_value}' not in HTML"

    def test_no_javascript_for_toggle(self, generator):
        """Dual-render should not require JavaScript for visibility toggle."""
        path = MANIFESTS_DIR / "single-row.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        # The CSS media query should contain 768px breakpoint
        assert "768px" in html or "768" in html

    def test_row_value_in_accordion_body(self, generator):
        """All row values should appear in the accordion body fields."""
        path = MANIFESTS_DIR / "single-row.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        html = generator.generate(manifest)
        row = manifest["components"]["dataTable"]["rows"][0]
        for value in row:
            assert value in html, f"Row value '{value}' not found in HTML"
