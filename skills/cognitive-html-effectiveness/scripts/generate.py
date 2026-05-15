#!/usr/bin/env python3
"""
cognitive-html-effectiveness — Template-based HTML Generator

Usage:
    python generate.py manifest.json [--output output.html] [--lang es|en]

Reads manifest.json, validates against manifest-schema.json, loads templates,
resolves palette overrides from AGENTS.md, composes HTML from components and
patterns via string.Template, and writes a self-contained HTML file.

Zero pip install required. Uses Python 3.6+ stdlib only.
"""

import argparse
import json
import os
import re
import string
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# ── Paths ──────────────────────────────────────────────────────────────

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
SCHEMA_PATH = SKILL_DIR / "manifest-schema.json"


# ── Default Palette ────────────────────────────────────────────────────

DEFAULT_PALETTE: Dict[str, str] = {
    "--ivory": "#FAF9F5",
    "--slate": "#141413",
    "--clay": "#D97757",
    "--clay-d": "#B85C3E",
    "--oat": "#E3DACC",
    "--olive": "#788C5D",
    "--rust": "#B04A3F",
    "--gray-050": "#F7F5EF",
    "--gray-100": "#F0EEE6",
    "--gray-200": "#E6E3DA",
    "--gray-300": "#D1CFC5",
    "--gray-500": "#87867F",
    "--gray-700": "#3D3D3A",
    "--white": "#FFFFFF",
    "--font-display": 'ui-serif, "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif',
    "--font-body": 'ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
    "--font-mono": 'ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace',
    "--text-display": "clamp(2.4rem, 4vw, 3.4rem)",
    "--text-h1": "clamp(1.85rem, 2.8vw, 2.5rem)",
    "--text-h2": "clamp(1.45rem, 2vw, 1.85rem)",
    "--text-h3": "1.25rem",
    "--text-body": "1rem",
    "--text-small": "0.875rem",
    "--text-micro": "0.75rem",
    "--space-1": "4px",
    "--space-2": "8px",
    "--space-3": "12px",
    "--space-4": "16px",
    "--space-5": "24px",
    "--space-6": "32px",
    "--space-7": "48px",
    "--space-8": "64px",
    "--container-reading": "72ch",
    "--container-page": "1180px",
    "--container-wide": "1380px",
    "--radius-1": "6px",
    "--radius-2": "10px",
    "--radius-3": "16px",
    "--radius-panel": "var(--radius-3)",
    "--radius-row": "var(--radius-2)",
    "--radius-pill": "999px",
    "--border": '1.5px solid var(--gray-300)',
    "--shadow-1": "0 1px 2px rgba(20, 20, 19, 0.06)",
    "--shadow-2": "0 10px 30px rgba(20, 20, 19, 0.08)",
    "--focus-ring": "0 0 0 3px rgba(217, 119, 87, 0.2)",
}

# Map component type in manifest to template filename (without .html suffix)
COMPONENT_TEMPLATE_MAP: Dict[str, str] = {
    "tldr": "tldr-box",
    "summary-band": "summary-band",
    "tradeoff-table": "tradeoff-table",
    "chips": "chips",
    "timeline": "timeline",
    "collapsible": "collapsible",
    "code-panel": "code-panel",
    "tabs": "tabs",
    "callout": "callout",
    "action-items": "action-items",
    "data-table": "data-table",
    "progress-bar": "progress-bar",
    "decision-card": "decision-card",
    "faq": "faq",
    "sidebar-nav": "sidebar-nav",
}

PATTERN_TEMPLATE_MAP: Dict[str, str] = {
    "comparison": "comparison",
    "walkthrough": "walkthrough",
    "review": "review",
    "design-system": "design-system",
    "prototyping": "prototyping",
    "diagram": "diagram",
    "deck": "deck",
    "explainer": "explainer",
    "report": "report",
    "editor": "editor",
}


# ── Utility ────────────────────────────────────────────────────────────

def _fmt_error(msg: str) -> str:
    """Format an error message for stderr."""
    return f"Error: {msg}"


def _die(msg: str, code: int = 1) -> None:
    """Print error message and exit."""
    print(_fmt_error(msg), file=sys.stderr)
    sys.exit(code)


# ── ManifestValidator ──────────────────────────────────────────────────

