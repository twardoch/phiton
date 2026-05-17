# Phiton Specification

Phiton is a symbolic notation for Python that uses Unicode characters to represent syntax more concisely. It's designed to compress code while remaining readable to those familiar with mathematical or physics notation.

## 1. Phiton Syntax (Concise Spec)

Phiton compresses Python using Unicode symbols:

**Control flow:** `⇐` (return), `↥` (yield), `⟳` (while), `∀` (for), `⋔` (if), `⋮` (else), `⊘` (pass), `⊠` (break), `⋯` (continue)

**Operators:** `≔` (=), `≡` (==), `≠` (!=), `∈` (in), `∉` (not in), `∧` (and), `∨` (or), `¬` (not), `≤` (<=), `≥` (>=)

**Special values:** `∅` (None), `⊤` (True), `⊥` (False)

**Functions:** `ƒ` (def), `λ` (lambda), `Σ` (class), `⊡` (async/await)

**Block structure:** `⟨...⟩` (indented blocks), `→` (statement separator)

**Common functions:** `ℓ` (len), `ℜ` (range), `ℯ` (enumerate), `φ` (filter), `ℤ` (zip), `ς` (sorted), `ℛ` (reversed)

**Domain prefixes:** `№` (numpy), `℗` (pandas), `χ` (sklearn), `μ` (matplotlib), `Ψ` (torch), `Φ` (tensorflow)

**Literals:** `#123` (numbers), `$text` (strings)

## 2. Phiton Syntax (Detailed Spec)

### 2.1. Introduction

Phiton represents Python code using Unicode characters. It serves as both a compression format and alternative syntax that emphasizes structural patterns.

### 2.2. Rationale

1. **Code Compression**: Reduce source code size while preserving meaning
2. **Visual Distinctiveness**: Make patterns immediately recognizable
3. **Semantic Clarity**: Use symbols that match programming concepts
4. **Pattern Recognition**: Standardize common idioms into concise forms
5. **Domain-Specific Optimization**: Shorthand for library operations
6. **Flexible Compression**: Support different levels based on needs

### 2.3. Core Language Elements

#### 2.3.1. Control Flow

| Phiton | Python | Description |
|--------|--------|-------------|
| `⇐` | `return` | Return statement |
| `↥` | `yield` | Yield statement |
| `↥⋮` | `yield from` | Yield from statement |
| `↑` | `raise` | Raise exception |
| `⟳` | `while` | While loop |
| `∀` | `for` | For loop |
| `⋔` | `if` | If statement |
| `⋮` | `else` | Else statement |
| `<tool_call>` | `try` | Try statement |
| `↦` | `match` | Match statement |
| `≐` | `case` | Case statement |
| `⊪` | `assert` | Assert statement |
| `⊘` | `pass` | Pass statement |
| `⋯` | `continue` | Continue statement |
| `⊠` | `break` | Break statement |

#### 2.3.2. Operators and Assignments

| Phiton | Python | Description |
|--------|--------|-------------|
| `≔` | `=` | Assignment |
| `≡` | `==` | Equality |
| `≠` | `!=` | Inequality |
| `∈` | `in` | Membership test |
| `∉` | `not in` | Negative membership |
| `∑` | `sum` | Sum function |
| `∫` | `map` | Map function |
| `⨁` | `reduce` | Reduce function |
| `△` | `+=` | Add and assign |
| `▽` | `-=` | Subtract and assign |
| `◊` | `*=` | Multiply and assign |
| `◆` | `/=` | Divide and assign |
| `≝` | `:=` | Walrus operator |
| `≤` | `<=` | Less than or equal |
| `≥` | `>=` | Greater than or equal |
| `∧` | `and` | Logical AND |
| `∨` | `or` | Logical OR |
| `¬` | `not` | Logical NOT |
| `⁇` | `is` | Identity test |
| `⁇¬` | `is not` | Negated identity test |

#### 2.3.3. Special Values

| Phiton | Python | Description |
|--------|--------|-------------|
| `∅` | `None` | None value |
| `⊤` | `True` | Boolean true |
| `⊥` | `False` | Boolean false |

#### 2.3.4. Functions and Classes

| Phiton | Python | Description |
|--------|--------|-------------|
| `ƒ` | `def` | Function definition |
| `λ` | `lambda` | Lambda function |
| `Σ` | `class` | Class definition |
| `⊙` | `@property` | Property decorator |
| `⊡` | `async`/`await` | Async/await |
| `⊞` | `@staticmethod` | Static method |
| `⊟` | `@classmethod` | Class method |
| `⍟` | `@abstractmethod` | Abstract method |
| `⛋` | `@dataclass` | Dataclass |

#### 2.3.5. Built-in Functions

