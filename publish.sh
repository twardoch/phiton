#!/usr/bin/env bash
# publish.sh: Build, install, version, and publish phiton to PyPI
# phiton: Python source code compressor/transpiler

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Build ==="
bash "$SCRIPT_DIR/build.sh"

echo "=== Install ==="
bash "$SCRIPT_DIR/install.sh"

echo "=== Version bump ==="
uvx gitnextver@latest

echo "=== Final build & publish ==="
uvx hatch build
uv publish

echo "=== Publish complete ==="
