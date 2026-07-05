# Phiton: symbolic Python code compressor

Phiton converts Python source code to a compact symbolic notation and back. It replaces keywords, operators, and common built-in calls with Unicode characters, shrinking code size while preserving structure.

```python
# Python
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Phiton (level 5)
ƒ factorial(n⦂int)→int⟨⋔n≤#1⟨⇐#1⟩→⇐n*factorial(n-#1)⟩
```

## Visual

![A bulky spotted python on the left compresses, via an arrow, into a single elegant thin curl on the right](docs/assets/icon.png)

## Who it's for

- Developers needing compact code for token-limited LLM context windows
- Anyone curious about alternative visual representations of Python syntax
- Researchers exploring code compression and representation

## Install

```bash
pip install phiton
# or
uv pip install phiton
```

## CLI usage

```bash
# Compress a file (creates example.phi)
python -m phiton example.py

# Decompress
python -m phiton example.phi --decompress

# Preview without writing
python -m phiton example.py --preview

# Set compression level (1=light, 5=maximum, default=5)
python -m phiton example.py --level 3

# Strip comments and type hints
python -m phiton example.py --comments=False --type-hints=False

# stdin/stdout pipeline
cat example.py | python -m phiton > example.phi
cat example.phi | python -m phiton --decompress > restored.py

# Process a directory
python -m phiton src/ --output-path compressed/
```

## Python API

```python
from phiton import phitonize, dephitonize, ConversionConfig

# Compress
out = phitonize(source_code)
print(out["result"])   # Phiton string
print(out["stats"])    # {"original_chars": ..., "compressed_chars": ..., "compression_ratio": ...}

# Decompress
out = dephitonize(phiton_code)
print(out["result"])   # Python string

# Custom settings
config = ConversionConfig(level=3, comments=False, type_hints=False)
out = phitonize(source_code, config=config)
```

## Symbol reference

| Python | Phiton | | Python | Phiton |
|--------|--------|-|--------|--------|
| `def` | `ƒ` | | `class` | `Σ` |
| `return` | `⇐` | | `yield` | `↥` |
| `if` | `⋔` | | `else` | `⋮` |
| `for` | `∀` | | `while` | `⟳` |
| `lambda` | `λ` | | `async/await` | `⊡` |
| `try` | `⚟` | | `raise` | `↑` |
| `assert` | `⊪` | | `pass` | `⊘` |
| `break` | `⊠` | | `continue` | `⋯` |
| `==` | `≡` | | `!=` | `≠` |
| `<=` | `≤` | | `>=` | `≥` |
| `and` | `∧` | | `or` | `∨` |
| `not` | `¬` | | `in` | `∈` |
| `None` | `∅` | | `True` | `⊤` |
| `False` | `⊥` | | `=` | `≔` |
| `len()` | `ℓ()` | | `range()` | `ℜ()` |
| `print()` | `Π()` | | `sum()` | `∑()` |
| `map()` | `∫()` | | `filter()` | `φ()` |
| block `{…}` | `⟨…⟩` | | statement sep | `→` |

**Library prefixes:** `numpy` → `№`, `pandas` → `℗`, `os` → `α`, `math` → `Δ`, `json` → `ξ`, `re` → `®`

## Compression levels

| Level | Description |
|-------|-------------|
| 1 | Minimal substitution, maximum readability |
| 2 | More symbols, redundant whitespace removed |
| 3 | Full symbol substitution, import optimisation |
| 4 | Aggressive whitespace removal, shorter forms |
| 5 | Maximum compression — all non-essential characters removed |

All flags (`--comments`, `--type-hints`, `--symbols`, `--minify`) work independently of level.

## How it works

**Python → Phiton** (`phitonize.py`):
1. Parse source with `ast.parse()`
2. Walk the AST; map each node type to its Phiton symbol
3. Replace common patterns (e.g. `if x is None` → `⋔x≡∅`)
4. Wrap indented blocks in `⟨…⟩`, separate statements with `→`
5. Apply level-specific `optimize_final()` pass

**Phiton → Python** (`dephitonize.py`):
1. Reconstruct literals (strip `#`, `$`, `「…」` prefixes)
2. Map Phiton symbols back to Python keywords
3. Rebuild indentation from `⟨…⟩` and `→`
4. Clean up spacing with regex passes

## Limitations

Phiton is a compression aid, not a lossless codec. Know the edges before you rely on it:

- **Statement-level round-trip is faithful.** Assignments and expressions compress and decompress back to AST-equivalent Python at every level. This is covered by tests.
- **Control-flow blocks do not yet round-trip cleanly.** Rebuilding indentation from `⟨…⟩`/`→` is a heuristic. `if`/`for`/`while`/`def` bodies can come back as invalid or subtly altered Python. Treat decompression of block-heavy code as a draft to review, not a drop-in restore. (Tracked in `TODO.md`.)
- **Substring substitution can bruise identifiers.** At levels 3–5 a name that contains a mapped token — `print` contains `int` — may be partially rewritten. Compression stays useful for LLM context; exact recovery is not guaranteed.
- **Comments are dropped** unless you keep `--comments` and stay at a low level.

The tool earns its keep in one direction: squeeze Python down so more of it fits in a context window. Round-tripping arbitrary programs byte-for-byte is out of scope for now.

## Configuration

```python
from phiton import ConversionConfig

config = ConversionConfig(
    level=5,          # 1–5, default 5
    comments=True,    # preserve comments
    type_hints=True,  # preserve type annotations
    minify=True,      # enable minification
    symbols=True,     # enable symbol substitution
)
```

## Development

```bash
git clone https://github.com/twardoch/phiton && cd phiton
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,test]"
python -m pytest tests/
ruff check . && ruff format .
```

## License

MIT. See `LICENSE`.
