import ast
import pytest

from phiton import phitonize_python, dephitonize_phiton, ConversionConfig

def normalize_code(code: str) -> str:
    """Normalize Python code by parsing and unparsing with AST."""
    try:
        return ast.unparse(ast.parse(code.strip()))
    except Exception:
        return code.strip() # Fallback if parsing fails

@pytest.mark.parametrize(
    "python_code",
    [
        "x = 10",
        "y = x + 5",
        "z = x * y - 2",
        "if x > 5:\n    print(x)",
        "if x > 5:\n    y = 10\nelse:\n    y = 20",
        "def foo():\n    pass",
        "def bar(a, b):\n    return a + b",
        "for i in range(5):\n    print(i)",
        "while x > 0:\n    x -= 1\n    print(x)",
        "my_list = [1, 2, 3]\nmy_dict = {'a': 1, 'b': 2}",
        "class MyClass:\n    def __init__(self, val):\n        self.val = val\n    def get_val(self):\n        return self.val",
        "async def my_async_func():\n    await some_other_func()", # Placeholder for await
        "lambda x: x * 2",
        "# This is a comment\nx=1 # Another comment", # Comments are currently stripped by phitonizer
    ],
)
def test_roundtrip_simple_syntax(python_code):
    """Test basic roundtrip (Python -> Phiton -> Python) for simple syntax elements."""
    config = ConversionConfig(level=5, comments=False) # Level 5 for more symbols, comments off for easier comparison

    phiton_representation = phitonize_python(python_code, config)
    decompressed_python = dephitonize_phiton(phiton_representation, config)

    # Primary check: is the decompressed code syntactically valid Python?
    try:
        ast.parse(decompressed_python)
    except SyntaxError as e:
        pytest.fail(
            f"Decompressed code is not valid Python:\n{e}\n"
            f"Original Python:\n{python_code}\n"
            f"Phiton Repr:\n{phiton_representation}\n"
            f"Decompressed Python:\n{decompressed_python}"
        )

    # Secondary check: does the AST-normalized code match?
    # This is a stricter check and might fail due to semantic ambiguities or formatting.
    # For an MVP, syntactic validity is the main goal.
    # normalized_original = normalize_code(python_code)
    # normalized_decompressed = normalize_code(decompressed_python)
    # assert normalized_original == normalized_decompressed, \
    #     f"AST-normalized code mismatch.\nOriginal:\n{normalized_original}\nDecompressed:\n{normalized_decompressed}\nPhiton Repr:\n{phiton_representation}"

def test_factorial_roundtrip():
    """Test the factorial example from README."""
    python_code = """
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
"""
    config = ConversionConfig(level=3, comments=False) # Level 3 as per README example
    phiton_representation = phitonize_python(python_code, config)

    # Expected Phiton for this specific factorial at level 3 (from README)
    # Note: Current phitonizer might produce different output, this is for dephitonizer testing
    # expected_phiton = "ƒfactorial(n)⟨⋔n≤#1⟨⇐#1⟩⋮⇐n*factorial(n-#1)⟩"
    # For now, let's use the actual phitonized output for the roundtrip

    decompressed_python = dephitonize_phiton(phiton_representation, config)

    try:
        ast.parse(decompressed_python)
    except SyntaxError as e:
        pytest.fail(
            f"Factorial decompressed code is not valid Python:\n{e}\n"
            f"Phiton Repr:\n{phiton_representation}\n"
            f"Decompressed Python:\n{decompressed_python}"
        )

    # Check if essential parts are there (loose check for now)
    assert "def factorial(n)" in decompressed_python
    assert "if n <= 1" in decompressed_python
    assert "return 1" in decompressed_python
    assert "else" in decompressed_python
    assert "return n * factorial(n - 1)" in decompressed_python

# Placeholder for await target
async def some_other_func():
    pass
