# Phiton Streamlining TODO for MVP (v1.0)

## Phase 1: Code Structure and Responsibility Clarification

- [ ] **Centralize Core Conversion Logic:**
    - [ ] Ensure `phitonize()` and `dephitonize()` in `src/phiton/__init__.py` are primary public API.
    - [ ] Refactor `phiton()` in `src/phiton/cli.py` to primarily handle CLI I/O and call API functions.
    - [ ] Consolidate logging for conversion process, controlled by `verbose` flag.
- [ ] **Refine Optimization Logic (`phitonize.py`, `utils.py`):**
    - [ ] Move all Phiton-string-based optimizations to `optimize_final` in `utils.py`.
    - [ ] Ensure `phitonize_node` in `phitonize.py` focuses on AST-to-Phiton symbol/structural mapping.
    - [ ] Review and clarify the roles/application order of `PATTERN_REPLACEMENTS`, `ADVANCED_PATTERNS`, and `COMMON_SUBEXPRESSIONS`.

## Phase 2: Simplification and MVP Focus for Core Logic

- [ ] **Simplify `phitonize_node` (`src/phiton/phitonize.py`):**
    - [ ] Review and simplify handling of less common/complex AST nodes for MVP robustness.
    - [ ] Prioritize common Python constructs.
- [ ] **Refine Dephitonization (`src/phiton/dephitonize.py`):**
    - [ ] Improve `_replace_symbols`, `_handle_literals`, `_reconstruct_blocks_and_lines`.
    - [ ] Focus on achieving syntactically valid Python output.
    - [ ] Use AST parsing warnings to guide dephitonization improvements.
- [ ] **Review and Prioritize Constants (`src/phiton/constants.py`):**
    - [ ] Verify `PYTHON_TO_PHITON` for unique and correct mappings.
    - [ ] Resolve symbol conflicts (e.g., `∀` for `all` vs. `for`).
    - [ ] Prioritize patterns in `PATTERN_REPLACEMENTS`, `ADVANCED_PATTERNS`, `COMMON_SUBEXPRESSIONS` that offer significant MVP value.

## Phase 3: CLI and Auxiliary Components

- [ ] **Streamline CLI (`src/phiton/cli.py`):**
    - [ ] Verify stdin/stdout operations.
    - [ ] Ensure clear help messages.
- [ ] **Review and Update Test Suite (`tests/`):**
    - [ ] Update tests failing due to refactoring.
    - [ ] Make `test_converter.py` tests more robust (e.g., check for symbol presence/absence rather than exact string matches for all levels).
    - [ ] Convert `tests/test_refactored.py` to an automated pytest test or remove if redundant.
- [ ] **Update Documentation and Auxiliary Files:**
    - [ ] Update `README.md` for any CLI changes.
    - [ ] Update `SPEC.md` to reflect MVP Phiton notation.
    - [ ] Iteratively update `CHANGELOG.md` with implemented changes.
    - [ ] Update `PROGRESS.md` to reflect streamlining progress.

## General Tasks (Throughout Implementation)

- [ ] Run `python -m pytest` frequently after changes.
- [ ] Manually verify core CLI operations.
