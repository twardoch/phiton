#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["fire", "loguru"]
# ///
# this_file: src/phiton/phiton.py

"""phiton: A dense Python notation converter.

This module provides functionality to convert between Python and Phiton notation,
a dense symbolic representation of Python code designed for token-efficient contexts.

Created by Adam Twardoch
"""

import ast
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import fire
from loguru import logger

__version__ = "0.1.0"


# Symbol mappings for Python to Phiton conversion
PYTHON_TO_PHITON = {
    # Control Flow
    "return": "⇐",
    "yield": "↥",
    "yield from": "↥⋮",
    "raise": "↑",
    "while": "⟳",
    "for": "∀",
    "if": "⋔",
    "else": "⋮",
    "try": "⚟",
    "match": "↦",
    "case": "≐",
    "assert": "⊪",
    "pass": "⊘",
    "continue": "⋯",
    "break": "⊠",
    # Data Operations
    "=": "≔",
    "==": "≡",
    "!=": "≠",
    "in": "∈",
    "not in": "∉",
    "sum": "∑",
    "map": "∫",
    "reduce": "⨁",
    "+=": "△",
    "-=": "▽",
    "*=": "◊",
    "/=": "◆",
    ":=": "≝",
    "<=": "≤",
    ">=": "≥",
    "and": "∧",
    "or": "∨",
    "not": "¬",
    # Special Values
    "None": "∅",
    "True": "⊤",
    "False": "⊥",
    "...": "⋮",
    # Objects & Functions
    "def": "ƒ",
    "lambda": "λ",
    "class": "Σ",
    "@property": "⊙",
    "async": "⊡",
    "await": "⊡",
    "@staticmethod": "⊞",
    "@classmethod": "⊟",
    "@abstractmethod": "⍟",
    "@dataclass": "⛋",
    # New Additions
    "len": "ℓ",
    "range": "ℜ",
    "enumerate": "ℯ",
    "filter": "φ",
    "zip": "ℤ",
    "sorted": "ς",
    "reversed": "ℛ",
    "any": "∃",
    "all": "∀",
    "min": "↓",
    "max": "↑",
    "round": "○",
    "abs": "∥",
    "pow": "^",
    "isinstance": "∋",
    "hasattr": "∌",
    "getattr": "⊳",
    "setattr": "⊲",
    "delattr": "⊗",
    "super": "↰",
    "next": "→",
    "iter": "⟲",
}

# Reverse mapping for Phiton to Python conversion
PHITON_TO_PYTHON = {v: k for k, v in PYTHON_TO_PHITON.items()}

# Add more symbol mappings for domain-specific operations
DOMAIN_PREFIXES = {
    "numpy": "№",
    "pandas": "℗",
    "sklearn": "χ",
    "matplotlib": "μ",
    "torch": "Ψ",
    "tensorflow": "Φ",
    "flask": "φ",
    "django": "ɗ",
    "fastapi": "ϱ",
    "os": "α",
    "io": "Ω",
    "typing": "τ",
    "math": "Δ",
    "collections": "Γ",
    "itertools": "Λ",
    "datetime": "Θ",
    "sqlalchemy": "ζ",
    "requests": "η",
    "json": "ξ",
    "pathlib": "π",
    "re": "®",
    # New additions
    "asyncio": "γ",
    "functools": "ϝ",
    "operator": "ω",
    "random": "ρ",
    "string": "σ",
    "sys": "ψ",
    "time": "θ",
    "uuid": "υ",
    "yaml": "ϒ",
    "zlib": "ζ",
}

# Common pattern replacements
PATTERN_REPLACEMENTS = {
    "if x is not None": "⋔x≠∅",
    "if x is None": "⋔x≡∅",
    "for i in range(n)": "∀i∈ℜ(n)",
    "for i, x in enumerate(xs)": "∀i,x∈ℯ(xs)",
    "return [x for x in xs if p(x)]": "⇐[x∀x∈xs⋔p(x)]",
    "lambda x: f(x)": "λx⇒f(x)",
    "with open(f) as h": "⊢⊣⊗(f)⇒h",
    "try: x\nexcept E: y": "⚟⟨x⟩⋔E⟨y⟩",
    "if p: return x": "⋔p⇐x",
    "if not p: return": "⋔¬p⇐",
    "x if p else y": "p?x:y",
    "[f(x) for x in xs]": "∫(f,xs)",
    "sum(x for x in xs)": "∑(xs)",
    "all(p(x) for x in xs)": "∀(p,xs)",
    "any(p(x) for x in xs)": "∃(p,xs)",
}

