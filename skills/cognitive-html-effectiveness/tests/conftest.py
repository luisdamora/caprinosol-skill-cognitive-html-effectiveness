"""Pytest fixtures for cognitive-html-effectiveness tests."""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict

import pytest

from scripts.generate import (
    DEFAULT_PALETTE,
    HTMLGenerator,
    ManifestValidator,
    SKILL_DIR,
    TEMPLATES_DIR,
    TemplateLoader,
)


# ── Fixture paths ─────────────────────────────────────────────────────

FIXTURES_DIR = Path(__file__).parent / "fixtures"
MANIFESTS_DIR = FIXTURES_DIR / "manifests"
SCHEMA_PATH = SKILL_DIR / "manifest-schema.json"


# ── Fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def validator() -> ManifestValidator:
    """Provide a ManifestValidator instance."""
    return ManifestValidator(SCHEMA_PATH)


@pytest.fixture
def loader() -> TemplateLoader:
    """Provide a TemplateLoader instance."""
    return TemplateLoader(TEMPLATES_DIR)


@pytest.fixture
def generator() -> HTMLGenerator:
    """Provide an HTMLGenerator instance."""
    return HTMLGenerator()


@pytest.fixture
def sample_manifest() -> Dict[str, Any]:
    """Load a valid sample manifest."""
    path = MANIFESTS_DIR / "valid-report.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def temp_dir() -> Path:
    """Provide a temporary directory for output files."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def manifest_paths() -> Dict[str, Path]:
    """Provide paths to all fixture manifests."""
    return {p.stem: p for p in MANIFESTS_DIR.glob("*.json")}


@pytest.fixture
def default_palette() -> Dict[str, str]:
    """Provide the default palette dict."""
    return dict(DEFAULT_PALETTE)
