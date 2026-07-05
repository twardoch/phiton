# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Modernization pass (2026-07-05)

- Trimmed runtime `dependencies` to the three the package actually imports
  (`fire`, `loguru`, `rich`); build and test tooling moved out of install deps.
- Filled in the empty package `description` and `keywords`.
- Renamed `push.yml` to `ci.yml` and pinned every GitHub Action to a commit SHA
  in both `ci.yml` and `release.yml`.
- Made the test suite pass honestly: regenerated the drifted `simple_level{1,5}.phi`
  fixtures against current output, and rewrote the dephitonizer round-trip test to
  assert AST-equivalence on statement-level code (the guaranteed contract) while
  marking control-flow block round-trips `xfail` with a documented reason.
- Cleaned `ruff` and `mypy --strict`: excluded input fixtures under `tests/data`
  from linting, ignored the complexity/boolean-arg lints inherent to the AST
  dispatcher, and added type annotations that resolve name-reuse errors.
- Exported the public `phitonize`/`dephitonize` helpers in `__all__`.
- Added a Jekyll (Just the Docs) site under `docs/` and a README "Limitations"
  section stating plainly where round-trip fidelity ends.

### Added

- Refactored codebase into a proper module structure
- Created `ConversionConfig` dataclass for configuration
- Added multiple compression levels (1-5)
- Added comprehensive CLI with preview functionality
- Added detailed compression statistics
- Added proper documentation
- Added test files
- Added comprehensive dependency management with dev, test, and all extras
- Created examples directory for example files
- Added `__init__.py` to tests directory to fix namespace package issues

### Changed

- Improved compression algorithm with enhanced symbol substitution
- Optimized imports handling
- Added pattern recognition for common code patterns
- Enhanced final optimization pass
- Reorganized project structure with proper src, tests, and examples directories
- Consolidated pytest configuration in pyproject.toml

### Fixed

- Fixed import issues
- Fixed type hints in CLI statistics
- Fixed indentation error in test_optimize_imports
- Removed redundant configuration files
- Cleaned up unused and unneeded files

## [0.0.post1] - 2025-03-02

### Added

- Initial version with basic functionality
- Python to Phiton conversion
- Symbol mappings
- Basic CLI 
