"""Run with: python3 .github/scripts/test_sync_changelog.py"""

from sync_changelog import REPO, convert

SAMPLE = """# Changelog

Intro, see [docs/RELEASING.md](docs/RELEASING.md).

## [Unreleased]

<!-- One line per change. -->

### Changed results

### Added

- Pin `xxhash<4`, needs lm-eval < 0.5 and {braces}.

### Fixed

## [0.3.0] - 2026-10-20

### Added

- First release.

```bash
echo {x} <y>
```

### Removed
"""

out = convert(SAMPLE)
assert out.startswith("---\ntitle: \"Changelog\"")
assert "# Changelog" not in out and "<!--" not in out
assert f"]({REPO}docs/RELEASING.md)" in out
assert "## Unreleased\n\n### Added" in out  # kept: it has an entry
assert "### Changed results" not in out and "### Fixed" not in out
assert "### Removed" not in out
assert "## 0.3.0 - 2026-10-20" in out
assert "`xxhash<4`, needs lm-eval &lt; 0.5 and \\{braces\\}." in out
assert "echo {x} <y>" in out  # fenced code untouched
print("ok")
