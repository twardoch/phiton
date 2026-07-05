#!/usr/bin/env python3
# this_file: tests/test_dephitonizer.py
"""Round-trip tests for the Phiton dephitonizer.

Phiton guarantees a *semantic* round-trip (compress -> decompress produces
AST-equivalent Python) only for statement-level code — assignments and
expressions — at the structure-preserving levels 1 and 2. Control-flow blocks
rely on the dephitonizer's block-reconstruction heuristic, which is an
acknowledged MVP limitation (see README "Limitations" and TODO.md). Those cases
are marked ``xfail`` so the suite documents the gap honestly instead of hiding
it: the day the heuristic is fixed, pytest reports an unexpected pass.
"""

import ast

import pytest

from phiton import ConversionConfig, dephitonize_phiton, phitonize_python

# Statement-level snippets that round-trip to AST-equivalent Python. These are
# the contract Phiton actually keeps: symbol substitution is reversible when no
# block structure has to be rebuilt.
ROUNDTRIP_STATEMENTS = [
    "x = 10",
    "y = x + 5",
    "z = x * y - 2",
    "result = a * b + c",
    "flag = True",
    "name = other",
    "total = a + b + c + d",
    "a = 1\nb = 2\nc = 3",
    "x = 10\ny = 20\nz = x + y",
    "value = n - 1",
]

# Constructs whose round-trip depends on block reconstruction. Known-lossy today.
ROUNDTRIP_BLOCKS = [
    "if x > 5:\n    print(x)",
    "for i in range(5):\n    print(i)",
    "while x > 0:\n    x -= 1",
    "def bar(a, b):\n    return a + b",
]


@pytest.mark.parametrize("level", [1, 2])
@pytest.mark.parametrize("python_code", ROUNDTRIP_STATEMENTS)
def test_statement_roundtrip_preserves_ast(python_code: str, level: int) -> None:
    """compress -> decompress yields AST-equivalent Python for statements."""
    config = ConversionConfig(level=level, comments=False)

    phiton = phitonize_python(python_code, config)
    decompressed = dephitonize_phiton(phiton, config)

    assert ast.dump(ast.parse(decompressed)) == ast.dump(ast.parse(python_code)), (
        f"Round-trip changed semantics.\n"
        f"Original:\n{python_code}\nPhiton:\n{phiton}\nDecompressed:\n{decompressed}"
    )


@pytest.mark.xfail(
    reason="Block reconstruction is a naive heuristic (MVP); see README Limitations.",
    strict=False,
)
@pytest.mark.parametrize("python_code", ROUNDTRIP_BLOCKS)
def test_block_roundtrip_is_valid_python(python_code: str) -> None:
    """Documents the known gap: block constructs do not yet round-trip cleanly."""
    config = ConversionConfig(level=5, comments=False)

    phiton = phitonize_python(python_code, config)
    decompressed = dephitonize_phiton(phiton, config)

    ast.parse(decompressed)  # xfails today; will xpass once blocks round-trip.
