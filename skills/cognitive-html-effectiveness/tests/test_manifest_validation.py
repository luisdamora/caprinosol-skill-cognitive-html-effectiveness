"""Tests for ManifestValidator — validates manifests against JSON Schema."""

import json

import pytest

from tests.conftest import MANIFESTS_DIR


class TestManifestValidation:
    """ManifestValidator should accept valid manifests and reject invalid ones."""

    def test_valid_manifest_passes(self, validator, sample_manifest):
        """A valid manifest with all required fields should pass without errors."""
        # Should not raise SystemExit
        validator.validate(sample_manifest)

    def test_valid_comparison_manifest_passes(self, validator):
        """A valid comparison manifest should pass."""
        path = MANIFESTS_DIR / "valid-comparison.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        validator.validate(manifest)

    def test_missing_required_field_rejected(self, validator):
        """Manifest missing 'pattern' should be rejected."""
        path = MANIFESTS_DIR / "missing-field.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        with pytest.raises(SystemExit) as exc:
            validator.validate(manifest)
        assert exc.value.code == 1

    def test_invalid_component_type_rejected(self, validator):
        """Component with 'type' not in valid enum should be rejected."""
        path = MANIFESTS_DIR / "invalid-type.json"
        with open(path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        with pytest.raises(SystemExit) as exc:
            validator.validate(manifest)
        assert exc.value.code == 1

    def test_empty_components_rejected(self, validator):
        """Manifest with empty components object should be rejected."""
        manifest = {
            "pattern": "report",
            "title": "Test",
            "lang": "en",
            "components": {}
        }
        with pytest.raises(SystemExit) as exc:
            validator.validate(manifest)
        assert exc.value.code == 1

    def test_invalid_pattern_rejected(self, validator):
        """Pattern name not in the enum should be rejected."""
        manifest = {
            "pattern": "invalid-pattern-name",
            "title": "Test",
            "lang": "en",
            "components": {
                "tldrBox": {
                    "type": "tldr",
                    "content": "Test"
                }
            }
        }
        with pytest.raises(SystemExit) as exc:
            validator.validate(manifest)
        assert exc.value.code == 1

    def test_invalid_lang_rejected(self, validator):
        """Language not in ['en', 'es'] should be rejected."""
        manifest = {
            "pattern": "report",
            "title": "Test",
            "lang": "fr",
            "components": {
                "tldrBox": {
                    "type": "tldr",
                    "content": "Test"
                }
            }
        }
        with pytest.raises(SystemExit) as exc:
            validator.validate(manifest)
        assert exc.value.code == 1

    def test_title_too_long_rejected(self, validator):
        """Title exceeding 120 characters should be rejected."""
        manifest = {
            "pattern": "report",
            "title": "X" * 121,
            "lang": "en",
            "components": {
                "tldrBox": {
                    "type": "tldr",
                    "content": "Test"
                }
            }
        }
        with pytest.raises(SystemExit) as exc:
            validator.validate(manifest)
        assert exc.value.code == 1

    def test_component_type_missing_rejected(self, validator):
        """Component without 'type' field should be rejected."""
        manifest = {
            "pattern": "report",
            "title": "Test",
            "lang": "en",
            "components": {
                "badComp": {
                    "content": "Missing type field"
                }
            }
        }
        with pytest.raises(SystemExit) as exc:
            validator.validate(manifest)
        assert exc.value.code == 1
