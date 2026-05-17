#!/usr/bin/env bash
# install.sh: Install phiton in editable mode
# phiton: Python source code compressor/transpiler

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Installing phiton (editable) ==="
uv pip install -e .
echo "=== Install complete ==="
