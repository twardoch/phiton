#!/usr/bin/env -S uv run -s
# /// script
# dependencies = []
# ///
# this_file: src/phiton/constants.py

"""Constants and symbol mappings for Phiton conversion."""

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
    # "...": "⋮", # Removed conflict: ⋮ is primarily for 'else' and block structure. Ellipsis (...) should be handled as a literal or have its own symbol.
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
    # "all": "∀", # This conflicts with "for" loop. 'for' is more fundamental.
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
    # "next": "→", # → is a structural token for newline, not for next()
    "iter": "⟲",
    "is": "⁇",
    "is not": "⁇¬",  # For is not
    "print": "Π",
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
