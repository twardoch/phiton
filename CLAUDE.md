# CLAUDE.md — phiton

Guidance for AI agents (and humans) working in this repository.

## What phiton is

A Python-to-Unicode code compressor. It parses Python with `ast`, maps each node
to a Phiton symbol (`def`→`ƒ`, `return`→`⇐`, `if`→`⋔`), and can decompress back.
The purpose is fitting more Python into an LLM context window — not lossless
archival. See `README.md` for the symbol table and levels.

## Source map (`this_file`)

- `src/phiton/__init__.py` — public API: `phitonize()` / `dephitonize()` (dict
  results with stats) and the lower-level `phitonize_python` / `dephitonize_phiton`.
- `src/phiton/phitonize.py` — `phitonize_python`: the AST-walking compressor. One
  large `phitonize_node` dispatch closure, one node type per `elif`.
- `src/phiton/dephitonize.py` — `dephitonize_phiton`: regex/heuristic decompressor.
  `_reconstruct_blocks_and_lines` rebuilds indentation from `⟨…⟩`/`→`.
- `src/phiton/constants.py` — all symbol maps (`PYTHON_TO_PHITON`, `DOMAIN_PREFIXES`,
  `PATTERN_REPLACEMENTS`, `ADVANCED_PATTERNS`, `COMMON_SUBEXPRESSIONS`).
- `src/phiton/utils.py` — `optimize_final` (level-specific compression) and stats.
- `src/phiton/config.py` — `ConversionConfig` dataclass (level, comments, etc.).
- `src/phiton/cli.py` — Fire CLI I/O wrapper.
- `tests/` — pytest suite. `tests/data/` holds Python *input fixtures* (excluded
  from ruff). `tests/data/expected/*.phi` are golden snapshots of current output.

## Load-bearing facts

- **Version is git-tag driven** via `hatch-vcs`; `src/phiton/__version__.py` and
  `VERSION.txt` are generated/ignored — never hand-edit or commit them.
- **Round-trip is only guaranteed for statement-level code** (assignments,
  expressions) at levels 1–2. Control-flow block round-trip is a known-lossy
  heuristic; see `test_dephitonizer.py` (xfail cases) and `TODO.md`.
- **Substitution in `COMMON_SUBEXPRESSIONS` is substring-based** and can corrupt
  identifiers at levels 3–5 (`print` contains `int`). Documented in `TODO.md`.

## Working here

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[test]"
python -m pytest tests/
python -m ruff check src/phiton tests && python -m ruff format --check src/phiton tests
python -m mypy src/phiton
```

Keep the compression engine surgical: it is an acknowledged MVP. Fix real bugs,
but do not rewrite the dispatcher or change the on-disk `.phi` format casually —
that is a semver-relevant change.