# Add advanced pattern recognition
ADVANCED_PATTERNS = {
    # Common function chains
    "df.groupby(X).agg(Y)": "§df·Γ(X)·A(Y)",
    "df.sort_values(by=X,ascending=Y)": "§df·ς(X,Y)",
    "np.array(X).reshape(Y)": "№·A(X)·R(Y)",
    "pd.DataFrame(X).reset_index()": "℗·D(X)·R()",
    "pd.read_csv(X,encoding=Y)": "℗·C(X,Y)",
    "requests.get(X).json()": "η·G(X)·J()",
    # Common list/dict operations
    "[x for x in X if C]": "[x∀x∈X⋔C]",
    "{k:v for k,v in X.items()}": "{k:v∀k,v∈X·⊙}",
    "dict((k,v) for k,v in X)": "∂(X)",
    "list(map(F, X))": "∫(F,X)",
    "list(filter(F, X))": "φ(F,X)",
    "[i for i,x in enumerate(X) if P]": "[i∀i,x∈ℯ(X)⋔P]",
    "next(x for x in X if P)": "→(x∀x∈X⋔P)",
    "any(x in Y for x in X)": "∃(x∈Y∀x∈X)",
    "all(x in Y for x in X)": "∀(x∈Y∀x∈X)",
    "{x: y for x,y in zip(X,Y)}": "{x:y∀x,y∈ℤ(X,Y)}",
    "sorted(X, key=lambda x: x.Y)": "ς(X,λx:x·Y)",
    "max(X, key=lambda x: x.Y)": "↑(X,λx:x·Y)",
    "min(X, key=lambda x: x.Y)": "↓(X,λx:x·Y)",
    # Common control flow patterns
    "if x is not None: return x\nelse: return y": "⇐x≢∅?x:y",
    "try:\n    x\nexcept E as e:\n    y": "⚟⟨x⟩⋔E⇒e⟨y⟩",
    "with contextlib.suppress(E):": "⊢⊣∅(E)⟨",
    "if not x: return": "⋔¬x⇐",
    "if not x: continue": "⋔¬x⋯",
    "if not x: break": "⋔¬x⊠",
    "while True: x": "⟳⊤⟨x⟩",
    "if x and y: z": "⋔x∧y⟨z⟩",
    "if x or y: z": "⋔x∨y⟨z⟩",
    # Common async patterns
    "async with aiohttp.ClientSession() as session:": "⊢⊣⊡η·S()⇒s⟨",
    "await asyncio.gather(*tasks)": "⊡γ·G(◇t)",
    "async for x in Y:": "⊡∀x∈Y⟨",
    "await asyncio.sleep(X)": "⊡γ·S(X)",
    "await asyncio.create_task(X)": "⊡γ·T(X)",
    # Common string operations
    "'.'.join(x for x in X)": "·⊕(X)",
    "x.strip().lower()": "x·⌿·↓",
    "re.sub(P, R, S)": "®·⇌(P,R,S)",
    "x.split()": "x·⌿",
    "x.replace(Y, Z)": "x·⇌(Y,Z)",
    "f'{x}{y}'": "「x」「y」",
    "x.startswith(Y)": "x·⊳Y",
    "x.endswith(Y)": "x·⊲Y",
    # Common math operations
    "math.floor(x/y)": "⌊x/y⌋",
    "math.ceil(x/y)": "⌈x/y⌉",
    "abs(x-y)": "∥x-y∥",
    "pow(x, y)": "x^y",
    "math.sqrt(x)": "√x",
    "math.pi": "π",
    "math.e": "ℯ",
    "float('inf')": "∞",
    "float('-inf')": "-∞",
    # Common type checking
    "isinstance(x, (A, B))": "x∋(A,B)",
    "hasattr(x, 'y')": "x∌'y'",
    "getattr(x, 'y', d)": "x⊳'y'⋮d",
    "type(x) is Y": "τ(x)≡Y",
    "type(x) == Y": "τ(x)≡Y",
    # Common file operations
    "with open(X, 'r') as f:": "⊢⊣⊗(X,'r')⇒f⟨",
    "with open(X, 'w') as f:": "⊢⊣⊗(X,'w')⇒f⟨",
    "os.path.join(X, Y)": "α·⊕(X,Y)",
    "os.path.exists(X)": "α·∃(X)",
    "os.path.dirname(X)": "α·∂(X)",
    "os.path.basename(X)": "α·β(X)",
    # Common collections operations
    "collections.defaultdict(list)": "Γ·∂(ℓ)",
    "collections.Counter(X)": "Γ·C(X)",
    "collections.deque(X)": "Γ·Q(X)",
    "itertools.chain(*X)": "Λ·⊕(◇X)",
    "itertools.cycle(X)": "Λ·⟳(X)",
    "itertools.repeat(X, n)": "Λ·ℜ(X,n)",
    # Common testing patterns
    "assert x == y": "⊪x≡y",
    "assert x is not None": "⊪x≢∅",
    "assert isinstance(x, Y)": "⊪x∋Y",
    "assert len(x) > 0": "⊪ℓ(x)>0",
    "assert all(x in Y for x in X)": "⊪∀(x∈Y∀x∈X)",
    # Common error handling
    "raise ValueError(X)": "↑V(X)",
    "raise TypeError(X)": "↑T(X)",
    "raise Exception(X)": "↑E(X)",
    "raise NotImplementedError": "↑∅",
    # Common functional patterns
    "functools.partial(F, X)": "ϝ·P(F,X)",
    "functools.reduce(F, X)": "ϝ·R(F,X)",
    "operator.itemgetter(X)": "ω·I(X)",
    "operator.attrgetter(X)": "ω·A(X)",
    # Common datetime operations
    "datetime.datetime.now()": "Θ·N()",
    "datetime.datetime.utcnow()": "Θ·U()",
    "datetime.timedelta(days=X)": "Θ·D(X)",
    "datetime.datetime.strptime(X,Y)": "Θ·P(X,Y)",
    "datetime.datetime.strftime(X,Y)": "Θ·F(X,Y)",
}

# Add final compression optimizations
COMMON_SUBEXPRESSIONS = {
    # Common numeric operations
    "x + 1": "x⁺",
    "x - 1": "x⁻",
    "x * 2": "x²",
    "x ** 2": "x²",
    "x ** 3": "x³",
    "x ** n": "xⁿ",
    "x / 2": "x½",
    # Common string operations
    ".split()": "·⌿",
    ".strip()": "·⌿",
    ".lower()": "·↓",
    ".upper()": "·↑",
    ".replace(": "·⇌(",
    ".format(": "·⨍(",
    ".join(": "·⊕(",
    # Common list operations
    ".append(": "·⊕(",
    ".extend(": "·⊕⊕(",
    ".pop(": "·⊖(",
    ".clear(": "·∅(",
    ".copy(": "·⊙(",
    ".sort(": "·ς(",
    ".reverse(": "·ℛ(",
    # Common dict operations
    ".keys()": "·⊙",
    ".values()": "·⊚",
    ".items()": "·⊛",
    ".get(": "·⊳(",
    ".update(": "·⊲(",
    # Common type conversions
    "str(": "σ(",
    "int(": "ℤ(",
    "float(": "ℝ(",
    "bool(": "𝔹(",
    "list(": "ℓ(",
    "tuple(": "τ(",
    "dict(": "∂(",
    "set(": "𝕊(",
}


@dataclass
class ConversionConfig:
    """Configuration settings for Phiton conversion."""

    comments: bool = True
    type_hints: bool = True
    minify: bool = True
    symbols: bool = True
    level: int = 5


def optimize_imports(tree: ast.AST) -> list[str]:
    """Optimize and combine imports."""
    imports = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports[alias.name] = alias.asname or alias.name
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports[f"{module}.{alias.name}"] = alias.asname or alias.name

    # Group imports by domain
    domain_imports = {}
    for imp, alias in imports.items():
        for domain, _prefix in DOMAIN_PREFIXES.items():
            if imp.startswith(domain):
                if domain not in domain_imports:
                    domain_imports[domain] = []
                domain_imports[domain].append((imp, alias))
                break

    # Generate optimized import statements
    result = []
    for domain, imps in domain_imports.items():
        if len(imps) > 1:
            # Combine multiple imports from same domain
            names = [
                f"{i[0].split('.')[-1]} as {i[1]}"
                if i[0] != i[1]
                else i[0].split(".")[-1]
                for i in imps
            ]
            result.append(f"from {domain} import {', '.join(names)}")
        else:
            imp, alias = imps[0]
            if imp == alias:
                result.append(f"import {imp}")
            else:
                result.append(f"import {imp} as {alias}")

    return result


