#!/usr/bin/env python3
"""Validate the proven-python repository.

Run from the repository root, this performs three checks:

1. The plugin and marketplace manifests are valid JSON and carry their required fields.
2. Every relative link in the skill and its references resolves to a real file.
3. No file contains an em dash or an en dash.

Exit status is 0 when the repository is clean and 1 when any check fails. Run it with
``python scripts/validate_repo.py``, or point it at another tree with ``--root PATH``.
"""

from __future__ import annotations

import argparse
import json
import re
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path

EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)
DASHES = (EM_DASH, EN_DASH)

EXCLUDED_DIRS = frozenset(
    {
        ".git",
        ".context",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        ".mypy_cache",
        ".ruff_cache",
        ".pytest_cache",
    }
)

PLUGIN_REQUIRED_FIELDS = ("name", "version", "description")
MARKETPLACE_REQUIRED_FIELDS = ("name", "owner", "plugins")
PLUGIN_ENTRY_REQUIRED_FIELDS = ("name", "source")

_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
_SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)


@dataclass(frozen=True)
class Violation:
    """A single validation failure.

    Attributes:
        kind: The failed check, one of "dash", "link", or "manifest".
        path: The repository-relative path of the offending file.
        detail: A human-readable description of the problem.
        line: The 1-based line number, when the problem is tied to one line.
    """

    kind: str
    path: str
    detail: str
    line: int | None = None

    def render(self) -> str:
        """Return a one-line, human-readable rendering of this violation."""
        where = self.path if self.line is None else f"{self.path}:{self.line}"
        return f"[{self.kind}] {where}: {self.detail}"


def iter_files(root: Path) -> Iterator[Path]:
    """Yield every file under root in sorted order, skipping excluded directories."""
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def _read_text(path: Path) -> str | None:
    """Return the file's text, or None when it is not valid UTF-8 (treated as binary)."""
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def scan_dashes(root: Path) -> list[Violation]:
    """Return a violation for every em dash or en dash in any text file under root."""
    violations: list[Violation] = []
    for path in iter_files(root):
        text = _read_text(path)
        if text is None:
            continue
        rel = path.relative_to(root).as_posix()
        for lineno, line in enumerate(text.splitlines(), start=1):
            if EM_DASH in line:
                violations.append(Violation("dash", rel, "contains an em dash", lineno))
            if EN_DASH in line:
                violations.append(Violation("dash", rel, "contains an en dash", lineno))
    return violations


def _non_fenced_lines(text: str) -> Iterator[tuple[int, str]]:
    """Yield (1-based line number, text) for lines outside fenced code blocks."""
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield lineno, line


def _link_candidates(line: str) -> list[str]:
    """Return link targets on a line: Markdown links and code-span paths ending in .md."""
    targets: list[str] = []
    for match in _MD_LINK_RE.finditer(line):
        targets.append(match.group(1).strip().strip("<>").split()[0])
    for match in _CODE_SPAN_RE.finditer(line):
        span = match.group(1).strip()
        if "/" in span and span.endswith(".md"):
            targets.append(span)
    return targets


def _is_relative_target(target: str) -> bool:
    """Return True when target is a path to resolve, not a URL or a bare anchor."""
    if not target or target.startswith("#"):
        return False
    return not _SCHEME_RE.match(target)


def scan_links(root: Path) -> list[Violation]:
    """Return a violation for every relative link under skills/ that does not resolve."""
    skill_root = root / "skills"
    violations: list[Violation] = []
    for path in iter_files(root):
        if path.suffix != ".md" or skill_root not in path.parents:
            continue
        text = _read_text(path)
        if text is None:
            continue
        rel = path.relative_to(root).as_posix()
        for lineno, line in _non_fenced_lines(text):
            for target in _link_candidates(line):
                if not _is_relative_target(target):
                    continue
                clean = target.split("#", 1)[0].split("?", 1)[0]
                if not clean:
                    continue
                if not (path.parent / clean).resolve().is_file():
                    detail = f"link target does not resolve: {target}"
                    violations.append(Violation("link", rel, detail, lineno))
    return violations


def _load_manifest(path: Path, root: Path) -> tuple[dict[str, object] | None, list[Violation]]:
    """Load a JSON manifest, returning the parsed object or the violations that block it."""
    rel = path.relative_to(root).as_posix()
    if not path.is_file():
        return None, [Violation("manifest", rel, "manifest file is missing")]
    text = _read_text(path)
    if text is None:
        return None, [Violation("manifest", rel, "manifest is not valid UTF-8")]
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, [Violation("manifest", rel, f"invalid JSON: {exc.msg} (line {exc.lineno})")]
    if not isinstance(data, dict):
        return None, [Violation("manifest", rel, "top level must be a JSON object")]
    return data, []


def _missing_fields(data: dict[str, object], fields: Sequence[str], rel: str) -> list[Violation]:
    """Return a violation for each required field absent from data."""
    return [
        Violation("manifest", rel, f"missing required field: {field}")
        for field in fields
        if field not in data
    ]


def validate_plugin_manifest(path: Path, root: Path) -> list[Violation]:
    """Validate the plugin manifest at path and return any violations."""
    data, blocking = _load_manifest(path, root)
    if data is None:
        return blocking
    rel = path.relative_to(root).as_posix()
    return _missing_fields(data, PLUGIN_REQUIRED_FIELDS, rel)


def validate_marketplace_manifest(path: Path, root: Path) -> list[Violation]:
    """Validate the marketplace manifest at path and return any violations."""
    data, blocking = _load_manifest(path, root)
    if data is None:
        return blocking
    rel = path.relative_to(root).as_posix()
    violations = _missing_fields(data, MARKETPLACE_REQUIRED_FIELDS, rel)
    if "plugins" not in data:
        return violations
    plugins = data["plugins"]
    if not isinstance(plugins, list) or not plugins:
        violations.append(Violation("manifest", rel, "plugins must be a non-empty array"))
        return violations
    for index, entry in enumerate(plugins):
        if not isinstance(entry, dict):
            violations.append(Violation("manifest", rel, f"plugins[{index}] must be an object"))
            continue
        violations.extend(
            Violation("manifest", rel, f"plugins[{index}] missing required field: {field}")
            for field in PLUGIN_ENTRY_REQUIRED_FIELDS
            if field not in entry
        )
    return violations


def run_all(root: Path) -> list[Violation]:
    """Run every check against root and return the combined violations."""
    plugin = root / ".claude-plugin" / "plugin.json"
    marketplace = root / ".claude-plugin" / "marketplace.json"
    violations: list[Violation] = []
    violations.extend(validate_plugin_manifest(plugin, root))
    violations.extend(validate_marketplace_manifest(marketplace, root))
    violations.extend(scan_links(root))
    violations.extend(scan_dashes(root))
    return violations


def _default_root() -> Path:
    """Return the repository root, inferred from this script's location."""
    return Path(__file__).resolve().parent.parent


def main(argv: Sequence[str] | None = None) -> int:
    """Validate the repository and return a process exit code."""
    parser = argparse.ArgumentParser(description="Validate the proven-python repository.")
    parser.add_argument(
        "--root",
        type=Path,
        default=_default_root(),
        help="Repository root to validate (defaults to this repository).",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    violations = run_all(root)
    if not violations:
        print("OK: manifests valid, links resolve, no em or en dashes.")
        return 0
    print(f"FAIL: {len(violations)} problem(s) found:")
    for violation in violations:
        print(f"  {violation.render()}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