| Phiton | Python | Description |
|--------|--------|-------------|
| `ℓ` | `len` | Length function |
| `ℜ` | `range` | Range function |
| `ℯ` | `enumerate` | Enumerate function |
| `φ` | `filter` | Filter function |
| `ℤ` | `zip` | Zip function |
| `ς` | `sorted` | Sorted function |
| `ℛ` | `reversed` | Reversed function |
| `∃` | `any` | Any function |
| `∀` | `all` | All function |
| `↓` | `min` | Min function |
| `↑` | `max` | Max function |
| `○` | `round` | Round function |
| `∥` | `abs` | Absolute value |
| `^` | `pow` | Power function |
| `Π` | `print` | Print function |

#### 2.3.6. Object Operations

| Phiton | Python | Description |
|--------|--------|-------------|
| `∋` | `isinstance` | Type check |
| `∌` | `hasattr` | Attribute check |
| `⊳` | `getattr` | Get attribute |
| `⊲` | `setattr` | Set attribute |
| `⊗` | `delattr` | Delete attribute |
| `↰` | `super` | Super function |
| `→` | `next` | Next function |
| `⟲` | `iter` | Iterator function |
| `·` | `.` | Attribute access |

#### 2.3.7. Block Structure

| Phiton | Python | Description |
|--------|--------|-------------|
| `⟨...⟩` | Indented block | Code block |
| `→` | Newline | Statement separator |
| `⦂` | `:` | Type annotation |

#### 2.3.8. Literals and Containers

| Phiton | Python | Description |
|--------|--------|-------------|
| `#123` | `123` | Numeric literal |
| `$text` | `"text"` | String literal |
| `⟦...⟧` | `{...}` | Dict/set comprehension |
| `⟬...⟭` | `[...]` | List comprehension |
| `⦅...⦆` | `(...)` | Tuple |
| `⟮...⟯` | `(...)` | Grouping |

#### 2.3.9. String Operations

| Phiton | Python | Description |
|--------|--------|-------------|
| `⌿` | `strip` | Strip whitespace |
| `⇌` | `replace` | Replace substring |
| `⨍` | `format` | Format string |
| `「...」` | `f'...'` | F-string |

#### 2.3.10. Collection Operations

| Phiton | Python | Description |
|--------|--------|-------------|
| `⊕` | `append` | Append to list |
| `⊖` | `pop` | Pop from list |
| `⊚` | `values` | Dictionary values |
| `⊛` | `items` | Dictionary items |

### 2.4. Domain-Specific Prefixes

| Phiton | Python | Description |
|--------|--------|-------------|
| `№` | `numpy` | NumPy library |
| `℗` | `pandas` | Pandas library |
| `χ` | `sklearn` | Scikit-learn library |
| `μ` | `matplotlib` | Matplotlib library |
| `Ψ` | `torch` | PyTorch library |
| `Φ` | `tensorflow` | TensorFlow library |
| `φ` | `flask` | Flask library |
| `ɗ` | `django` | Django library |
| `ϱ` | `fastapi` | FastAPI library |
| `α` | `os` | OS library |
| `Ω` | `io` | IO library |
| `τ` | `typing` | Typing library |
| `Δ` | `math` | Math library |
| `Γ` | `collections` | Collections library |
| `Λ` | `itertools` | Itertools library |
| `Θ` | `datetime` | Datetime library |
| `ζ` | `sqlalchemy`/`zlib` | SQLAlchemy/zlib library |
| `η` | `requests` | Requests library |
| `ξ` | `json` | JSON library |
| `π` | `pathlib` | Pathlib library |
| `®` | `re` | Regex library |
| `γ` | `asyncio` | Asyncio library |
| `ϝ` | `functools` | Functools library |
| `ω` | `operator` | Operator library |
| `ρ` | `random` | Random library |
| `σ` | `string` | String library |
| `ψ` | `sys` | System library |
| `θ` | `time` | Time library |
| `υ` | `uuid` | UUID library |
| `ϒ` | `yaml` | YAML library |

### 2.5. Pattern Replacements

| Python Pattern | Phiton Equivalent |
|----------------|-------------------|
| `if x is not None` | `⋔x≠∅` |
| `if x is None` | `⋔x≡∅` |
| `for i in range(n)` | `∀i∈ℜ(n)` |
| `for i, x in enumerate(xs)` | `∀i,x∈ℯ(xs)` |
| `return [x for x in xs if p(x)]` | `⇐[x∀x∈xs⋔p(x)]` |
| `lambda x: f(x)` | `λx⇒f(x)` |
| `with open(f) as h` | `⊢⊣⊗(f)⇒h` |
| `try: x\nexcept E: y` | `<tool_call>⟨x⟩⋔E⟨y⟩` |
| `if p: return x` | `⋔p⇐x` |
| `if not p: return` | `⋔¬p⇐` |
| `x if p else y` | `p?x:y` |
| `[f(x) for x in xs]` | `∫(f,xs)` |
| `sum(x for x in xs)` | `∑(xs)` |
| `all(p(x) for x in xs)` | `∀(p,xs)` |
| `any(p(x) for x in xs)` | `∃(p,xs)` |