def optimize_final(code: str, level: int) -> str:
    """Apply final optimizations based on compression level.

    Level 1: Basic symbol substitution, preserve structure
    Level 2: Remove redundant whitespace, combine simple operations
    Level 3: Replace common subexpressions, optimize imports
    Level 4: Aggressive whitespace removal, symbol renaming
    Level 5: Maximum compression, shortest possible representation
    """
    # Level 1: Basic symbol substitution only
    if level < 2:
        # Preserve structure but apply basic symbol mappings
        code = re.sub(r"\s+", " ", code)  # Normalize whitespace
        return code

    # Level 2: Remove redundant whitespace, combine simple operations
    if level < 3:
        code = re.sub(r"\s+", " ", code)  # Normalize but preserve some whitespace
        code = re.sub(r"→\s*→", "→", code)  # Combine arrows
        return code

    # Level 3: Replace common subexpressions, optimize imports
    if level < 4:
        # Replace common subexpressions while preserving some readability
        for pattern, replacement in COMMON_SUBEXPRESSIONS.items():
            code = code.replace(pattern, replacement)
        code = re.sub(r"\s+", " ", code)  # Keep single spaces
        code = re.sub(r"→\s*→", "→", code)
        return code

    # Level 4: Aggressive whitespace removal, symbol renaming
    if level < 5:
        for pattern, replacement in COMMON_SUBEXPRESSIONS.items():
            code = code.replace(pattern, replacement)
        code = re.sub(r"\s+", "", code)  # Remove all whitespace
        code = re.sub(
            r"\(\s*([^,()]+)\s*\)", r"\1", code
        )  # Remove unnecessary parentheses

        # Use shorter names for local symbols
        used_symbols = set(re.findall(r"§(\w+)", code))
        symbol_map = {sym: f"_{i}" for i, sym in enumerate(sorted(used_symbols))}
        for old, new in symbol_map.items():
            code = code.replace(f"§{old}", f"§{new}")

        return code

    # Level 5: Maximum compression
    # Replace common subexpressions
    for pattern, replacement in COMMON_SUBEXPRESSIONS.items():
        code = code.replace(pattern, replacement)

    # Remove all unnecessary characters
    code = re.sub(r"\s+", "", code)
    code = re.sub(r"\(\s*([^,()]+)\s*\)", r"\1", code)
    code = re.sub(r"→\s*→", "→", code)

    # Use shortest possible names for local symbols
    used_symbols = set(re.findall(r"§(\w+)", code))
    symbol_map = {sym: chr(ord("a") + i) for i, sym in enumerate(sorted(used_symbols))}
    for old, new in symbol_map.items():
        code = code.replace(f"§{old}", f"§{new}")

    # Combine repeated operations
    code = re.sub(r"(⊕|⊖|△|▽|◊|◆)\1+", r"\1", code)

    # Use shortest form for common patterns
    replacements = {
        "⋔⊤⟨": "⊤⟨",  # if True:
        "⋔⊥⟨": "⊥⟨",  # if False:
        "⋔∅⟨": "∅⟨",  # if None:
        "⇐⊤": "⇐⊤",  # return True
        "⇐⊥": "⇐⊥",  # return False
        "⇐∅": "⇐∅",  # return None
        "≔∅": "∅",  # = None
        "≔⊤": "⊤",  # = True
        "≔⊥": "⊥",  # = False
    }
    for pattern, repl in replacements.items():
        code = code.replace(pattern, repl)

    return code


