# GitHub Actions Workflows

Since the GitHub App doesn't have workflows permission, here are the enhanced workflow files that should be manually applied:

## Enhanced CI Workflow (`.github/workflows/push.yml`)

```yaml
name: Build & Test

on:
  push:
    branches: [main]
    tags-ignore: ["v*"]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write
  id-token: write

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Ruff lint
        uses: astral-sh/ruff-action@v3
        with:
          version: "latest"
          args: "check --output-format=github"

      - name: Run Ruff Format
        uses: astral-sh/ruff-action@v3
        with:
          version: "latest"
          args: "format --check --respect-gitignore"

  test:
    name: Run Tests
    needs: quality
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
        os: [ubuntu-latest, windows-latest, macos-latest]
      fail-fast: false
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: ${{ matrix.python-version }}
          enable-cache: true
          cache-suffix: ${{ matrix.os }}-${{ matrix.python-version }}

      - name: Install test dependencies
        run: |
          uv pip install --system --upgrade pip
          uv pip install --system ".[test]"

      - name: Run tests with Pytest
        run: uv run pytest -n auto --maxfail=1 --disable-warnings --cov-report=xml --cov-config=pyproject.toml --cov=src/phiton --cov=tests tests/

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-${{ matrix.python-version }}-${{ matrix.os }}
          path: coverage.xml
        if: matrix.os == 'ubuntu-latest'

  build:
    name: Build Distribution
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Needed for proper versioning

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: "3.12"
          enable-cache: true

      - name: Install build tools
        run: uv pip install build hatchling hatch-vcs

      - name: Build distributions
        run: uv run python -m build --outdir dist

      - name: Upload distribution artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist-files
          path: dist/
          retention-days: 5

  build-binaries:
    name: Build Binaries
    needs: test
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.12"]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: ${{ matrix.python-version }}
          enable-cache: true

      - name: Install dependencies including PyInstaller
        run: |
          uv sync
          uv add pyinstaller

      - name: Build binary with PyInstaller
        run: |
          uv run pyinstaller --onefile --name phiton-${{ matrix.os }} --add-data "src/phiton:phiton" src/phiton/__main__.py
        shell: bash

      - name: Test binary (Unix)
        if: matrix.os != 'windows-latest'
        run: |
          ./dist/phiton-${{ matrix.os }} --version

      - name: Test binary (Windows)
        if: matrix.os == 'windows-latest'
        run: |
          ./dist/phiton-${{ matrix.os }}.exe --version

      - name: Upload binary artifacts
        uses: actions/upload-artifact@v4
        with:
          name: phiton-binary-${{ matrix.os }}
          path: dist/phiton-${{ matrix.os }}*
          retention-days: 5
```

## Enhanced Release Workflow (`.github/workflows/release.yml`)

```yaml
name: Release

on:
  push:
    tags: ["v*"]

permissions:
  contents: write
  id-token: write

jobs:
  test:
    name: Run Tests
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
        os: [ubuntu-latest, windows-latest, macos-latest]
      fail-fast: false
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: ${{ matrix.python-version }}
          enable-cache: true

      - name: Install test dependencies
        run: |
          uv sync

      - name: Run tests with Pytest
        run: uv run pytest -n auto --maxfail=1 --disable-warnings tests/

  build-distribution:
    name: Build Python Distribution
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: "3.12"
          enable-cache: true

      - name: Install build tools
        run: uv pip install build hatchling hatch-vcs

      - name: Build distributions
        run: uv run python -m build --outdir dist

      - name: Verify distribution files
        run: |
          ls -la dist/
          test -n "$(find dist -name '*.whl')" || (echo "Wheel file missing" && exit 1)
          test -n "$(find dist -name '*.tar.gz')" || (echo "Source distribution missing" && exit 1)

      - name: Upload distribution artifacts
        uses: actions/upload-artifact@v4
        with:
          name: python-distributions
          path: dist/

  build-binaries:
    name: Build Binaries
    needs: test
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.12"]
    runs-on: ${{ matrix.os }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"
          python-version: ${{ matrix.python-version }}
          enable-cache: true

      - name: Install dependencies including PyInstaller
        run: |
          uv sync
          uv add pyinstaller

      - name: Build binary with PyInstaller
        run: |
          uv run pyinstaller --onefile --name phiton-${{ matrix.os }} --add-data "src/phiton:phiton" src/phiton/__main__.py
        shell: bash

      - name: Test binary (Unix)
        if: matrix.os != 'windows-latest'
        run: |
          ./dist/phiton-${{ matrix.os }} --version

      - name: Test binary (Windows)
        if: matrix.os == 'windows-latest'
        run: |
          ./dist/phiton-${{ matrix.os }}.exe --version

      - name: Upload binary artifacts
        uses: actions/upload-artifact@v4
        with:
          name: phiton-binary-${{ matrix.os }}
          path: dist/phiton-${{ matrix.os }}*

  release:
    name: Create Release
    needs: [build-distribution, build-binaries]
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/phiton
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts/

      - name: Organize artifacts
        run: |
          mkdir -p release-assets
          cp -r artifacts/python-distributions/* release-assets/ || true
          cp -r artifacts/phiton-binary-*/* release-assets/ || true
          ls -la release-assets/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_TOKEN }}
          packages-dir: artifacts/python-distributions/

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: release-assets/*
          generate_release_notes: true
          body: |
            ## Installation

            ### Using pip/uv
            ```bash
            pip install phiton
            # or
            uv pip install phiton
            ```

            ### Using precompiled binaries
            Download the appropriate binary for your platform from the assets below:
            - `phiton-ubuntu-latest` - Linux binary
            - `phiton-windows-latest.exe` - Windows binary  
            - `phiton-macos-latest` - macOS binary

            Make the binary executable and run:
            ```bash
            chmod +x phiton-ubuntu-latest  # Linux/macOS only
            ./phiton-ubuntu-latest --help
            ```

            ## Changes in this release
            See the automatically generated release notes below.
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Manual Application Instructions

To apply these workflow enhancements:

1. **Copy the CI workflow**: Replace the contents of `.github/workflows/push.yml` with the enhanced CI workflow above
2. **Copy the Release workflow**: Replace the contents of `.github/workflows/release.yml` with the enhanced release workflow above

The key improvements include:
- ✅ **Multiplatform testing** - Tests on Ubuntu, Windows, and macOS
- ✅ **Binary compilation** - PyInstaller-based binary builds for all platforms
- ✅ **Artifact management** - Comprehensive artifact collection and release
- ✅ **Enhanced releases** - Rich release notes with installation instructions

## Testing the Workflows

After applying the workflows:

1. **Test CI**: Push changes to a branch and create a PR
2. **Test Release**: Create a git tag: `git tag v1.0.0 && git push origin v1.0.0`
3. **Verify Artifacts**: Check the release page for binary downloads

The workflows will automatically:
- Run tests on all platforms
- Build Python distributions
- Create platform-specific binaries
- Upload everything to PyPI and GitHub releases