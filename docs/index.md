---
title: Home
layout: default
nav_order: 1
---

# Phiton

Phiton rewrites Python in symbols. `def` becomes `ƒ`, `return` becomes `⇐`, `if`
becomes `⋔` — the same code, fewer characters, so more of it fits in an LLM
context window.

```python
# Python
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Phiton (level 5)
ƒ factorial(n⦂int)→int⟨⋔n≤#1⟨⇐#1⟩→⇐n*factorial(n-#1)⟩
```

## Install

```bash
pip install phiton
# or
uv pip install phiton
```

## Compress and restore

```bash
python -m phiton example.py                 # -> example.phi
python -m phiton example.phi --decompress   # -> example.py
python -m phiton example.py --level 3        # 1 = light, 5 = maximum
```

## Read next

- **[README on GitHub](https://github.com/twardoch/phiton#readme)** — full symbol
  table, compression levels, and the Python API.
- **Limitations** — statement-level code round-trips faithfully; control-flow
  blocks are a draft to review, not a lossless restore. See the README's
  Limitations section before relying on decompression.

Phiton earns its keep in one direction: squeeze Python down so more of it fits.
Byte-for-byte round-tripping of arbitrary programs is out of scope for now.
