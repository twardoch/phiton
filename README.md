# Phiton: Symbolic Python Code Compressor

Phiton is a unique tool that transforms standard Python code into a concise, symbolic notation and back. It leverages a rich set of Unicode characters to represent Python syntax, aiming to reduce code size and offer a different visual perspective on program structure.

## Table of Contents

1.  [What is Phiton?](#what-is-phiton)
2.  [Who is it For?](#who-is-it-for)
3.  [Why is it Useful?](#why-is-it-useful)
4.  [Installation](#installation)
5.  [Usage](#usage)
    *   [Command-Line Interface (CLI)](#command-line-interface-cli)
    *   [Programmatic Usage (Python API)](#programmatic-usage-python-api)
6.  [Technical Deep-Dive](#technical-deep-dive)
    *   [How Phiton Works](#how-phiton-works)
        *   [Python to Phiton (`phitonize`)](#python-to-phiton-phitonize)
        *   [Phiton to Python (`dephitonize`)](#phiton-to-python-dephitonize)
    *   [Core Modules](#core-modules)
    *   [Phiton Symbol Reference](#phiton-symbol-reference)
    *   [Compression Levels Explained](#compression-levels-explained)
    *   [Coding and Contributing](#coding-and-contributing)
        *   [Development Setup](#development-setup)
        *   [Running Tests](#running-tests)
        *   [Linting and Formatting](#linting-and-formatting)
        *   [Contribution Guidelines](#contribution-guidelines)
    *   [License](#license)

---

## What is Phiton?

Phiton is a bidirectional Python code compressor and decompressor. It takes your Python scripts (`.py`) and converts them into a highly condensed format (`.phi`) using a system of symbols inspired by mathematical and logical notation. This "Phitonized" code can then be converted back to standard Python, aiming for functional equivalence.

The core idea is to replace common Python keywords, operators, and even some standard library functions with single Unicode characters or short symbolic sequences. For example, `def` becomes `ƒ`, `return` becomes `⇐`, and `if` becomes `⋔`.

## Who is it For?

Phiton is designed for:

*   **Developers seeking extreme code conciseness:** Useful in environments where code size is a critical constraint.
*   **Enthusiasts of symbolic notation:** For those who appreciate or are curious about representing code in a more symbolic, mathematical-like language.
*   **Researchers in code representation:** Provides a platform for experimenting with alternative code syntaxes and compression techniques.
*   **Educational purposes:** Can be a novel way to explore Python syntax and semantics from a different angle.

## Why is it Useful?

*   **Code Size Reduction:** Significantly shrinks Python code, which can be beneficial for storage, transmission, or certain embedded applications.
*   **Alternative Code Perspective:** The symbolic notation can offer a different way to visualize and understand code structure and logic, potentially highlighting patterns not immediately obvious in standard Python.
*   **Exploration of Code Obfuscation (and De-obfuscation):** While not its primary goal, the transformation can act as a form of code obfuscation, with the tool itself being the key to de-obfuscation.
*   **Experimental & Fun:** It's an interesting experiment in programming language representation.

## Installation

You can install Phiton using `uv` or `pip`.

**Using uv:**

```bash
uv pip install phiton
```

**Using pip (legacy):**

```bash
pip install phiton
```

**Install from the GitHub repository:**

For the latest version directly from the repository:

```bash
uv pip install git+https://github.com/twardoch/phiton.git
```

Or with pip:

```bash
pip install git+https://github.com/twardoch/phiton.git
```

**For development:**

If you want to contribute to Phiton or work with the source code, clone the repository and install it in editable mode with development and testing dependencies:

```bash
git clone https://github.com/twardoch/phiton.git
cd phiton
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
# Install in editable mode
pip install -e ".[dev,test]"
```

## Usage

Phiton can be used both as a command-line tool and as a Python library.

### Command-Line Interface (CLI)

The CLI is invoked using `python -m phiton`. You can see all options with `python -m phiton -- --help`.

**Compress a Python file:**

```bash
python -m phiton example.py
```
This will create `example.phi` in the same directory if `--output-path` is not specified.

**Specify an output file or directory:**

```bash
python -m phiton example.py --output-path compressed_example.phi
python -m phiton my_project_dir/ --output-path compressed_project_dir/ # Processes files in directory
```

**Read from stdin and write to stdout:**

```bash
cat example.py | python -m phiton > example.phi
```

**Decompress a Phiton file:**

Use the `--decompress` or `-d` flag.
```bash
python -m phiton example.phi --decompress
```
To output to stdout:
```bash
cat example.phi | python -m phiton --decompress > example_decompressed.py
```

**Preview compression/decompression without saving:**

The output will be printed to the console.
```bash
python -m phiton example.py --preview
cat example.phi | python -m phiton --decompress --preview
```

**Adjust compression level (1-5, default is 5 for max compression):**

```bash
python -m phiton example.py --level 3
```

**Control preservation of comments and type hints (both default to `True`):**

```bash
python -m phiton example.py --comments=False --type-hints=False
```

**Control minification and symbol substitution (both default to `True`):**

```bash
python -m phiton example.py --minify=False --symbols=False
```

**Show version:**

```bash
python -m phiton version
```
Alternatively:
```bash
python -m phiton --version
```

**Key CLI Options:**

*   `input_path`: Path to the file or directory to process. Reads from stdin if not provided.
*   `--output-path` (or `-o`): Path to save the processed output. Writes to stdout if not provided.
*   `--decompress` (or `-d`): Boolean flag. If present, decompress Phiton to Python. Default is to compress.
*   `--level` (or `-l`): Integer (1-5). Compression level. Higher means more compression. Default: 5.
*   `--comments`: Boolean. `True` to preserve comments, `False` to remove. Default: `True`.
*   `--type-hints`: Boolean. `True` to preserve type hints, `False` to remove. Default: `True`.
*   `--minify`: Boolean. `True` to enable minification, `False` to disable. Default: `True`.
*   `--symbols`: Boolean. `True` to use symbol substitution, `False` to disable. Default: `True`.
*   `--preview`: Boolean flag. If present, print output to console instead of saving to file.
*   `--verbose` (or `-v`): Boolean flag. If present, print verbose processing information and statistics.
*   `version`: Subcommand to show Phiton version and exit. Can also use `--version`.

### Programmatic Usage (Python API)

You can use Phiton's compression and decompression capabilities directly in your Python code.

**Import necessary components:**

```python
from phiton import phitonize, dephitonize, ConversionConfig
```

**Basic compression:**

```python
source_code = """
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
"""

# Compress the code
# phitonize() returns a dictionary with 'result' (compressed code) and 'stats'
compression_output = phitonize(source_code)
phiton_code = compression_output["result"]
stats = compression_output["stats"]

print("Phiton Code:")
print(phiton_code)
print("\\nCompression Stats:")
print(stats)
```

**Basic decompression:**

```python
# Assuming phiton_code from the example above
decompression_output = dephitonize(phiton_code)
python_code_restored = decompression_output["result"]
stats_decomp = decompression_output["stats"]

print("\\nRestored Python Code:")
print(python_code_restored)
print("\\nDecompression Stats:")
print(stats_decomp)
```

**Using `ConversionConfig` for more control:**

The `ConversionConfig` dataclass allows you to customize the conversion process, similar to the CLI options.

```python
custom_config = ConversionConfig(
    level=3,             # Compression level (1-5)
    comments=False,      # Remove comments
    type_hints=False,    # Remove type hints
    minify=True,         # Enable minification (removes whitespace, etc.)
    symbols=True         # Enable symbol substitution
)

compressed_with_config = phitonize(source_code, config=custom_config)
print("\\nPhiton Code (Level 3, no comments/hints):")
print(compressed_with_config["result"])

# Decompression can also use a config, though its options are less impactful on the dephitonize process
decompressed_with_config = dephitonize(compressed_with_config["result"], config=custom_config)
print("\\nRestored Python Code (from Level 3):")
print(decompressed_with_config["result"])
```

The `phitonize()` and `dephitonize()` functions in `src/phiton/__init__.py` are the main public API entry points. They internally call `phitonize_python()` and `dephitonize_phiton()` respectively, which handle the core conversion logic.

---

## Technical Deep-Dive

This section provides a more detailed look into Phiton's internal workings, its symbolic language, and guidelines for development and contribution.

### How Phiton Works

Phiton's conversion process relies heavily on Python's Abstract Syntax Tree (AST) module for parsing and transforming code.

#### Python to Phiton (`phitonize`)

The `phitonize` process (primarily implemented in `src/phiton/phitonize.py` via the `phitonize_python` function) involves these key stages:

1.  **Parsing:** The input Python source code is first parsed into an AST using Python's `ast.parse()` function. If the code is syntactically invalid Python, this step will fail.
2.  **AST Traversal:** The AST is traversed node by node. For each node type (e.g., `ast.FunctionDef`, `ast.If`, `ast.BinOp`), specific logic determines its Phiton representation.
3.  **Symbol Substitution:** Python keywords, operators, and known function names are replaced with their corresponding Phiton Unicode symbols. These mappings are defined in `PYTHON_TO_PHITON` within `src/phiton/constants.py`. For example, `def` becomes `ƒ`, `return` becomes `⇐`, `==` becomes `≡`.
4.  **Literal Handling:**
    *   Numeric literals (integers, floats) are prefixed with `#` (e.g., `123` becomes `#123`).
    *   String literals are prefixed with `$` (e.g., `"text"` becomes `$text`). F-strings (`f"Hello {name}"`) are converted to `「Hello {name}」`.
    *   `None`, `True`, and `False` are converted to `∅`, `⊤`, and `⊥` respectively (at higher compression levels).
5.  **Block Structure:** Indented code blocks in Python are typically enclosed in `⟨...⟩` in Phiton. Multiple statements on a single logical line (if not part of a new block) are separated by `→`.
6.  **Domain-Specific Prefixes:** Common libraries can be represented by a prefix symbol (e.g., `numpy` as `№`, `pandas` as `℗`). These are defined in `DOMAIN_PREFIXES` in `src/phiton/constants.py`. Accessing attributes or methods uses a `·` (e.g., `numpy.array` might become `№·array`).
7.  **Pattern Replacements:**
    *   **Basic Patterns:** Common Python idioms (e.g., `if x is None:`) are replaced with shorter Phiton equivalents (e.g., `⋔x≡∅`). Defined in `PATTERN_REPLACEMENTS` in `src/phiton/constants.py`.
    *   **Advanced Patterns:** More complex or chained operations (e.g., `df.groupby(X).agg(Y)`) can be replaced by very concise Phiton forms (e.g., `§df·Γ(X)·A(Y)`). Defined in `ADVANCED_PATTERNS` in `src/phiton/constants.py`.
8.  **Configuration Application:** The `ConversionConfig` object (specifying `level`, `comments`, `type_hints`, `minify`, `symbols`) influences these steps. For example:
    *   `comments=False` will attempt to strip comments.
    *   `type_hints=False` will attempt to strip type hints.
    *   `symbols=False` would skip most symbolic replacements.
    *   `minify=True` enables various minification techniques.
9.  **Optimization Pass:** The `optimize_final` function in `src/phiton/utils.py` applies further compression techniques based on the specified `level`. This includes aggressive whitespace removal, combining operations, and replacing common subexpressions (from `COMMON_SUBEXPRESSIONS` in `constants.py`).

#### Phiton to Python (`dephitonize`)

The `dephitonize` process (primarily implemented in `src/phiton/dephitonize.py` via the `dephitonize_phiton` function) reverses the Phitonization:

1.  **Literal Reconstruction:** Phiton literal prefixes (`#`, `$`, `「...」`) are removed, and the values are converted back to Python's string or numeric representations.
2.  **Symbol Replacement:** Phiton symbols are mapped back to their Python keyword/operator equivalents using the `PHITON_TO_PYTHON` mapping (the reverse of `PYTHON_TO_PHITON`). Domain prefixes are also converted back.
3.  **Block and Line Reconstruction:** This is one of the most complex parts. The `_reconstruct_blocks_and_lines` helper function attempts to rebuild Python's indentation and statement structure from Phiton's `⟨...⟩` block markers and `→` statement separators. It also handles keywords like `else` and `elif` to correctly structure conditional blocks. Colons are added to block-initiating statements (like `if`, `def`, `class`, `for`, `while`).
4.  **Spacing and Formatting:** Various regex substitutions are applied to clean up spacing around operators, parentheses, and keywords to produce more idiomatic Python code.
5.  **AST Validation (Optional):** The decompressed code can be parsed by `ast.parse()` to check for syntactic validity. Warnings are logged if errors occur.

**Note:** While Phiton aims for perfect round-trip conversion (Python -> Phiton -> Python), the aggressive nature of some higher-level compressions and the complexities of Python syntax mean that 100% fidelity for all possible code is a challenging goal. Decompression is generally robust but can sometimes produce stylistically different (though functionally equivalent) Python, or struggle with highly esoteric Phiton inputs.

### Core Modules

*   `src/phiton/__init__.py`: Public API (`phitonize`, `dephitonize`, `ConversionConfig`).
*   `src/phiton/__main__.py`: Entry point for CLI.
*   `src/phiton/cli.py`: Implements the command-line interface using `fire`.
*   `src/phiton/config.py`: Defines `ConversionConfig` dataclass.
*   `src/phiton/constants.py`: Contains all symbol mappings, pattern replacements, and domain prefixes. **This is the heart of the Phiton language definition.**
*   `src/phiton/phitonize.py`: Core logic for Python to Phiton conversion.
*   `src/phiton/dephitonize.py`: Core logic for Phiton to Python conversion.
*   `src/phiton/utils.py`: Utility functions, including `optimize_final` for compression level logic and `calculate_stats`.

### Phiton Symbol Reference

The following table details some of the most common symbols used in Phiton. For a comprehensive list, refer to `src/phiton/constants.py`.

| Python         | Phiton | Description             | Category       |
|----------------|--------|-------------------------|----------------|
| `def`          | `ƒ`    | Function definition     | Definitions    |
| `class`        | `Σ`    | Class definition        | Definitions    |
| `lambda`       | `λ`    | Lambda function         | Definitions    |
| `async`        | `⊡`    | Async keyword           | Definitions    |
| `await`        | `⊡`    | Await keyword           | Definitions    |
| `return`       | `⇐`    | Return statement        | Control Flow   |
| `yield`        | `↥`    | Yield statement         | Control Flow   |
| `yield from`   | `↥⋮`   | Yield from              | Control Flow   |
| `if`           | `⋔`    | If statement            | Control Flow   |
| `else`         | `⋮`    | Else statement          | Control Flow   |
| `for`          | `∀`    | For loop                | Control Flow   |
| `while`        | `⟳`    | While loop              | Control Flow   |
| `break`        | `⊠`    | Break statement         | Control Flow   |
| `continue`     | `⋯`    | Continue statement      | Control Flow   |
| `pass`         | `⊘`    | Pass statement          | Control Flow   |
| `try`          | `⚟`    | Try statement           | Control Flow   |
| `except`       | `⋔`    | Except clause (similar to if) | Control Flow   |
| `raise`        | `↑`    | Raise exception         | Control Flow   |
| `assert`       | `⊪`    | Assert statement        | Control Flow   |
| `=`            | `≔`    | Assignment              | Operators      |
| `==`           | `≡`    | Equality                | Operators      |
| `!=`           | `≠`    | Inequality              | Operators      |
| `<`            | `<`    | Less than               | Operators      |
| `<=`           | `≤`    | Less than or equal      | Operators      |
| `>`            | `>`    | Greater than            | Operators      |
| `>=`           | `≥`    | Greater than or equal   | Operators      |
| `+`            | `+`    | Addition                | Operators      |
| `-`            | `-`    | Subtraction             | Operators      |
| `*`            | `*`    | Multiplication          | Operators      |
| `/`            | `/`    | Division                | Operators      |
| `in`           | `∈`    | Membership test         | Operators      |
| `not in`       | `∉`    | Negated membership test | Operators      |
| `is`           | `⁇`    | Identity test           | Operators      |
| `is not`       | `⁇¬`   | Negated identity test   | Operators      |
| `and`          | `∧`    | Logical AND             | Operators      |
| `or`           | `∨`    | Logical OR              | Operators      |
| `not`          | `¬`    | Logical NOT             | Operators      |
| `None`         | `∅`    | None value              | Special Values |
| `True`         | `⊤`    | True value              | Special Values |
| `False`        | `⊥`    | False value             | Special Values |
| `len()`        | `ℓ()`  | Length function         | Built-ins      |
| `range()`      | `ℜ()`  | Range function          | Built-ins      |
| `print()`      | `Π()`  | Print function          | Built-ins      |
| `enumerate()`  | `ℯ()`  | Enumerate function      | Built-ins      |
| `zip()`        | `ℤ()`  | Zip function            | Built-ins      |
| `sorted()`     | `ς()`  | Sorted function         | Built-ins      |
| `sum()`        | `∑()`  | Sum function            | Built-ins      |
| `map()`        | `∫()`  | Map function            | Built-ins      |
| `filter()`     | `φ()`  | Filter function         | Built-ins      |
| `.` (attribute)| `·`    | Attribute access        | Structure      |
| Indented Block | `⟨...⟩`| Code block enclosure    | Structure      |
| Statement Sep. | `→`    | Statement separator     | Structure      |
| Type Hint Sep. | `⦂`    | Type annotation colon   | Structure      |
| Numeric Literal| `#123` | e.g., `123`             | Literals       |
| String Literal | `$abc` | e.g., `"abc"`           | Literals       |
| F-String       | `「」` | e.g., `f"{var}"`        | Literals       |

**Domain Prefixes (Examples):**

| Python Lib | Phiton |
|------------|--------|
| `numpy`    | `№`    |
| `pandas`   | `℗`    |
| `os`       | `α`    |
| `math`     | `Δ`    |
| `json`     | `ξ`    |
| `re`       | `®`    |

### Compression Levels Explained

Phiton offers 5 compression levels, controlled by the `--level` CLI argument or the `level` parameter in `ConversionConfig`. These levels determine the aggressiveness of the `optimize_final` function in `src/phiton/utils.py` and other behaviors in the phitonization process:

*   **Level 1 (Basic):**
    *   Minimal symbol substitution.
    *   Preserves most of the original code structure and readability (relative to Phiton).
    *   Normalizes whitespace to single spaces.

*   **Level 2 (Moderate):**
    *   More symbol substitutions.
    *   Removes redundant whitespace more effectively.
    *   Combines simple operations (e.g., `→ →` becomes `→`).

*   **Level 3 (Standard):**
    *   Full symbol substitution as defined in `constants.py`.
    *   Replaces common subexpressions (e.g., `x + 1` might become `x⁺` if defined in `COMMON_SUBEXPRESSIONS`).
    *   Optimizes imports (this is a structural part of `phitonize_python` rather than `optimize_final`).
    *   Aims for a good balance between compression and the possibility of somewhat readable Phiton.

*   **Level 4 (High):**
    *   Aggressive whitespace removal (most spaces removed).
    *   More aggressive symbol renaming for internally generated symbols for frequent expressions (if this optimization is active).
    *   May remove some "optional" structural characters if deemed safe (e.g., some parentheses via `optimize_final`).

*   **Level 5 (Maximum - Default):**
    *   All optimizations from Level 4.
    *   Applies the most aggressive techniques to achieve the shortest possible Phiton representation. This includes removing all non-essential characters, using the shortest forms for common patterns (e.g., `≔∅` might become just `∅`), and combining repeated operational symbols, as handled by `optimize_final`.
    *   The primary goal is minimal size.

The `ConversionConfig` also has flags like `comments`, `type_hints`, `minify`, and `symbols` which interact with the level. For instance, even at level 5, if `symbols=False`, symbolic replacement won't occur. Typically, for higher compression, `minify` and `symbols` would be `True`.

### Coding and Contributing

We welcome contributions to Phiton! Here's how to get started:

#### Development Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/twardoch/phiton.git
    cd phiton
    ```
2.  Create and activate a virtual environment (Python 3.10+ recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
    ```
3.  Install dependencies, including development tools:
    ```bash
    pip install -e ".[dev,test]"
    ```
    This installs Phiton in editable mode and pulls in `pytest` for testing and `ruff` for linting/formatting.

#### Running Tests

Execute the test suite using `pytest`:

```bash
python -m pytest tests
```
Or for more detailed test execution including coverage, as configured in `pyproject.toml` (via hatch scripts):
```bash
python -m pytest --cov-report=term-missing --cov-config=pyproject.toml --cov=src/phiton --cov=tests tests
```

#### Linting and Formatting

We use `ruff` for linting and formatting.

*   **Check for issues:**
    ```bash
    ruff check .
    ```
*   **Format code:**
    ```bash
    ruff format .
    ```
*   **Fix issues automatically (where possible) and then format:**
    ```bash
    ruff check . --fix --unsafe-fixes
    ruff format .
    ```
Pre-commit hooks are configured in `.pre-commit-config.yaml` to automate these checks. It's recommended to install them: `pre-commit install`.

#### Contribution Guidelines

1.  **Familiarize Yourself:** Before contributing, please review the `SPEC.md` to understand the Phiton language design and the existing codebase, particularly `src/phiton/constants.py`, `src/phiton/phitonize.py`, and `src/phiton/dephitonize.py`.
2.  **Create an Issue:** For new features or significant changes, it's good practice to open an issue first to discuss the proposal.
3.  **Fork and Branch:** Fork the repository and create a new branch for your feature or bug fix (e.g., `feature/my-new-feature` or `fix/issue-123`).
4.  **Develop:** Write your code, ensuring it adheres to the existing style. Add tests for any new functionality or bug fixes. Ensure your code is well-commented where necessary.
5.  **Test and Lint:** Ensure all tests pass (`pytest`) and the code is free of linting errors (`ruff check .`).
6.  **Document:** Update `README.md` or other relevant documentation if your changes affect usage, functionality, or the Phiton specification.
7.  **Pull Request:** Submit a pull request to the `main` branch of the upstream Phiton repository. Provide a clear description of your changes, why they are needed, and link any relevant issues.

### License

Phiton is licensed under the MIT License. See the `LICENSE` file for more details.
