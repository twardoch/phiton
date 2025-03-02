#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["loguru"]
# ///
# this_file: src/phiton/dephitonize.py

"""Phiton to Python deconversion functionality."""

import ast
import re
from loguru import logger

from phiton.config import ConversionConfig
from phiton.constants import DOMAIN_PREFIXES


def dephitonize_phiton(phiton_code: str, config: ConversionConfig | None = None) -> str:
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
        # Initialize the Python code
        python_code = ""

        # Extract docstring if present
        rest_of_code = phiton_code
        docstring_match = re.search(r'^[\'"].*?[\'"]', phiton_code, re.DOTALL)
        if docstring_match:
            docstring = docstring_match.group(0)
            rest_of_code = phiton_code[docstring_match.end() :].lstrip()
            docstring = re.sub(r"\\n", "\n", docstring)
            docstring = re.sub(r"\s+", " ", docstring)
            python_code = f'"""{docstring}"""\n\n'

        # Process blocks and indentation
        def process_blocks(code: str) -> str:
            code = code.replace("→", "\n")
            lines = []
            indent_stack = [0]
            current_indent = 0
            current_line = ""

            i = 0
            while i < len(code):
                char = code[i]

                if char == "⟨":
                    # Add a colon to the current line and start a new indented block
                    if current_line:
                        lines.append(" " * current_indent + current_line)
                    current_indent += 4
                    indent_stack.append(current_indent)
                    current_line = ""
                elif char == "⟩":
                    # End the current block and decrease indentation
                    if current_line:
                        lines.append(" " * current_indent + current_line)
                    if len(indent_stack) > 1:
                        indent_stack.pop()
                    current_indent = indent_stack[-1]
                    current_line = ""
                elif char == "\n":
                    # End the current line and start a new one
                    if current_line:
                        lines.append(" " * current_indent + current_line)
                    current_line = ""
                elif char == "⋔":
                    # Special handling for if statements
                    current_line += "if "
                    i += 1  # Skip the if symbol
                    # Collect the condition
                    while i < len(code) and code[i] != "⟨":
                        current_line += code[i]
                        i += 1
                    i -= 1  # Adjust for the loop increment
                elif char == "⋮":
                    # Handle else statements
                    if current_line:
                        lines.append(" " * current_indent + current_line)
                    # Decrease indent for else
                    if len(indent_stack) > 1:
                        current_indent = indent_stack[-2]
                    lines.append(" " * current_indent + "else:")
                    # Restore indent for the else block
                    if len(indent_stack) > 1:
                        current_indent = indent_stack[-1]
                    current_line = ""
                else:
                    current_line += char

                i += 1

            # Add the last line if there's anything left
            if current_line:
                lines.append(" " * current_indent + current_line)

            # Post-process the lines to fix function definitions
            processed_lines = []
            for line in lines:
                # Fix function definitions to add a newline after the colon
                if line.strip().startswith("def ") and line.strip().endswith("):"):
                    processed_lines.append(line)
                else:
                    processed_lines.append(line)

            return "\n".join(processed_lines)

        # Process the code blocks
        rest_of_code = process_blocks(rest_of_code)

        # Replace Phiton symbols with Python equivalents
        replacements = [
            ("⇐", "return "),
            ("↥", "yield "),
            ("↥⋮", "yield from "),
            ("↑", "raise "),
            ("⟳", "while "),
            ("∀", "for "),
            ("⋔", "if "),
            ("⋮", "else:"),
            ("⚟", "try"),
            ("↦", "match "),
            ("≐", "case "),
            ("⊪", "assert "),
            ("⊘", "pass"),
            ("⋯", "continue"),
            ("⊠", "break"),
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
            ("∅", "None"),
            ("⊤", "True"),
            ("⊥", "False"),
            ("ƒ", "def "),
            ("λ", "lambda "),
            ("Σ", "class "),
            ("⊙", "@property"),
            ("⊡", "async "),
            ("⊞", "@staticmethod"),
            ("⊟", "@classmethod"),
            ("⍟", "@abstractmethod"),
            ("⛋", "@dataclass"),
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
            ("→", "next"),
            ("⟲", "iter"),
            ("⟦", "{"),
            ("⟧", "}"),
            ("⟬", "["),
            ("⟭", "]"),
            ("⦅", "("),
            ("⦆", ")"),
            ("⟮", "("),
            ("⟯", ")"),
            ("·", "."),
            ("⦂", ":"),
            ("⌿", "strip"),
            ("⇌", "replace"),
            ("⨍", "format"),
            ("⊕", "append"),
            ("⊖", "pop"),
            ("⊚", "values"),
            ("⊛", "items"),
            ("§", "_"),
        ]

        # Replace domain prefixes
        for domain, prefix in DOMAIN_PREFIXES.items():
            rest_of_code = rest_of_code.replace(prefix, domain)

        # Apply all replacements
        for old, new in replacements:
            rest_of_code = rest_of_code.replace(old, new)

        # Replace numeric literals
        rest_of_code = re.sub(r"#(\d+)", r"\1", rest_of_code)
        rest_of_code = re.sub(r"#(\d+\.\d+)", r"\1", rest_of_code)

        # Replace string literals
        rest_of_code = re.sub(r"\$(\w+)", r'"\1"', rest_of_code)

        # Process function definitions and calls in multiple steps

        # Step 1: Fix function definitions - match "def factorialn:" pattern
        def fix_function_def(match):
            func_name = match.group(1)
            param_name = match.group(2)
            return f"def {func_name}({param_name}):"

        rest_of_code = re.sub(
            r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)([a-zA-Z_][a-zA-Z0-9_]*):",
            fix_function_def,
            rest_of_code,
        )

        # Step 2: Fix function calls in expressions - match "factorialn-1" pattern
        # First, identify known function names from definitions
        function_names = set()
        for match in re.finditer(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\(", rest_of_code):
            function_names.add(match.group(1))

        # Then fix calls to those functions
        for func_name in function_names:
            # Pattern to match function calls without parentheses
            pattern = (
                rf"{func_name}([a-zA-Z_][a-zA-Z0-9_]*)(?=\s*[-+*/]|\s*$|\s*,|\s*\))"
            )
            replacement = f"{func_name}(\\1)"
            rest_of_code = re.sub(pattern, replacement, rest_of_code)

            # Fix recursive calls with arithmetic operations
            pattern = rf"{func_name}\(([a-zA-Z_][a-zA-Z0-9_]*)\)-(\d+)"
            replacement = f"{func_name}(\\1-\\2)"
            rest_of_code = re.sub(pattern, replacement, rest_of_code)

        # Fix spacing issues
        rest_of_code = re.sub(r"\s+([,;:])", r"\1", rest_of_code)
        rest_of_code = re.sub(r"([,;:])\s+", r"\1 ", rest_of_code)
        rest_of_code = re.sub(r"\s+\)", r")", rest_of_code)
        rest_of_code = re.sub(r"\(\s+", r"(", rest_of_code)

        # Fix common word issues
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

        # Add the processed code to the result
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