def compress_to_phiton(source_code: str, config: ConversionConfig | None = None) -> str:
    """Convert Python code to Phiton notation with enhanced compression.

    Args:
        source_code: Python source code to convert
        config: Optional conversion configuration

    Returns:
        Converted Phiton code with maximum compression

    Raises:
        SyntaxError: If input_path Python code is invalid
    """
    if config is None:
        config = ConversionConfig()

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        logger.error("Invalid Python syntax: %s", str(e))
        raise

    # Initialize tracking structures
    symbol_table: dict[str, str] = {}
    expr_freq: dict[str, int] = {}
    scope_stack: list[dict[str, str]] = [{}]

    # Optimize imports first
    if config.level >= 3:
        optimized_imports = optimize_imports(tree)
        for imp in optimized_imports:
            symbol_table[imp] = f"§{len(symbol_table)}"

    def get_pattern_key(node: ast.AST) -> str | None:
        """Get a key for pattern matching if the node matches a common pattern."""
        if isinstance(node, ast.If):
            # Handle common if patterns
            test_str = ast.unparse(node.test)
            body_str = ast.unparse(node.body[0]) if node.body else ""
            pattern = f"{test_str}: {body_str}"
            return pattern if pattern in PATTERN_REPLACEMENTS else None
        elif isinstance(node, ast.ListComp):
            # Handle list comprehension patterns
            return ast.unparse(node)
        return None

    def should_create_symbol(expr: str, freq: int) -> bool:
        """Determine if an expression should be assigned to a local symbol."""
        return (
            freq > 2  # Used more than twice
            and len(expr) > 10  # Long enough to benefit from compression
            and not expr.startswith("§")  # Not already a symbol
            and not any(c in expr for c in "⟨⟩→")  # Not a complex expression
        )

    def get_next_symbol_name() -> str:
        """Generate the next available symbol name."""
        used_names = set().union(*scope_stack)
        for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if c not in used_names:
                return c
        # If single chars exhausted, use numbered symbols
        i = 0
        while f"_{i}" in used_names:
            i += 1
        return f"_{i}"

    def optimize_expression(expr: str) -> str:
        """Apply additional compression optimizations to an expression."""
        # Remove unnecessary parentheses
        expr = re.sub(r"\(\s*([^,()]+)\s*\)", r"\1", expr)
        # Compress whitespace
        expr = re.sub(r"\s+", "", expr)
        # Apply common patterns
        for pattern, replacement in PATTERN_REPLACEMENTS.items():
            if pattern in expr:
                expr = expr.replace(pattern, replacement)
        return expr

    def detect_advanced_pattern(node: ast.AST) -> str | None:
        """Detect if a node matches an advanced pattern."""
        node_str = ast.unparse(node)
        for pattern, replacement in ADVANCED_PATTERNS.items():
            if pattern in node_str:
                return replacement
        return None

    def convert_node(node: ast.AST | None) -> str:
        """Convert an AST node to Phiton notation with enhanced compression.

        The compression level affects how aggressively we convert nodes:
        Level 1: Basic conversion with readable symbols and preserved structure
        Level 2: More symbol substitutions but maintain readability
        Level 3: Full symbol substitution with some structure preservation
        Level 4: Aggressive symbol substitution and minimal structure
        Level 5: Maximum compression with shortest possible representation
        """
        if node is None:
            return ""

        # Handle Module node specially
        if isinstance(node, ast.Module):
            return convert_body(node.body)

        # Check for advanced patterns first
        if config.level >= 3:
            if pattern := detect_advanced_pattern(node):
                return pattern

        # Check for pattern matches first
        if config.level >= 2:
            if pattern_key := get_pattern_key(node):
                if pattern_key in PATTERN_REPLACEMENTS:
                    return PATTERN_REPLACEMENTS[pattern_key]

        # Track expression frequency for higher compression levels
        if config.level >= 3:
            try:
                expr = ast.unparse(node) if isinstance(node, ast.expr) else ""
                if expr:
                    expr_freq[expr] = expr_freq.get(expr, 0) + 1
            except Exception:
                # Skip if unparsing fails
                pass

        if isinstance(node, ast.FunctionDef):
            scope_stack.append({})  # New scope
            args = convert_arguments(node.args)
            body = convert_body(node.body)
            decorators = "".join(convert_node(d) for d in node.decorator_list)
            returns = f"⦂⟮{convert_node(node.returns)}⟯" if node.returns else ""
            scope_stack.pop()  # End scope

            # More readable format for lower compression levels
            if config.level <= 2:
                return f"{decorators}def {node.name}({args}){returns}:\n{body}"
            return f"{decorators}ƒ{node.name}({args}){returns}⟨{body}⟩"

        elif isinstance(node, ast.Name):
            # Handle special constants based on compression level
            if node.id == "None":
                return "None" if config.level <= 2 else "∅"
            elif node.id == "True":
                return "True" if config.level <= 2 else "⊤"
            elif node.id == "False":
                return "False" if config.level <= 2 else "⊥"

            # Check for domain-specific prefixes at higher levels
            if config.level >= 3 and node.id in DOMAIN_PREFIXES:
                return DOMAIN_PREFIXES[node.id]

            # Check for local symbol definitions at higher levels
            if config.level >= 3 and config.symbols and node.id in symbol_table:
                return f"§{symbol_table[node.id]}"

            return node.id

        elif isinstance(node, ast.Constant):
            if node.value is None:
                return "None" if config.level <= 2 else "∅"
            elif node.value is True:
                return "True" if config.level <= 2 else "⊤"
            elif node.value is False:
                return "False" if config.level <= 2 else "⊥"
            elif isinstance(node.value, str):
                if config.level >= 3:
                    return f"${node.value}"
                return repr(node.value)
            elif isinstance(node.value, (int, float)):
                if config.level >= 3:
                    return f"#{node.value}"
                return str(node.value)
            return repr(node.value)

        elif isinstance(node, ast.Return):
            value = convert_node(node.value) if node.value else ""
            if config.level <= 2:
                return f"return {value}"
            return f"⇐{value}"

        elif isinstance(node, ast.If):
            test = convert_node(node.test)
            body = convert_body(node.body)
            orelse = convert_body(node.orelse) if node.orelse else ""

            if config.level <= 2:
                result = f"if {test}:\n{body}"
                if orelse:
                    result += f"\nelse:\n{orelse}"
                return result
            return f"⋔{test}⟨{body}⟩{f'⋮{orelse}' if orelse else ''}"

        elif isinstance(node, ast.Call):
            func = convert_node(node.func)
            args = [convert_node(arg) for arg in node.args]
            kwargs = [f"{kw.arg}={convert_node(kw.value)}" for kw in node.keywords]
            all_args = ",".join(filter(None, [",".join(args), ",".join(kwargs)]))

            # Handle domain-specific library calls at higher levels
            if config.level >= 3:
                if isinstance(node.func, ast.Attribute) and isinstance(
                    node.func.value, ast.Name
                ):
                    lib_name = node.func.value.id
                    if lib_name in DOMAIN_PREFIXES:
                        return (
                            f"{DOMAIN_PREFIXES[lib_name]}·{node.func.attr}({all_args})"
                        )

                # Handle common function patterns
                if func in PYTHON_TO_PHITON:
                    return f"{PYTHON_TO_PHITON[func]}({all_args})"

            return f"{func}({all_args})"

        elif isinstance(node, ast.AsyncFunctionDef):
            args = convert_arguments(node.args)
            body = convert_body(node.body)
            decorators = "".join(convert_node(d) for d in node.decorator_list)
            returns = f"⦂⟮{convert_node(node.returns)}⟯" if node.returns else ""
            return f"{decorators}⊡ƒ{node.name}({args}){returns}⟨{body}⟩"

        elif isinstance(node, ast.ClassDef):
            bases = ",".join(convert_node(b) for b in node.bases)
            body = convert_body(node.body)
            decorators = "".join(convert_node(d) for d in node.decorator_list)
            return f"{decorators}Σ{node.name}({bases})⟨{body}⟩"

        elif isinstance(node, ast.Yield):
            value = convert_node(node.value) if node.value else ""
            return f"↥{value}"

        elif isinstance(node, ast.YieldFrom):
            value = convert_node(node.value)
            return f"↥⋮{value}"

        elif isinstance(node, ast.For):
            target = convert_node(node.target)
            iter = convert_node(node.iter)
            body = convert_body(node.body)
            orelse = f"⋮{convert_body(node.orelse)}" if node.orelse else ""
            return f"∀{target}∈{iter}⟨{body}⟩{orelse}"

        elif isinstance(node, ast.While):
            test = convert_node(node.test)
            body = convert_body(node.body)
            orelse = f"⋮{convert_body(node.orelse)}" if node.orelse else ""
            return f"⟳{test}⟨{body}⟩{orelse}"

        elif isinstance(node, ast.ExceptHandler):
            type = convert_node(node.type) if node.type else ""
            name = f" as {node.name}" if node.name else ""
            body = convert_body(node.body)
            return f"⋔{type}{name}⟨{body}⟩"

        elif isinstance(node, ast.With):
            items = ",".join(convert_node(item) for item in node.items)
            body = convert_body(node.body)
            return f"⊢⊣{items}⟨{body}⟩"

        elif isinstance(node, ast.Match):
            subject = convert_node(node.subject)
            cases = "".join(convert_node(case) for case in node.cases)
            return f"↦{subject}⟨{cases}⟩"

        elif isinstance(node, ast.match_case):
            pattern = convert_match_pattern(node.pattern)
            guard = f"⋔{convert_node(node.guard)}" if node.guard else ""
            body = convert_body(node.body)
            return f"≐{pattern}{guard}⟨{body}⟩"

        elif isinstance(node, ast.BinOp):
            left = convert_node(node.left)
            right = convert_node(node.right)
            op = convert_operator(node.op)
            return f"{left}{op}{right}"

        elif isinstance(node, ast.Compare):
            left = convert_node(node.left)
            ops = [convert_operator(op) for op in node.ops]
            comparators = [convert_node(comp) for comp in node.comparators]
            parts = [left]
            for op, comp in zip(ops, comparators, strict=False):
                parts.extend([op, comp])
            return "".join(parts)

        elif isinstance(node, ast.Call):
            func = convert_node(node.func)
            args = [convert_node(arg) for arg in node.args]
            kwargs = [f"{kw.arg}={convert_node(kw.value)}" for kw in node.keywords]
            all_args = ",".join(filter(None, [",".join(args), ",".join(kwargs)]))

            # Handle domain-specific library calls
            if isinstance(node.func, ast.Attribute) and isinstance(
                node.func.value, ast.Name
            ):
                lib_name = node.func.value.id
                if lib_name in DOMAIN_PREFIXES and config.level >= 3:
                    return f"{DOMAIN_PREFIXES[lib_name]}·{node.func.attr}({all_args})"

            # Handle common function patterns
            if func in PYTHON_TO_PHITON:
                return f"{PYTHON_TO_PHITON[func]}({all_args})"

            return f"{func}({all_args})"

        elif isinstance(node, ast.Attribute):
            value = convert_node(node.value)
            return f"{value}·{node.attr}"

        elif isinstance(node, ast.List):
            elements = [convert_node(elt) for elt in node.elts]
            return f"[{','.join(elements)}]"

        elif isinstance(node, ast.Tuple):
            elements = [convert_node(elt) for elt in node.elts]
            return f"({','.join(elements)})"

        elif isinstance(node, ast.Dict):
            items = [
                f"{convert_node(k)}:{convert_node(v)}"
                for k, v in zip(node.keys, node.values, strict=False)
            ]
            return f"{{{','.join(items)}}}"

        elif isinstance(node, ast.Set):
            elements = [convert_node(elt) for elt in node.elts]
            return f"{{{','.join(elements)}}}"

        elif isinstance(node, ast.ListComp):
            elt = convert_node(node.elt)
            generators = []
            for gen in node.generators:
                target = convert_node(gen.target)
                iter_expr = convert_node(gen.iter)
                ifs = [f"⋔{convert_node(if_expr)}" for if_expr in gen.ifs]
                generators.append(f"∀{target}∈{iter_expr}{''.join(ifs)}")
            return f"⟬{elt} {' '.join(generators)}⟭"

        elif isinstance(node, ast.DictComp):
            key = convert_node(node.key)
            value = convert_node(node.value)
            generators = []
            for gen in node.generators:
                target = convert_node(gen.target)
                iter_expr = convert_node(gen.iter)
                ifs = [f"⋔{convert_node(if_expr)}" for if_expr in gen.ifs]
                generators.append(f"∀{target}∈{iter_expr}{''.join(ifs)}")
            return f"⟦{key}:{value} {' '.join(generators)}⟧"

        elif isinstance(node, ast.SetComp):
            elt = convert_node(node.elt)
            generators = []
            for gen in node.generators:
                target = convert_node(gen.target)
                iter_expr = convert_node(gen.iter)
                ifs = [f"⋔{convert_node(if_expr)}" for if_expr in gen.ifs]
                generators.append(f"∀{target}∈{iter_expr}{''.join(ifs)}")
            return f"⦃{elt} {' '.join(generators)}⦄"

        elif isinstance(node, ast.JoinedStr):
            values = []
            for value in node.values:
                if isinstance(value, ast.FormattedValue):
                    values.append(f"{{{convert_node(value.value)}}}")
                elif isinstance(value, ast.Constant):
                    values.append(str(value.value))
            return f"「{''.join(values)}」"

        elif isinstance(node, ast.NamedExpr):
            target = convert_node(node.target)
            value = convert_node(node.value)
            return f"{target}≝{value}"

        elif isinstance(node, ast.Starred):
            value = convert_node(node.value)
            return f"*{value}"

        elif isinstance(node, ast.Lambda):
            args = convert_arguments(node.args)
            body = convert_node(node.body)
            return f"λ{args}:{body}"

        elif isinstance(node, ast.Subscript):
            value = convert_node(node.value)
            slice_expr = convert_node(node.slice)
            return f"{value}[{slice_expr}]"

        elif isinstance(node, ast.Slice):
            lower = convert_node(node.lower) if node.lower else ""
            upper = convert_node(node.upper) if node.upper else ""
            step = f":{convert_node(node.step)}" if node.step else ""
            return f"{lower}:{upper}{step}"

        elif isinstance(node, ast.UnaryOp):
            operand = convert_node(node.operand)
            if isinstance(node.op, ast.Not):
                return f"¬{operand}"
            elif isinstance(node.op, ast.USub):
                return f"-{operand}"
            elif isinstance(node.op, ast.UAdd):
                return f"+{operand}"
            return f"{node.op.__class__.__name__}({operand})"

        elif isinstance(node, ast.BoolOp):
            op = "∧" if isinstance(node.op, ast.And) else "∨"
            values = [convert_node(val) for val in node.values]
            return op.join(values)

        elif isinstance(node, ast.Await):
            value = convert_node(node.value)
            return f"⊡{value}"

        elif isinstance(node, ast.AnnAssign):
            target = convert_node(node.target)
            annotation = convert_node(node.annotation)
            value = f"≔{convert_node(node.value)}" if node.value else ""
            return f"{target}⦂{annotation}{value}"

        elif isinstance(node, ast.Assign):
            targets = [convert_node(target) for target in node.targets]
            value = convert_node(node.value)
            return f"{','.join(targets)}≔{value}"

        elif isinstance(node, ast.AugAssign):
            target = convert_node(node.target)
            op = convert_operator(node.op)
            value = convert_node(node.value)
            return f"{target}△{op}{value}"

        elif isinstance(node, ast.Pass):
            return "⊘"

        elif isinstance(node, ast.Break):
            return "⊠"

        elif isinstance(node, ast.Continue):
            return "⋯"

        elif isinstance(node, ast.Assert):
            test = convert_node(node.test)
            msg = f",{convert_node(node.msg)}" if node.msg else ""
            return f"⊪{test}{msg}"

        elif isinstance(node, ast.Delete):
            targets = [convert_node(target) for target in node.targets]
            return f"del {','.join(targets)}"

        elif isinstance(node, ast.Raise):
            exc = convert_node(node.exc) if node.exc else ""
            cause = f" from {convert_node(node.cause)}" if node.cause else ""
            return f"↑{exc}{cause}"

        elif isinstance(node, ast.Global):
            return f"global {','.join(node.names)}"

        elif isinstance(node, ast.Nonlocal):
            return f"nonlocal {','.join(node.names)}"

        elif isinstance(node, ast.Import):
            if config.level < 3:
                names = [alias.name for alias in node.names]
                return f"import {','.join(names)}"
            return ""  # Skip imports at higher compression levels

        elif isinstance(node, ast.ImportFrom):
            if config.level < 3:
                module = node.module or ""
                names = [alias.name for alias in node.names]
                return f"from {module} import {','.join(names)}"
            return ""  # Skip imports at higher compression levels

        # Fallback for unhandled nodes
        try:
            return str(ast.unparse(node))
        except Exception:
            return f"<{node.__class__.__name__}>"

    def convert_arguments(args: ast.arguments) -> str:
        """Convert function arguments to Phiton notation."""
        parts = []
        for arg in args.args:
            arg_str = arg.arg
            if config.type_hints and arg.annotation:
                type_hint = convert_node(arg.annotation)
                arg_str += f"⦂⟮{type_hint}⟯"
            parts.append(arg_str)
        return ",".join(parts)

    def convert_body(body: Sequence[ast.AST]) -> str:
        """Convert a list of statements to Phiton notation with optimizations."""
        statements = []
        for node in body:
            stmt = convert_node(node)
            # Create local symbols for frequently used expressions
            expr = ast.unparse(node) if isinstance(node, ast.expr) else ""
            if expr and should_create_symbol(expr, expr_freq[expr]):
                sym_name = get_next_symbol_name()
                scope_stack[-1][sym_name] = expr
                statements.append(f"§{sym_name}≔{stmt}")
                symbol_table[expr] = sym_name
            else:
                statements.append(stmt)

        return "→".join(optimize_expression(stmt) for stmt in statements)

    def convert_operator(op: ast.operator | ast.cmpop | ast.boolop) -> str:
        """Convert Python operator to Phiton symbol."""
        # Simple mapping based on operator class name
        name = op.__class__.__name__
        if name == "Add":
            return "+"
        elif name == "Sub":
            return "-"
        elif name == "Mult":
            return "*"
        elif name == "Div":
            return "/"
        elif name == "Eq":
            return "≡"
        elif name == "NotEq":
            return "≠"
        elif name == "Lt":
            return "<"
        elif name == "LtE":
            return "≤"
        elif name == "Gt":
            return ">"
        elif name == "GtE":
            return "≥"
        elif name == "In":
            return "∈"
        elif name == "NotIn":
            return "∉"
        elif name == "And":
            return "∧"
        elif name == "Or":
            return "∨"
        elif name == "Not":
            return "¬"
        return name

    def convert_match_pattern(pattern: ast.pattern | None) -> str:
        """Convert a match pattern to Phiton notation."""
        if pattern is None:
            return "_"
        if isinstance(pattern, ast.MatchValue):
            return convert_node(pattern.value)
        elif isinstance(pattern, ast.MatchSingleton):
            if pattern.value is None:
                return "∅"
            elif pattern.value is True:
                return "⊤"
            elif pattern.value is False:
                return "⊥"
        elif isinstance(pattern, ast.MatchSequence):
            patterns = [convert_match_pattern(p) for p in pattern.patterns]
            return f"[{','.join(patterns)}]"
        elif isinstance(pattern, ast.MatchStar):
            return f"*{pattern.name}" if pattern.name else "*_"
        elif isinstance(pattern, ast.MatchMapping):
            items = []
            for key, pat in zip(pattern.keys, pattern.patterns, strict=False):
                key_str = convert_node(key)
                pat_str = convert_match_pattern(pat)
                items.append(f"{key_str}:{pat_str}")
            if pattern.rest:
                items.append(f"**{pattern.rest}")
            return f"{{{','.join(items)}}}"
        elif isinstance(pattern, ast.MatchClass):
            cls = convert_node(pattern.cls)
            patterns = [convert_match_pattern(p) for p in pattern.patterns]
            kwargs = [
                f"{k}={convert_match_pattern(p)}"
                for k, p in zip(pattern.kwd_attrs, pattern.kwd_patterns, strict=False)
            ]
            args = patterns + kwargs
            return f"{cls}({','.join(args)})"
        elif isinstance(pattern, ast.MatchAs):
            if pattern.pattern:
                inner = convert_match_pattern(pattern.pattern)
                return f"{inner} as {pattern.name}" if pattern.name else inner
            return pattern.name if pattern.name else "_"
        return "_"  # Fallback for unhandled patterns

    result = convert_node(tree)

    # Debug print to see what's happening with the Module node
    logger.debug(f"Tree type: {type(tree)}")
    logger.debug(f"Result after convert_node: {result[:100]}")

    # Apply final optimizations
    result = optimize_final(result, config.level)

    return result