class ManifestValidator:
    """Validates a manifest dict against manifest-schema.json using jsonschema."""

    def __init__(self, schema_path: Path = SCHEMA_PATH):
        self.schema = self._load_schema(schema_path)

    def _load_schema(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            _die(f"Schema file not found: {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            _die(f"Invalid schema JSON at {path}: {e}")

    def validate(self, manifest: Dict[str, Any]) -> None:
        """
        Validate manifest against schema. Raises SystemExit (via _die) on failure.
        Uses jsonschema if available, falls back to manual checks.
        """
        try:
            import jsonschema
            try:
                jsonschema.validate(instance=manifest, schema=self.schema)
                return
            except jsonschema.exceptions.ValidationError as e:
                path = " → ".join(str(p) for p in e.absolute_path) if e.absolute_path else "root"
                _die(f"Validation failed at {path}: {e.message}")
        except ImportError:
            self._manual_validate(manifest)

    def _manual_validate(self, manifest: Dict[str, Any]) -> None:
        """Fallback manual validation when jsonschema is not available."""
        errors: List[str] = []

        # Required top-level fields
        for field in ("pattern", "title", "lang", "components"):
            if field not in manifest:
                errors.append(f"Missing required top-level field: '{field}'")

        if errors:
            _die("\n".join(errors))

        # pattern enum check
        valid_patterns = set(PATTERN_TEMPLATE_MAP.keys())
        if manifest.get("pattern") not in valid_patterns:
            _die(
                f"Invalid pattern '{manifest.get('pattern')}'. Must be one of: "
                f"{', '.join(sorted(valid_patterns))}"
            )

        # lang enum check
        if manifest.get("lang") not in ("en", "es"):
            _die(f"Invalid lang '{manifest.get('lang')}'. Must be 'en' or 'es'.")

        # title length
        if len(manifest.get("title", "")) > 120:
            _die(f"Title exceeds 120 characters ({len(manifest['title'])} chars).")

        # components must be a non-empty object
        components = manifest.get("components", {})
        if not isinstance(components, dict) or len(components) == 0:
            _die("'components' must be a non-empty object.")

        # Validate each component has a valid type
        valid_types = set(COMPONENT_TEMPLATE_MAP.keys())
        for key, comp in components.items():
            if not isinstance(comp, dict):
                errors.append(f"Component '{key}' must be an object.")
                continue
            if "type" not in comp:
                errors.append(f"Component '{key}' is missing required field 'type'.")
            elif comp["type"] not in valid_types:
                errors.append(
                    f"Component '{key}' has invalid type '{comp['type']}'. "
                    f"Must be one of: {', '.join(sorted(valid_types))}"
                )

        if errors:
            _die("\n".join(errors))


# ── TemplateLoader ─────────────────────────────────────────────────────

class TemplateLoader:
    """Loads and caches string.Template objects from the templates directory."""

    _JOIN_PATTERN = re.compile(r'\$JOIN\{([^}]+)\}')

    def __init__(self, templates_dir: Path = TEMPLATES_DIR):
        self.templates_dir = templates_dir
        self._cache: Dict[str, string.Template] = {}

    def load(self, name: str) -> string.Template:
        """
        Load a template by name (without .html suffix).
        Searches: templates/<name>.html, templates/components/<name>.html,
                  templates/patterns/<name>.html
        """
        if name in self._cache:
            return self._cache[name]

        paths = [
            self.templates_dir / f"{name}.html",
            self.templates_dir / "components" / f"{name}.html",
            self.templates_dir / "patterns" / f"{name}.html",
        ]

        for path in paths:
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                tmpl = string.Template(content)
                self._cache[name] = tmpl
                return tmpl

        _die(f"Template not found: '{name}' (searched: {', '.join(str(p) for p in paths)})")

    def resolve_component_template(self, component_type: str) -> string.Template:
        """Resolve a component type to its template filename."""
        filename = COMPONENT_TEMPLATE_MAP.get(component_type)
        if not filename:
            _die(f"Unknown component type: '{component_type}'")
        return self.load(filename)

    def resolve_pattern_template(self, pattern_name: str) -> string.Template:
        """Resolve a pattern name to its template filename."""
        filename = PATTERN_TEMPLATE_MAP.get(pattern_name)
        if not filename:
            _die(f"Unknown pattern: '{pattern_name}'")
        return self.load(filename)


# ── HTMLGenerator ──────────────────────────────────────────────────────

class HTMLGenerator:
    """Orchestrates HTML generation from manifest + templates."""

    _STYLE_RE = re.compile(r'<style[^>]*>(.*?)</style>', re.DOTALL)

    def __init__(
        self,
        template_loader: Optional[TemplateLoader] = None,
        validator: Optional[ManifestValidator] = None,
        skill_dir: Path = SKILL_DIR,
    ):
        self.loader = template_loader or TemplateLoader()
        self.validator = validator or ManifestValidator()
        self.skill_dir = skill_dir

    # ── Palette Resolution ───────────────────────────────────────────

    def resolve_palette(self, manifest_palette: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Resolve palette: start with defaults, merge AGENTS.md overrides,
        then merge manifest overrides.
        """
        palette = dict(DEFAULT_PALETTE)

        # Check AGENTS.md in skill dir AND project root
        agents_paths = [
            self.skill_dir.parent.parent / "AGENTS.md",  # project root
            Path.cwd() / "AGENTS.md",
        ]
        for agents_path in agents_paths:
            overrides = self._parse_agents_palette(agents_path)
            if overrides:
                palette.update(overrides)

        # Manifest palette overrides
        if manifest_palette:
            for key, value in manifest_palette.items():
                css_key = f"--{key}" if not key.startswith("--") else key
                palette[css_key] = value

        return palette

    def _parse_agents_palette(self, path: Path) -> Dict[str, str]:
        """Parse palette overrides from AGENTS.md block."""
        if not path.exists():
            return {}

        content = path.read_text(encoding="utf-8")
        marker_start = "<!-- cognitive-html:palette -->"
        marker_end = "<!-- /cognitive-html:palette -->"

        start = content.find(marker_start)
        if start == -1:
            return {}
        start += len(marker_start)

        end = content.find(marker_end, start)
        if end == -1:
            return {}

        block = content[start:end].strip()
        # Remove yaml code fences if present
        if block.startswith("```yaml"):
            block = block[7:]
        if block.endswith("```"):
            block = block[:-3]

        overrides: Dict[str, str] = {}
        for line in block.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, _, val = line.partition(":")
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                css_key = f"--{key}" if not key.startswith("--") else key
                overrides[css_key] = val

        return overrides

    def palette_to_css(self, palette: Dict[str, str]) -> str:
        """Convert palette dict to CSS :root variable block."""
        lines = [":root {"]
        for key, value in palette.items():
            # Value may already include var() references — just emit directly
            lines.append(f"  {key}: {value};")
        lines.append("}")
        return "\n".join(lines)

    # ── JOIN Processing ───────────────────────────────────────────────

    def process_joins(self, template: string.Template, data: Dict[str, Any]) -> str:
        """
        Process $JOIN{name} markers in the template source.
        For each marker, look up 'name' in data, iterate array items,
        render each item through the named fragment template, join with newlines.
        Recursively processes joins inside fragment templates.
        """
        source = template.template if isinstance(template, string.Template) else template
        result = source

        for match in TemplateLoader._JOIN_PATTERN.finditer(source):
            join_key = match.group(1)
            full_marker = match.group(0)

            # Resolve the data for this join
            items = self._resolve_join_data(join_key, data)

            if not items:
                result = result.replace(full_marker, "", 1)
                continue

            # Load the fragment template
            fragment_tmpl = self.loader.load(join_key)

            rendered_fragments: List[str] = []
            for item in items:
                if isinstance(item, dict):
                    # Recursively process joins with item as data
                    processed = self.process_joins(fragment_tmpl, {**data, **item})
                    rendered = string.Template(processed).safe_substitute(**self._flatten(item))
                elif isinstance(item, (list, tuple)):
                    # Map array to colN keys (for data-table rows)
                    item_dict = {f"col{i}": str(v) for i, v in enumerate(item)}

                    # For data-table-row: pre-render $cells as <td> elements
                    if join_key == "data-table-row":
                        cells_html = "".join(
                            f'        <td>{val}</td>\n' for val in item
                        )
                        item_dict["cells"] = cells_html.rstrip('\n')

                    # For data-table-accordion-row: generate $primary_value and $fields
                    if join_key == "data-table-accordion-row":
                        columns = data.get("columns", [])
                        labels = data.get("rowFieldLabels", {})
                        primary = data.get("primaryColumn", columns[0] if columns else "")
                        primary_idx = columns.index(primary) if primary in columns else 0

                        item_dict["primary_value"] = str(item[primary_idx]) if primary_idx < len(item) else ""

                        fields_html = ""
                        for i, val in enumerate(item):
                            col_name = columns[i] if i < len(columns) else f"col{i}"
                            label = labels.get(col_name, col_name)
                            fields_html += (
                                f'      <div class="accordion-field">\n'
                                f'        <span class="accordion-label">{label}</span>\n'
                                f'        <span class="accordion-value">{val}</span>\n'
                                f'      </div>\n'
                            )
                        item_dict["fields"] = fields_html.rstrip('\n')

                    processed = self.process_joins(fragment_tmpl, item_dict)
                    rendered = string.Template(processed).safe_substitute(**item_dict)
                else:
                    rendered = fragment_tmpl.safe_substitute(value=str(item))
                rendered_fragments.append(rendered)

            joined = "\n".join(rendered_fragments)
            result = result.replace(full_marker, joined, 1)

        return result

    def _resolve_join_data(self, join_key: str, data: Dict[str, Any]) -> List[Any]:
        """Resolve $JOIN data from manifest component data."""
        # Map join key names to the data keys they reference
        join_to_data: Dict[str, str] = {
            "data-table-header": "columns",
            "data-table-row": "rows",
            "data-table-accordion-row": "rows",
            "data-table-cell": "colN",  # generated from row array
            "data-table-accordion-field": "colN",  # generated from row array
            "code-panel-line": "lines",
            "summary-band-item": "items",
            "tradeoff-table-row": "rows",
            "chip-item": "items",
            "timeline-entry": "entries",
            "action-item": "items",
            "tab-button": "tabs",
            "tab-pane": "tabs",
            "faq-item": "items",
            "sidebar-nav-link": "links",
            "sidebar-nav-file": "files",
            "decision-option": "options",
        }

        if join_key in join_to_data:
            key = join_to_data[join_key]
            if key in data and isinstance(data[key], list):
                return data[key]

        # Also try matching join_key directly as a data key
        if join_key in data and isinstance(data.get(join_key), list):
            return data[join_key]

        # Generic fallback for common keys
        for candidate_key in ("items", "rows", "entries", "tabs", "columns", "links", "files", "options", "lines"):
            if candidate_key in data and isinstance(data[candidate_key], list):
                return data[candidate_key]

        return []

    def _flatten(self, d: Dict[str, Any]) -> Dict[str, str]:
        """Flatten a dict to string values for string.Template substitution."""
        return {k: (str(v) if not isinstance(v, str) else v) for k, v in d.items()}

    # ── CSS Extraction ───────────────────────────────────────────────

    def _extract_css(self, component_html: str) -> tuple:
        """
        Extract <style> blocks from rendered component HTML.
        Returns (html_without_style_blocks, extracted_css_text).
        """
        css_parts: List[str] = []
        html_without = component_html
        for match in self._STYLE_RE.finditer(component_html):
            css_parts.append(match.group(1).strip())
        # Remove all <style> blocks from HTML
        html_without = self._STYLE_RE.sub('', html_without).strip()
        css_text = '\n'.join(css_parts)
        return (html_without, css_text)

    # ── Component Rendering ──────────────────────────────────────────

    def render_component(self, component_data: Dict[str, Any]) -> tuple:
        """
        Render a single component from its manifest data.
        Returns (rendered_html_without_styles, extracted_css_string).
        """
        comp_type = component_data.get("type", "")
        tmpl = self.loader.resolve_component_template(comp_type)

        # For data-table: pre-render $DATA_TABLE_HEADERS from columns array
        if comp_type == "data-table":
            columns = component_data.get("columns", [])
            rows = component_data.get("rows", [])
            headers_html = "".join(f'        <th>{col}</th>\n' for col in columns)
            # Build extended data with pre-rendered headers
            extended_data = dict(component_data)
            extended_data["DATA_TABLE_HEADERS"] = headers_html.rstrip('\n')

            # Handle empty table: generate "No data" row
            if not rows:
                col_count = len(columns)
                extended_data["DATA_TABLE_HEADERS"] = headers_html.rstrip('\n')
                # Add empty row placeholder
                extended_data["_empty_table"] = True

            # Process $JOIN markers
            joined_source = self.process_joins(tmpl, extended_data)

            # Substitute remaining placeholders
            flat = self._flatten(extended_data)
            result = string.Template(joined_source).safe_substitute(**flat)
        else:
            # Process $JOIN markers in the template source before substitution
            joined_source = self.process_joins(tmpl, component_data)

            # Now substitute the remaining placeholders
            flat = self._flatten(component_data)
            result = string.Template(joined_source).safe_substitute(**flat)

        # Extract CSS from component <style> blocks
        clean_html, css = self._extract_css(result)
        return (clean_html, css)

    def render_components(self, components: Dict[str, Any]) -> tuple:
        """
        Render all components from the manifest.
        Returns (joined_html, concatenated_css, per_component_html_dict).
        Deduplicates CSS: each component's style is emitted once.
        """
        html_parts: List[str] = []
        css_parts: List[str] = []
        seen_css: set = set()
        component_html_map: Dict[str, str] = {}
        for comp_key, comp_data in components.items():
            if isinstance(comp_data, dict) and "type" in comp_data:
                html, css = self.render_component(comp_data)
                html_parts.append(html)
                component_html_map[comp_key] = html
                # CSS deduplication: use hash of CSS content as key
                css_key = hash(css)
                if css_key not in seen_css and css.strip():
                    seen_css.add(css_key)
                    css_parts.append(css)
        return ("\n".join(html_parts), "\n".join(css_parts), component_html_map)

    # ── Pattern Rendering ────────────────────────────────────────────

    def render_pattern(self, pattern_name: str, components_html: str,
                       slot_map: Optional[Dict[str, str]] = None,
                       component_html_map: Optional[Dict[str, str]] = None) -> str:
        """
        Render a pattern template by wrapping the combined components HTML.
        If slot_map provided: substitute each $SLOT_NAME with its component HTML.
        If not: fall back to $COMPONENTS_HTML for backward compat.
        Unmapped slots resolve to empty string (no error).
        Invalid slot reference (non-existent component key) → error.
        """
        tmpl = self.loader.resolve_pattern_template(pattern_name)

        # Build substitution dict with fallback
        subst: Dict[str, str] = {
            "COMPONENTS_HTML": components_html,
        }

        if slot_map and component_html_map:
            for slot_name, comp_key in slot_map.items():
                if comp_key not in component_html_map:
                    _die(f"Invalid slot reference: '{comp_key}' is not a valid component key in manifest")
                subst[slot_name] = component_html_map[comp_key]

        result = tmpl.safe_substitute(**subst)
        return result

    # ── Full Generation ──────────────────────────────────────────────

    def generate(
        self,
        manifest: Dict[str, Any],
        lang_override: Optional[str] = None,
    ) -> str:
        """
        Full generation pipeline:
        1. Validate manifest
        2. Resolve palette
        3. Render all components
        4. Render pattern
        5. Compose into base.html
        """
        # 1. Validate
        self.validator.validate(manifest)

        # 2. Resolve palette
        lang = lang_override or manifest.get("lang", "en")
        palette = self.resolve_palette(manifest.get("palette"))
        css_tokens = self.palette_to_css(palette)

        # 3. Render components
        components_data = manifest.get("components", {})
        body_html, component_css, component_html_map = self.render_components(components_data)

        # 4. Render pattern if applicable
        pattern_name = manifest.get("pattern", "")
        slot_map = manifest.get("slots")
        if pattern_name:
            body_html = self.render_pattern(
                pattern_name, body_html,
                slot_map=slot_map,
                component_html_map=component_html_map,
            )

        # 5. Compose into base.html
        base_tmpl = self.loader.load("base")
        export_js = manifest.get("exportJs", "")

        final_html = base_tmpl.safe_substitute(
            PAGE_TITLE=manifest.get("title", "Untitled"),
            PAGE_LANG=lang,
            EYEBROW=manifest.get("eyebrow", ""),
            PALETTE_CSS=css_tokens,
            COMPONENT_CSS=component_css,
            BODY_HTML=body_html,
            EXPORT_JS=export_js,
        )

        return final_html


# ── CLI ────────────────────────────────────────────────────────────────

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate self-contained HTML from a manifest JSON file.",
        epilog="Example: python generate.py manifest.json --output report.html --lang es",
    )
    parser.add_argument(
        "manifest",
        type=str,
        help="Path to the manifest JSON file",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Output HTML file path (default: <manifest-stem>.html)",
    )
    parser.add_argument(
        "--lang",
        "-l",
        type=str,
        default=None,
        choices=["en", "es"],
        help="Override language (overrides manifest lang)",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    # Resolve manifest path
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        _die(f"Manifest file not found: {manifest_path}")

    # Read manifest
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest: Dict[str, Any] = json.load(f)
    except json.JSONDecodeError as e:
        _die(f"Invalid JSON in manifest: {e}")

    # Resolve output path
    if args.output:
        output_path = Path(args.output)
    else:
        stem = manifest_path.stem
        output_path = manifest_path.parent / f"{stem}.html"

    # Generate
    generator = HTMLGenerator()
    html = generator.generate(manifest, lang_override=args.lang)

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated: {output_path.resolve()}", file=sys.stdout)


if __name__ == "__main__":
    main()
