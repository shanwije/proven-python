"""Tests for the repository validation script.

These build a small repository in a temporary directory for each case, so they touch no real
files and do not depend on the layout of this repo. Dash characters are written with escape
sequences so this test file itself stays free of em and en dashes.
"""

from __future__ import annotations

import json
from pathlib import Path

import validate_repo as vr

EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)


def _write(path: Path, text: str) -> None:
    """Write text to path, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _valid_plugin() -> str:
    """Return the JSON body of a valid plugin manifest."""
    return json.dumps({"name": "proven-python", "version": "0.1.0", "description": "A skill."})


def _valid_marketplace() -> str:
    """Return the JSON body of a valid marketplace manifest."""
    return json.dumps(
        {
            "name": "proven-python",
            "owner": {"name": "shanwije"},
            "plugins": [{"name": "proven-python", "source": "./"}],
        }
    )


def _make_repo(root: Path) -> None:
    """Build a minimal, fully valid repository under root."""
    _write(root / ".claude-plugin" / "plugin.json", _valid_plugin())
    _write(root / ".claude-plugin" / "marketplace.json", _valid_marketplace())
    _write(
        root / "skills" / "proven-python" / "SKILL.md",
        "# Skill\n\nSee `references/style.md` and `checklists/done.md`.\n",
    )
    _write(root / "skills" / "proven-python" / "references" / "style.md", "# Style\n")
    _write(root / "skills" / "proven-python" / "checklists" / "done.md", "# Done\n")


def _kinds(violations: list[vr.Violation]) -> set[str]:
    """Return the set of violation kinds present."""
    return {v.kind for v in violations}


def test_clean_repo_has_no_violations(tmp_path: Path) -> None:
    """A correctly formed repository produces no violations."""
    _make_repo(tmp_path)
    assert vr.run_all(tmp_path) == []


def test_em_dash_is_flagged(tmp_path: Path) -> None:
    """An em dash anywhere in a text file is a dash violation."""
    _make_repo(tmp_path)
    _write(tmp_path / "skills" / "proven-python" / "references" / "style.md", f"# Style{EM_DASH}\n")
    violations = vr.scan_dashes(tmp_path)
    assert any(v.kind == "dash" and "style.md" in v.path for v in violations)


def test_en_dash_is_flagged(tmp_path: Path) -> None:
    """An en dash anywhere in a text file is a dash violation."""
    _write(tmp_path / "notes.txt", f"a {EN_DASH} b\n")
    violations = vr.scan_dashes(tmp_path)
    assert [v.kind for v in violations] == ["dash"]
    assert violations[0].line == 1


def test_hyphen_is_not_a_dash(tmp_path: Path) -> None:
    """An ordinary hyphen does not trip the dash scan."""
    _write(tmp_path / "notes.txt", "pre-commit is fine\n")
    assert vr.scan_dashes(tmp_path) == []


def test_missing_link_target_is_flagged(tmp_path: Path) -> None:
    """A skill code-span path that does not resolve is a link violation."""
    _make_repo(tmp_path)
    (tmp_path / "skills" / "proven-python" / "references" / "style.md").unlink()
    violations = vr.scan_links(tmp_path)
    assert any(v.kind == "link" and "style.md" in v.detail for v in violations)


def test_markdown_link_resolution(tmp_path: Path) -> None:
    """A relative Markdown link is checked; present resolves, absent is flagged."""
    skill = tmp_path / "skills" / "proven-python"
    _write(skill / "SKILL.md", "# S\n\n[guide](./guide.md)\n")
    assert any(v.kind == "link" for v in vr.scan_links(tmp_path))
    _write(skill / "guide.md", "# G\n")
    assert vr.scan_links(tmp_path) == []


def test_external_and_anchor_links_are_ignored(tmp_path: Path) -> None:
    """Links with a scheme or a bare anchor are not resolved against the filesystem."""
    skill = tmp_path / "skills" / "proven-python"
    _write(skill / "SKILL.md", "# S\n\n[web](https://example.com) and [a](#section)\n")
    assert vr.scan_links(tmp_path) == []


def test_links_inside_fenced_block_are_ignored(tmp_path: Path) -> None:
    """Paths shown inside a fenced code block are illustrative, not links."""
    skill = tmp_path / "skills" / "proven-python"
    _write(skill / "SKILL.md", "# S\n\n```\nfoo/bar.md\n```\n")
    assert vr.scan_links(tmp_path) == []


def test_plugin_missing_field_is_flagged(tmp_path: Path) -> None:
    """A plugin manifest missing a required field is a manifest violation."""
    path = tmp_path / ".claude-plugin" / "plugin.json"
    _write(path, json.dumps({"name": "x", "description": "y"}))
    violations = vr.validate_plugin_manifest(path, tmp_path)
    assert any("version" in v.detail for v in violations)


def test_invalid_json_is_flagged(tmp_path: Path) -> None:
    """A manifest that is not valid JSON is a manifest violation."""
    path = tmp_path / ".claude-plugin" / "plugin.json"
    _write(path, "{not json")
    violations = vr.validate_plugin_manifest(path, tmp_path)
    assert violations and violations[0].kind == "manifest"


def test_missing_manifest_is_flagged(tmp_path: Path) -> None:
    """A manifest file that does not exist is a manifest violation."""
    path = tmp_path / ".claude-plugin" / "plugin.json"
    violations = vr.validate_plugin_manifest(path, tmp_path)
    assert any("missing" in v.detail for v in violations)


def test_marketplace_empty_plugins_is_flagged(tmp_path: Path) -> None:
    """A marketplace with an empty plugins array is a manifest violation."""
    path = tmp_path / ".claude-plugin" / "marketplace.json"
    _write(path, json.dumps({"name": "m", "owner": {"name": "o"}, "plugins": []}))
    violations = vr.validate_marketplace_manifest(path, tmp_path)
    assert any("non-empty" in v.detail for v in violations)


def test_marketplace_plugin_missing_source_is_flagged(tmp_path: Path) -> None:
    """A marketplace plugin entry without a source is a manifest violation."""
    path = tmp_path / ".claude-plugin" / "marketplace.json"
    _write(
        path,
        json.dumps({"name": "m", "owner": {"name": "o"}, "plugins": [{"name": "p"}]}),
    )
    violations = vr.validate_marketplace_manifest(path, tmp_path)
    assert any("source" in v.detail for v in violations)


def test_main_returns_zero_on_clean_repo(tmp_path: Path) -> None:
    """main exits 0 and says so when the repository is clean."""
    _make_repo(tmp_path)
    assert vr.main(["--root", str(tmp_path)]) == 0


def test_main_returns_one_on_violation(tmp_path: Path) -> None:
    """main exits 1 when any check fails."""
    _make_repo(tmp_path)
    _write(tmp_path / "bad.md", f"has {EM_DASH} dash\n")
    assert vr.main(["--root", str(tmp_path)]) == 1