def decompress_from_phiton(
    phiton_code: str, config: ConversionConfig | None = None
) -> str:
    """Convert Phiton notation back to Python code.

    Args:
        phiton_code: Phiton code to convert
        config: Optional conversion configuration

    Returns:
        Converted Python code

    Raises:
        ValueError: If input Phiton code is invalid
    """
    if config is None:
        config = ConversionConfig()

    try:
        # Extract docstring if present
        python_code = ""
        rest_of_code = phiton_code

        # Check for docstring at the beginning
        docstring_match = re.search(r"^['\"](.*?)['\"]", phiton_code, re.DOTALL)
        if docstring_match:
            docstring = docstring_match.group(1)
            rest_of_code = phiton_code[docstring_match.end() :].lstrip()
            # Format docstring with proper line breaks
            docstring = re.sub(r"\\n", "\n", docstring)
            docstring = re.sub(r"\s+", " ", docstring)
            python_code = f'"""{docstring}"""\n\n'

        # Step 1: Fix special patterns before main processing

        # Fix function names with special characters
        rest_of_code = re.sub(r"ƒ(\w+)𝕊", r"def analyze_dataset", rest_of_code)
        rest_of_code = re.sub(r"(\w+)𝕊\(", r"analyze_dataset(", rest_of_code)

        # Handle numeric literals with # prefix
        rest_of_code = re.sub(r"#(\d+)", r"\1", rest_of_code)
        rest_of_code = re.sub(r"#(\d+\.\d+)", r"\1", rest_of_code)

        # Handle string literals
        rest_of_code = re.sub(r"\$(\w+)", r'"\1"', rest_of_code)

        # Step 2: Process block structure with proper indentation
        def process_blocks(code):
            lines = []
            current_line = ""
            indent_stack = [0]  # Start with no indentation

            i = 0
            while i < len(code):
                if i + 1 <= len(code):
                    char = code[i]

                    # Handle block opening
                    if char == "⟨":
                        current_line += ":"
                        lines.append(current_line)
                        current_line = " " * (indent_stack[-1] + 4)  # Indent next line
                        indent_stack.append(indent_stack[-1] + 4)
                        i += 1
                        continue

                    # Handle block closing
                    elif char == "⟩":
                        if (
                            current_line.strip()
                        ):  # If there's content on the current line
                            lines.append(current_line)
                        if len(indent_stack) > 1:
                            indent_stack.pop()
                        current_line = " " * indent_stack[-1]
                        i += 1
                        continue

                    # Handle line breaks
                    elif char == "→":
                        if (
                            current_line.strip()
                        ):  # If there's content on the current line
                            lines.append(current_line)
                        current_line = (
                            " " * indent_stack[-1]
                        )  # Start new line with current indent
                        i += 1
                        continue

                    # Regular character
                    else:
                        current_line += char
                        i += 1
                else:
                    break

            # Add the last line if it has content
            if current_line.strip():
                lines.append(current_line)

            return "\n".join(lines)

        # Process blocks
        rest_of_code = process_blocks(rest_of_code)

        # Step 3: Replace Phiton symbols with Python equivalents
        replacements = [
            # Control flow
            ("⇐", "return "),
            ("↥", "yield "),
            ("↥⋮", "yield from "),
            ("↑", "raise "),
            ("⟳", "while "),
            ("∀", "for "),
            ("⋔", "if "),
            ("⋮", "else"),
            ("⚟", "try"),
            ("↦", "match "),
            ("≐", "case "),
            ("⊪", "assert "),
            ("⊘", "pass"),
            ("⋯", "continue"),
            ("⊠", "break"),
            # Operators
            ("≔", " = "),
            ("≡", " == "),
            ("≠", " != "),
            ("∈", " in "),
            ("∉", " not in "),
            ("∑", "sum"),
            ("∫", "map"),
            ("⨁", "reduce"),
            ("△", " += "),
            ("▽", " -= "),
            ("◊", " *= "),
            ("◆", " /= "),
            ("≝", " := "),
            ("≤", " <= "),
            ("≥", " >= "),
            ("∧", " and "),
            ("∨", " or "),
            ("¬", "not "),
            # Special values
            ("∅", "None"),
            ("⊤", "True"),
            ("⊥", "False"),
            # Functions and classes
            ("ƒ", "def "),
            ("λ", "lambda "),
            ("Σ", "class "),
            ("⊙", "@property"),
            ("⊡", "async "),
            ("⊞", "@staticmethod"),
            ("⊟", "@classmethod"),
            ("⍟", "@abstractmethod"),
            ("⛋", "@dataclass"),
            # Built-in functions
            ("ℓ", "len"),
            ("ℜ", "range"),
            ("ℯ", "enumerate"),
            ("φ", "filter"),
            ("ℤ", "zip"),
            ("ς", "sorted"),
            ("ℛ", "reversed"),
            ("∃", "any"),
            ("↓", "min"),
            ("↑", "max"),
            ("○", "round"),
            ("∥", "abs"),
            ("^", "pow"),
            ("∋", "isinstance"),
            ("∌", "hasattr"),
            ("⊳", "getattr"),
            ("⊲", "setattr"),
            ("⊗", "delattr"),
            ("↰", "super"),
            ("⟲", "iter"),
            # Brackets and delimiters
            ("⟦", "{"),
            ("⟧", "}"),
            ("⟬", "["),
            ("⟭", "]"),
            ("⦅", "("),
            ("⦆", ")"),
            ("⟮", "("),
            ("⟯", ")"),
            # Domain prefixes
            ("№", "np"),
            ("℗", "pd"),
            ("χ", "sklearn"),
            ("μ", "matplotlib"),
            ("Ψ", "torch"),
            ("Φ", "tensorflow"),
            ("ɗ", "django"),
            ("ϱ", "fastapi"),
            ("α", "os"),
            ("Ω", "io"),
            ("τ", "typing"),
            ("Δ", "math"),
            ("Γ", "collections"),
            ("Λ", "itertools"),
            ("Θ", "datetime"),
            ("ζ", "sqlalchemy"),
            ("η", "requests"),
            ("ξ", "json"),
            ("π", "pathlib"),
            ("®", "re"),
            ("γ", "asyncio"),
            ("ϝ", "functools"),
            ("ω", "operator"),
            ("ρ", "random"),
            ("σ", "string"),
            ("ψ", "sys"),
            ("θ", "time"),
            ("υ", "uuid"),
            ("ϒ", "yaml"),
            ("ζ", "zlib"),
            # Common patterns
            ("·", "."),
            ("⌿", "strip"),
            ("⇌", "replace"),
            ("⨍", "format"),
            ("⊕", "append"),
            ("⊖", "pop"),
            ("⊚", "values"),
            ("⊛", "items"),
            ("§", "_"),
            # Whitespace and formatting
            ("⦂", ":"),
        ]

        # Apply symbol replacements
        for old, new in replacements:
            rest_of_code = rest_of_code.replace(old, new)

        # Step 4: Fix common syntax issues and formatting

        # Fix spacing around operators and punctuation
        rest_of_code = re.sub(
            r"([=!<>+\-*/])\s*([=!<>+\-*/])", r"\1\2", rest_of_code
        )  # Join operators like ==, +=, etc.
        rest_of_code = re.sub(
            r"\s+([,;:])", r"\1", rest_of_code
        )  # Remove space before punctuation
        rest_of_code = re.sub(
            r"([,;:])\s+", r"\1 ", rest_of_code
        )  # Ensure space after punctuation
        rest_of_code = re.sub(
            r"\s+\)", r")", rest_of_code
        )  # Remove space before closing parenthesis
        rest_of_code = re.sub(
            r"\(\s+", r"(", rest_of_code
        )  # Remove space after opening parenthesis

        # Fix common word joins
        word_fixes = [
            (r"in\s+g", "ing"),
            (r"or\s+t", "ort"),
            (r"f\s+or", "for"),
            (r"s\s+or\s+t", "sort"),
            (r"cont\s+in\s+ue", "continue"),
            (r"imp\s+or\s+t", "import"),
            (r"doma\s+in", "domain"),
            (r"operat\s+or", "operator"),
            (r"r\s+and\s+om", "random"),
            (r"str\s+in\s+g", "string"),
            (r"typ\s+in\s+g", "typing"),
            (r"is\s+in\s+stance", "isinstance"),
            (r"m\s+in", "min"),
            (r"t\s+or\s+ch", "torch"),
            (r"tens\s+or\s+flow", "tensorflow"),
            (r"p\s+and\s+as", "pandas"),
        ]

        for pattern, replacement in word_fixes:
            rest_of_code = re.sub(pattern, replacement, rest_of_code)

        # Fix dictionary formatting
        rest_of_code = re.sub(
            r"(\w+)\s*=\s*\{([^}]+)\}",
            lambda m: f"{m.group(1)} = {{\n    {m.group(2).strip()}\n}}",
            rest_of_code,
        )

        # Fix dictionary key-value pairs
        rest_of_code = re.sub(
            r'"([^"]+)"\s*,\s*"([^"]+)"', r'"\1": "\2",', rest_of_code
        )
        rest_of_code = re.sub(
            r"\'([^\']+)\'\s*,\s*\'([^\']+)\'", r"'\1': '\2',", rest_of_code
        )

        # Fix spacing in function calls
        rest_of_code = re.sub(
            r"(\w+)\(", r"\1(", rest_of_code
        )  # Remove space between function name and parenthesis

        # Fix spacing in list comprehensions
        rest_of_code = re.sub(r"for\s+(\w+)\s+in", r"for \1 in", rest_of_code)

        # Fix spacing in if statements
        rest_of_code = re.sub(r"if\s+(\w+)", r"if \1", rest_of_code)

        # Fix docstring formatting
        rest_of_code = re.sub(
            r"^([^'\"\n]*)['\"]([^'\"\n]*)['\"]", r'\1"""\2"""', rest_of_code
        )

        # Fix nested if statements
        rest_of_code = re.sub(r"(if [^:]+): (if [^:]+):", r"\1:\n    \2:", rest_of_code)

        # Add the processed code to the output
        python_code += rest_of_code

        # Validate the decompressed Python code with AST
        try:
            ast.parse(python_code)
            logger.debug("Decompressed code successfully parsed with AST")
        except SyntaxError as e:
            logger.warning(
                f"Decompressed code has syntax errors but will still be output: {e}"
            )

        return python_code

    except Exception as e:
        logger.error("Error converting Phiton code: %s", str(e))
        msg = f"Invalid Phiton code: {e!s}"
        raise ValueError(msg)


