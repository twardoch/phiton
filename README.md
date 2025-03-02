# Phiton

Phiton is a Python code compressor that converts standard Python code into a more concise notation using mathematical symbols and advanced compression techniques.

## Features

- Convert Python code to a compressed symbolic notation
- Adjustable compression levels (1-5)
- Preserve comments and type hints (optional)
- Command-line interface with rich output
- Support for processing individual files or entire directories
- Detailed compression statistics

## Installation

```bash
pip install phiton
```

Or install directly from the repository:

```bash
pip install git+https://github.com/twardoch/phiton.git
```

## Usage

### Command Line

Compress a Python file:

```bash
python -m phiton compress example.py
```

Preview compression without saving:

```bash
python -m phiton compress example.py --preview
```

Compress with specific options:

```bash
python -m phiton compress example.py --level=3 --comments=False --type-hints=False
```

Compress an entire directory:

```bash
python -m phiton compress my_project/ --output-path=compressed/
```

Show version:

```bash
python -m phiton version
```

### Python API

```python
from phiton import compress_string, compress_file, ConversionConfig

# Basic usage
result = compress_string("def hello(name: str) -> str:\n    return f'Hello, {name}!'")
print(result["result"])  # Compressed code
print(result["stats"])   # Compression statistics

# With custom configuration
config = ConversionConfig(
    level=3,             # Compression level (1-5)
    comments=False,      # Don't preserve comments
    type_hints=True,     # Preserve type hints
    minify=True,         # Minify the code
    symbols=True,        # Use symbol substitution
)
result = compress_string("def hello(name: str) -> str:\n    return f'Hello, {name}!'", config)

# Compress a file
stats = compress_file("example.py", "example.phi", config)
```

## Compression Levels

Phiton offers 5 compression levels:

1. **Basic**: Minimal symbol substitution, preserves structure and readability
2. **Moderate**: More symbol substitutions while maintaining readability
3. **Standard**: Full symbol substitution with some structure preservation
4. **High**: Aggressive symbol substitution and minimal structure
5. **Maximum**: Highest compression with shortest possible representation

## Symbol Examples

| Python | Phiton | Description |
|--------|--------|-------------|
| `def`  | `ƒ`    | Function definition |
| `return` | `⇐`  | Return statement |
| `if`   | `⋔`    | Conditional |
| `for`  | `∀`    | For loop |
| `in`   | `∈`    | Membership test |
| `None` | `∅`    | None value |
| `True` | `⊤`    | True value |
| `False` | `⊥`   | False value |
| `and`  | `∧`    | Logical AND |
| `or`   | `∨`    | Logical OR |
| `not`  | `¬`    | Logical NOT |
| `==`   | `≡`    | Equality |
| `!=`   | `≠`    | Inequality |
| `<=`   | `≤`    | Less than or equal |
| `>=`   | `≥`    | Greater than or equal |
| `=`    | `≔`    | Assignment |

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 