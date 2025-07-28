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
from phiton.constants import DOMAIN_PREFIXES, PHITON_TO_PYTHON

# Pre-sort Phiton symbols by length (descending) to handle multi-char symbols correctly.
# Example: "==" (≡) should be replaced before "=" (≔) if "=" is part of "==".
# However, current PHITON_TO_PYTHON keys are single characters mostly, or unique multi-char.
# Sorting by length is a general good practice for robust replacement.
SORTED_PHITON_SYMBOLS = sorted(PHITON_TO_PYTHON.keys(), key=len, reverse=True)

REVERSE_DOMAIN_PREFIXES = {v: k for k, v in DOMAIN_PREFIXES.items()}
SORTED_REVERSE_DOMAIN_PREFIXES = sorted(REVERSE_DOMAIN_PREFIXES.keys(), key=len, reverse=True)


def _replace_symbols(code: str) -> str:
    """Replace Phiton symbols with Python equivalents."""
    # Replace domain prefixes first (e.g., №· -> numpy.)
    for phiton_prefix in SORTED_REVERSE_DOMAIN_PREFIXES:
        python_module = REVERSE_DOMAIN_PREFIXES[phiton_prefix]
        # Assuming domain prefixes are followed by "·" for attribute access
        code = code.replace(f"{phiton_prefix}·", f"{python_module}.")
        # If a domain prefix is used standalone (less common but possible)
        code = code.replace(phiton_prefix, python_module)


    for phiton_symbol in SORTED_PHITON_SYMBOLS:
        python_equivalent = PHITON_TO_PYTHON[phiton_symbol]
        # Add spaces around all replaced symbols initially.
        # Specific cases like '.' or '@' might need refinement if this is too broad.
        if python_equivalent == ".":
             code = code.replace(phiton_symbol, ".")
        elif python_equivalent.startswith("@"):
             code = code.replace(phiton_symbol, f"\n{python_equivalent}\n") # Decorators on new line
        else:
            code = code.replace(phiton_symbol, f" {python_equivalent} ")

    # Normalize multiple spaces to one
    code = re.sub(r" +", " ", code)
    # Clean up spaces around parentheses and commas for common cases
    code = code.replace(" ( ", "(").replace(" ) ", ")")
    code = code.replace(" [ ", "[").replace(" ] ", "]")
    code = code.replace(" { ", "{").replace(" } ", "}")
    code = code.replace(" , ", ", ")
    code = code.replace(" . ", ".") # a . b -> a.b
    return code.strip() # Strip leading/trailing for the whole processed string

def _handle_literals(code: str) -> str:
    """Convert Phiton literals to Python literals."""
    # Numeric literals: #123 -> 123, #12.3 -> 12.3
    # Ensure space if number follows an identifier (e.g. range#5 -> range 5)
    code = re.sub(r"([a-zA-Z_]\w*)#(-?\d+\.\d+)", r"\1 \2", code)
    code = re.sub(r"([a-zA-Z_]\w*)#(-?\d+)", r"\1 \2", code)
    code = re.sub(r"#(-?\d+\.\d+)", r"\1", code) # General case
    code = re.sub(r"#(-?\d+)", r"\1", code)     # General case

    # String literals: $text -> "text"
    # This needs to be careful not to mess with f-strings if they are handled differently
    code = re.sub(r"\$([a-zA-Z_][a-zA-Z0-9_]*)", r'"\1"', code) # Simple identifiers
    # TODO: Handle $ with spaces or more complex content if spec allows: $ "hello world" -> "\"hello world\""

    # F-string literals: 「...」 -> f"..."
    # This requires careful handling of internal {}
    # For now, a simple replacement. Complex f-strings might need more.
    code = re.sub(r"「(.*?)」", r'f"\1"', code)
    return code