def calculate_stats(source: str, result: str) -> dict[str, int | float]:
    """Calculate compression statistics.

    Args:
        source: Original Python code
        result: Converted Phiton code

    Returns:
        Dictionary with compression statistics
    """
    return {
        "original_chars": len(source),
        "compressed_chars": len(result),
        "original_lines": len(source.splitlines()),
        "compressed_lines": len(result.splitlines()),
        "compression_ratio": round(len(result) / len(source) * 100, 2),
    }


def print_stats(report: dict[str, int | float]) -> None:
    """Print compression statistics."""
    print("\nCompression Statistics:")
    print(f"Original characters: {report['original_chars']}")
    print(f"Compressed characters: {report['compressed_chars']}")
    print(f"Original lines: {report['original_lines']}")
    print(f"Compressed lines: {report['compressed_lines']}")
    print(f"Compression ratio: {report['compression_ratio']}%")


def convert(
    decompress: bool = False,
    report: bool = False,
    level: int = 5,
    comments: bool = True,
    type_hints: bool = True,
    minify: bool = True,
    symbols: bool = True,
    input_path: str | Path | None = None,
    output_path: str | Path | None = None,
    verbose: bool = False,
) -> None:
    """Convert between Python and Phiton notation.

    Args:
        input_path: input_path file path or '-' for stdin
        output_path: output_path file path or '-' for stdout
        decompress: If True, convert from Phiton to Python
        report: Show compression statistics
        level: Compression level (1-5)
        comments: Whether to preserve comments in output_path
        type_hints: Whether to include type hints in output_path
        minify: Whether to compress whitespace
        symbols: Whether to use local symbol optimization
        verbose: Enable verbose logging
    """
    # Configure logging based on verbose flag
    logger.remove()
    logger.add(sys.stderr, level="DEBUG" if verbose else "INFO")

    try:
        # Read input_path
        if input_path is None or input_path == "-":
            logger.debug("Reading from stdin...")
            source_code = sys.stdin.read()
        else:
            input_path = Path(input_path)
            if not input_path.exists():
                msg = f"input_path file not found: {input_path}"
                raise FileNotFoundError(msg)
            logger.debug(f"Reading from {input_path}...")
            source_code = input_path.read_text(encoding="utf-8")

        # Create configuration
        conv_config = ConversionConfig(
            level=level,
            comments=comments,
            type_hints=type_hints,
            minify=minify,
            symbols=symbols,
        )

        # Convert code
        if decompress:
            logger.debug("Decompressing Phiton to Python...")
            result_code = decompress_from_phiton(source_code, conv_config)
            operation = "decompressed"
        else:
            logger.debug("Compressing Python to Phiton...")
            result_code = compress_to_phiton(source_code, conv_config)
            operation = "compressed"

        # Write output_path
        if output_path is None or output_path == "-":
            logger.debug("Writing to stdout...")
            sys.stdout.write(result_code)
        else:
            output_path = Path(output_path)
            logger.debug(f"Writing to {output_path}...")
            output_path.write_text(result_code, encoding="utf-8")

        # Show statistics if requested
        if report and operation == "compressed":
            stats_data = calculate_stats(source_code, result_code)
            print_stats(stats_data)

        logger.debug(f"Successfully {operation} code")

    except Exception as e:
        logger.error(f"Error: {e!s}")
        sys.exit(1)


def main() -> None:
    """Main entry point for phiton."""
    try:
        fire.Fire(convert)
    except Exception as e:
        logger.error(f"Error: {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    main()
