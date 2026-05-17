# Phiton: A Python Compressor Using Unicode Symbols

## Origins (6 months ago)

Adam Twardoch, a typographer interested in Unicode and mathematical notation, created Phiton on March 2nd, 2025. The idea was simple: replace Python keywords with semantically meaningful Unicode symbols.

```python
# Ordinary Python:
def calculate_statistics(numbers: list[float]) -> dict[str, float]:
    if not numbers:
        return {"mean": 0.0, "median": 0.0, "std_dev": 0.0}
    return {"mean": sum(numbers) / len(numbers)}

# Phiton output:
ƒcalculate_statisticsnumbers⦂⟮List[float]⟯⦂⟮Dict[(str,float)]⟯⟨⋔¬numbers⟨⇐{$mean:#0.0}⟩→⇐{$mean:∑numbers/ℓnumbers}⟩
```

## Early Development

Adam worked alone initially, refining symbol mappings and handling AST parsing. Version numbers progressed quickly: `v1.0.0`, `v1.0.4 spec`, `v1.0.5`, `v1.0.6`.

Key symbol choices in `constants.py`:

```python
PYTHON_TO_PHITON = {
    "return": "⇐",
    "yield": "↥", 
    "while": "⟳",
    "for": "∀",
    "if": "⋔",
    "None": "∅",
    "True": "⊤",
    "False": "⊥",
}
```

These weren't arbitrary. `∅` for `None` represents the empty set. `∀` for `for` reflects "for all" in logic.

## First Refactor (6 months ago)

By late March, the codebase needed structure. The project moved to `src/phiton/` with these modules:

- `constants.py`: Symbol mappings
- `phitonize.py`: Python to Phiton conversion
- `cli.py`: Command-line interface
- `utils.py`: Helper functions

## Enhanced Features (6 months ago)

Spring brought new capabilities:
- Five compression levels
- CLI options for batch processing
- Directory handling

```bash
# Level 1: Minimal compression
python -m phiton example.py --level 1

# Level 5: Maximum compression
python -m phiton example.py --level 5
```

## Decompression Challenges

The main issue: Phiton could compress Python well but couldn't reliably decompress it back. The dephitonizer was incomplete and fragile.

## AI Collaboration Begins (9 weeks ago)

On June 23rd, 2025, `google-labs-jules[bot]` joined the project. Its first major contribution (PR #1) included:
- Code modernization
- Linting fixes
- A working dephitonizer
- Test repairs

The bot rewrote the dephitonizer with clear logic:

```python
def _reconstruct_blocks_and_lines(self, code: str) -> str:
    """Reconstruct Python block structure from Phiton."""
    # Convert block markers ⟨...⟩ to proper Python indentation
    # Handle statement separators → 
    # Add colons to block-initiating statements
    # Deal with else/elif properly
```

Unlike previous versions, this one documented its approach and limitations.

## Documentation Update (8 weeks ago)

PR #3 delivered a complete README rewrite with:
- Installation instructions (`uv` and `pip`)
- Working CLI examples
- Python API documentation
- AST parsing explanation
- Symbol reference table

The README expanded from basic description to comprehensive guide.

## Build System Implementation (5 weeks ago)

PR #4 added CI/CD with:
- Semantic versioning
- Multi-platform builds
- Automated releases

Commit history showed typical development cycle:
```
feat(ci): add multi-platform binary build workflows
chore: remove build artifacts
chore: add dist/ to .gitignore
```

## Final Architecture

```
src/phiton/
├── __init__.py      # Public API: phitonize() and dephitonize()
├── constants.py     # Unicode mappings
├── phitonize.py     # AST transformation
├── dephitonize.py   # Decompression logic
├── cli.py           # Command-line interface
├── config.py        # Configuration
└── utils.py         # Statistics and optimization
```

## Symbol Design

Phiton maps Python syntax to mathematical/logical symbols:

```python
# Control flow
"for" → "∀"     # "for all"
"while" → "⟳"   # Loop symbol
"if" → "⋔"      # Decision point
"return" → "⇐"  # Return arrow

# Logic operators
"and" → "∧"
"or" → "∨" 
"not" → "¬"

# Values
"None" → "∅"    # Empty set
"True" → "⊤"    # Truth value
"False" → "⊥"   # False value
```

## Collaboration Model

The project showed effective human-AI teamwork:
1. Human provides vision and domain expertise
2. AI handles implementation and documentation
3. Human reviews and directs development
4. Both iterate toward better solutions

## Current Features

Phiton now offers:
- Five compression levels
- Reliable decompression
- Support for classes, async/await, type hints
- File and directory processing
- Compression statistics

Example compression (53% size reduction):
```python
# Original (100 characters):
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Phiton Level 5 (47 characters):
ƒfactorial n⦂⟮int⟯⦂⟮int⟯⟨⋔n≤#1⟨⇐#1⟩→⇐n*factorial n-#1⟩
```

## Development Insights

This collaboration revealed strengths in both partners:
- AI excels at structured implementation and documentation
- Humans provide creative direction and meaningful design choices
- Combined effort produces more robust results than either alone

## Future Plans

As of August 2025, planned improvements include:
- Better pattern recognition
- Enhanced compression algorithms
- Expanded domain-specific prefixes

## Try It

```bash
pip install phiton

# Compress Python code:
python -m phiton your_script.py

# Decompress Phiton back to Python:
python -m phiton your_script.phi --decompress
```