def _reconstruct_blocks_and_lines(code: str) -> str:
    """Reconstruct indentation and newlines from Phiton block/line syntax."""
    # Split by Phiton structural tokens, now including 'else' (from ⋮) as a potential structure point
    tokens = re.split(r"(⟨|⟩|→| else | else:)", code) # Added ' else ' and ' else:'

    output_lines = []
    current_line_segments = []
    indent_level = 0
    indent_spaces = "    "

    for token in tokens:
        if token is None:
            continue
        token_stripped = token.strip()
        if not token_stripped: # Skip empty strings that can result from split
            continue

        if token_stripped == "⟨":
            if current_line_segments:
                line_content = "".join(current_line_segments).strip()
                if re.match(r"^(async\s+def|if|for|while|def|class|try|except|elif|else|with|match|case)\b", line_content) and not line_content.endswith(":"):
                    line_content += ":"
                output_lines.append(indent_spaces * indent_level + line_content)
                current_line_segments = []
            indent_level += 1
        elif token_stripped == "⟩":
            if current_line_segments:
                output_lines.append(indent_spaces * indent_level + "".join(current_line_segments).strip())
                current_line_segments = []
            indent_level = max(0, indent_level - 1)
        elif token_stripped == "→":
            if current_line_segments:
                output_lines.append(indent_spaces * indent_level + "".join(current_line_segments).strip())
                current_line_segments = []
        elif token_stripped in {"else", "else:"}:
            if current_line_segments:
                output_lines.append(indent_spaces * indent_level + "".join(current_line_segments).strip())
                current_line_segments = []

            # 'else' or 'else:' should be dedented by one level from current block content.
            # (current_indent is for content *inside* the if block)
            else_indent_level = max(0, indent_level - 1)
            output_lines.append(indent_spaces * else_indent_level + "else:")
            # Content of the else block (whether single line or ⟨...⟩) will start at this new level.
            indent_level = else_indent_level + 1
        elif token_stripped.startswith("elif "): # e.g. "elif condition" (colon added later)
            if current_line_segments:
                output_lines.append(indent_spaces * indent_level + "".join(current_line_segments).strip())
                current_line_segments = []
            elif_indent_level = max(0, indent_level - 1)
            output_lines.append(indent_spaces * elif_indent_level + token_stripped) # Add colon later
            indent_level = elif_indent_level + 1
        else:
            current_line_segments.append(token)

    if current_line_segments:
        output_lines.append(indent_spaces * indent_level + "".join(current_line_segments).strip())

    # Filter out any completely empty lines that might have been formed
    final_code = "\n".join(line for line in output_lines if line.strip())

    # Ensure block-starting keywords end with a colon if followed by an indented line,
    # but only if they don't already have one.
    # This is a bit heuristic.
    lines = final_code.split("\n")
    for i in range(len(lines) - 1):
        current_line_stripped = lines[i].strip()
        # Check if the line starts with a block keyword and is followed by an indented line
        if re.match(r"^(async\s+def|if|for|while|def|class|try|except|elif|else|with|match|case)\b", current_line_stripped):
            current_line_indent = len(lines[i]) - len(lines[i].lstrip())
            next_line_indent = len(lines[i+1]) - len(lines[i+1].lstrip())
            if next_line_indent > current_line_indent:
                if not lines[i].rstrip().endswith(":"): # Check rstrip to handle potential trailing spaces before colon
                    lines[i] = f"{lines[i].rstrip()}:"
    final_code = "\n".join(lines)

    return final_code.strip()


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

    logger.debug(f"Original Phiton code: {phiton_code}")
    processed_code = phiton_code

    # 1. Handle Literals (before symbol replacement if symbols might be in literals)
    processed_code = _handle_literals(processed_code)
    logger.debug(f"After literal handling: {processed_code}")

    # 2. Replace Phiton symbols with Python equivalents
    processed_code = _replace_symbols(processed_code)
    logger.debug(f"After symbol replacement: {processed_code}")

    # Ensure function/class definitions have parentheses if they were omitted by Phiton for no-arg cases
    # e.g. "def foo" becomes "def foo()"
    # This should be applied before block reconstruction which adds colons.
    processed_code = re.sub(r"^(def |class )([a-zA-Z_]\w*)$", r"\1\2()", processed_code, flags=re.MULTILINE)
    # And ensure space between name and open paren if phitonizer made it funcname(
    processed_code = re.sub(r"(def |class )([a-zA-Z_]\w*)\(", r"\1\2 (", processed_code) # Add space: name( -> name (
    # Attempt to fix def nameparam -> def name(param), very cautiously
    processed_code = re.sub(r"(def |class )([a-zA-Z_]\w+)([a-zA-Z_]\w+)(?=\s*[:⟨])", r"\1\2(\3)", processed_code)


    logger.debug(f"After func def/class fix: {processed_code}")

    # Specific fix for "await def" -> "async def"
    processed_code = processed_code.replace("await def ", "async def ")
    logger.debug(f"After async def fix: {processed_code}")

    # Insert newline marker (→) before 'else'/'elif' if they follow a block end '⟩'
    # or if they appear after a statement ending without '→' already.
    # This helps _reconstruct_blocks_and_lines to correctly place them.
    processed_code = re.sub(r"(⟩)( *(?:else|elif ))", r"\1→\2", processed_code)
    # If 'else:' or 'elif ...:' is not preceded by '→' or '⟨' (already handled by split),
    # and it's not start of string, it implies it followed a single statement.
    # This is harder to fix generally without breaking valid single-line if/else.
    # The phitonizer should ideally use '→⋮' for multiline 'else'.
    # For now, the re.split in _reconstruct_blocks_and_lines includes ' else ' and ' else:'
    # which should help isolate it.

    logger.debug(f"After else/elif pre-processing: {processed_code}")

    # 3. Reconstruct blocks and lines (basic for now)
    # This is the most complex part and current _reconstruct_blocks_and_lines is naive.
    # For MVP, it might only handle simple cases correctly.
    # The current _reconstruct_blocks_and_lines is too simple and likely incorrect for many cases.
    # The original factorial-specific logic was removed.
    # A proper parser or more sophisticated regex would be needed for robust block reconstruction.
    # For now, let's assume a very simplified block handling or rely on later formatting.

    # The old block processing logic was very specific.
    # Let's try a very basic structural replacement for now, then format.
    # Replace block start/end and statement separators
    # ⟨ -> start of new indented block
    # ⟩ -> end of indented block
    # → -> newline at current indent

    python_code = _reconstruct_blocks_and_lines(processed_code)
    logger.debug(f"After block/line reconstruction: {python_code}")

    # General clean up of spacing that might have occurred from symbol replacement and block reconstruction.
    python_code = re.sub(r" +\.", ".", python_code) # space before dot
    python_code = re.sub(r"\. +", ".", python_code) # space after dot
    python_code = re.sub(r" +,", ",", python_code)  # space before comma
    python_code = re.sub(r" +=", " =", python_code) # print = foo -> print=foo
    python_code = re.sub(r"= +", "= ", python_code) # print =foo -> print = foo
    python_code = re.sub(r" +\(", "(", python_code) # space before open paren
    python_code = re.sub(r" +\)", ")", python_code) # space before close paren (might be too aggressive)
    python_code = re.sub(r"\( +", "(", python_code) # space after open paren
    python_code = re.sub(r" +\)", ")", python_code) # space before close paren

    # Specific fix for "def funcname (params)" -> "def funcname(params)"
    python_code = re.sub(r"(def|class)\s+([\w_]+)\s+\(", r"\1 \2(", python_code)
    # Fix for "return value" -> "return value" (ensure one space)
    python_code = re.sub(r"return\s+(\S)", r"return \1", python_code)

    # Add parentheses for common functions if followed by a literal/identifier not in parens
    # e.g. "range 5" -> "range(5)", "len mylist" -> "len(mylist)"
    # This is a bit heuristic and might need refinement.
    common_funcs_requiring_parens = ["range", "len", "str", "int", "float", "list", "tuple", "dict", "set", "sum", "min", "max", "abs", "round", "sorted", "reversed", "enumerate", "zip", "filter", "map"]
    for func_name in common_funcs_requiring_parens:
        # Matches "funcname identifier" or "funcname literal" not followed by '('
        python_code = re.sub(rf"\b({func_name})\s+([a-zA-Z_]\w*|\d+\.?\d*)\b(?!\s*\()", r"\1(\2)", python_code)


    logger.debug(f"After final cleanups and func call fix: {python_code}")

    # Final validation with AST (optional, but good for debugging)
    try:
        ast.parse(python_code)
        logger.debug("Decompressed code successfully parsed with AST.")
    except SyntaxError as e:
        logger.warning(
            f"Decompressed code has syntax errors (will be output as is): {e}\nProblematic code snippet:\n---\n{python_code}\n---"
        )

    return python_code.strip()

    # except Exception as e:
    #     logger.error("Error converting Phiton code: %s", str(e))
    #     msg = f"Invalid Phiton code: {e!s}"
    #     raise ValueError(msg) from e