### 2.6. Advanced Patterns

| Python Pattern | Phiton Equivalent |
|----------------|-------------------|
| `df.groupby(X).agg(Y)` | `§df·Γ(X)·A(Y)` |
| `np.array(X).reshape(Y)` | `№·A(X)·R(Y)` |
| `pd.DataFrame(X).reset_index()` | `℗·D(X)·R()` |
| `[x for x in X if C]` | `[x∀x∈X⋔C]` |
| `{k:v for k,v in X.items()}` | `{k:v∀k,v∈X·⊙}` |
| `list(map(F, X))` | `∫(F,X)` |
| `next(x for x in X if P)` | `→(x∀x∈X⋔P)` |
| `sorted(X, key=lambda x: x.Y)` | `ς(X,λx:x·Y)` |
| `if x is not None: return x\nelse: return y` | `⇐x≢∅?x:y` |
| `try:\n    x\nexcept E as e:\n    y` | `</tool_call>⟨x⟩⋔E⇒e⟨y⟩` |
| `async with aiohttp.ClientSession() as session:` | `⊢⊣⊡η·S()⇒s⟨` |
| `await asyncio.gather(*tasks)` | `⊡γ·G(◇t)` |
| `'.'.join(x for x in X)` | `·⊕(X)` |
| `x.strip().lower()` | `x·⌿·↓` |
| `math.floor(x/y)` | `⌊x/y⌋` |
| `math.ceil(x/y)` | `⌈x/y⌉` |
| `abs(x-y)` | `∥x-y∥` |
| `math.sqrt(x)` | `√x` |
| `with open(X, 'r') as f:` | `⊢⊣⊗(X,'r')⇒f⟨` |
| `collections.defaultdict(list)` | `Γ·∂(ℓ)` |
| `assert x == y` | `⊪x≡y` |
| `raise ValueError(X)` | `↑V(X)` |
| `datetime.datetime.now()` | `Θ·N()` |

### 2.7. Compression Levels

1. **Level 1**: Basic conversion with readable symbols and preserved structure
2. **Level 2**: More symbol substitutions but maintain readability
3. **Level 3**: Full symbol substitution with some structure preservation
4. **Level 4**: Aggressive symbol substitution and minimal structure
5. **Level 5**: Maximum compression with shortest representation

### 2.8. Conversion Process

#### Python to Phiton (`phitonize`)

1. Parse Python code into AST
2. Traverse AST and convert each node to Phiton notation
3. Apply pattern replacements for common idioms
4. Apply compression optimizations based on level
5. Generate symbol table for frequently used expressions
6. Optimize imports and structure

#### Phiton to Python (`dephitonize`)

1. Apply symbol replacements to convert Phiton to Python
2. Replace numeric and string literals
3. Fix function definitions and calls
4. Process blocks and indentation
5. Validate the decompressed Python code

### 2.9. Examples

#### Factorial Function

**Python:**
```python
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
```

**Phiton (Level 3):**
```
ƒfactorialn⟨⋔n≤#1⟨⇐#1⟩⋮⇐n*factorialn-#1⟩
```

#### List Comprehension

**Python:**
```python
[x * 2 for x in range(10) if x % 2 == 0]
```

**Phiton (Level 3):**
```
[x*#2∀x∈ℜ(#10)⋔x%#2≡#0]
```

#### Class Definition

**Python:**
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, my name is {self.name}"
```

**Phiton (Level 3):**
```
ΣPerson⟨ƒ__init__self,name,age⟨self·name≔name→self·age≔age⟩→ƒgreetself⟨⇐「Hello, my name is {self·name}」⟩⟩
```

### 2.10. Implementation Notes

1. **AST-based Conversion**: Both phitonize and dephitonize use Python's AST for reliable transformation
2. **Pattern Priority**: More specific patterns take precedence over general ones
3. **Symbol Table**: Frequently used expressions are cached
4. **Scope Awareness**: Symbol substitutions respect Python scoping rules
5. **Validation**: Generated code is validated through AST parsing
6. **Error Handling**: Conversion errors provide detailed feedback
7. **Compression Optimization**: Advanced compression uses frequency analysis

### 2.11. Best Practices

1. Use compression level 1-2 for frequently read code
2. Use level 3 for balance of readability and compression
3. Reserve levels 4-5 for maximum compression when readability matters less
4. Document compression level in project metadata
5. Maintain style guide for consistent usage
6. Consider syntax highlighting for Phiton code
7. Include original Python in comments for complex transformations