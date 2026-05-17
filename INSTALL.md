# Installation Guide

This guide covers the different ways to install Phiton.

## Quick Installation

### Using the install script (Recommended)

```bash
curl -sSf https://raw.githubusercontent.com/twardoch/phiton/main/install.sh | bash
```

Installs the latest binary to `~/.local/bin` and detects your platform automatically.

### Using pip/uv

```bash
# Using pip
pip install phiton

# Using uv (faster, preferred)
uv pip install phiton
```

### Using precompiled binaries

Download the correct binary from the [latest release](https://github.com/twardoch/phiton/releases/latest):

- **Linux**: `phiton-ubuntu-latest`
- **Windows**: `phiton-windows-latest.exe`
- **macOS**: `phiton-macos-latest`

Make it executable and test:

```bash
# Linux/macOS
chmod +x phiton-ubuntu-latest
./phiton-ubuntu-latest --help

# Windows
phiton-windows-latest.exe --help
```

## Detailed Installation Methods

### 1. Install Script Options

The script accepts these arguments:

```bash
# Install to a specific directory
curl -sSf https://raw.githubusercontent.com/twardoch/phiton/main/install.sh | bash -s -- --dir /usr/local/bin

# Install a specific version
curl -sSf https://raw.githubusercontent.com/twardoch/phiton/main/install.sh | bash -s -- --version v1.0.0

# Skip PATH modification
curl -sSf https://raw.githubusercontent.com/twardoch/phiton/main/install.sh | bash -s -- --no-path

# Show help
curl -sSf https://raw.githubusercontent.com/twardoch/phiton/main/install.sh | bash -s -- --help
```

### 2. Manual Binary Installation

1. Visit the [releases page](https://github.com/twardoch/phiton/releases)
2. Download the binary for your system
3. Move it to a directory in your PATH:

```bash
# Linux/macOS system-wide
sudo mv phiton-ubuntu-latest /usr/local/bin/phiton
sudo chmod +x /usr/local/bin/phiton

# Or user-only
mkdir -p ~/.local/bin
mv phiton-ubuntu-latest ~/.local/bin/phiton
chmod +x ~/.local/bin/phiton
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Development Installation

To work on Phiton or test unreleased features:

```bash
# Clone the repo
git clone https://github.com/twardoch/phiton.git
cd phiton

# Install UV if missing
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up virtual environment and dependencies
uv venv --python 3.12
source .venv/bin/activate
uv sync

# Install in editable mode
uv pip install -e .

# Run tests
./scripts/test.sh

# Build the project
./scripts/build.sh
```

### 4. Docker Installation

```bash
# Build the image
docker build -t phiton .

# Run Phiton on a file
docker run --rm -v $(pwd):/workspace phiton example.py
```

## Verification

Check that Phiton works after installation:

```bash
# Check version
phiton --version

# Test basic functionality
echo "def hello(): print('Hello, world!')" | phiton

# Show help
phiton --help
```

## Platform-Specific Notes

### Linux

Built on Ubuntu. Should work on most modern Linux systems.  
If it doesn't:

1. Confirm glibc is installed
2. Try installing with pip/uv instead
3. Check execute permissions

### macOS

Built for recent macOS versions.  
For older systems:

1. Install via pip/uv
2. Update Xcode command line tools
3. Allow the binary in System Preferences > Security if needed

### Windows

Built for Windows 10/11.  
Older versions might need:

1. Installation via pip/uv
2. Latest Microsoft Visual C++ Redistributable
3. Running from Command Prompt or PowerShell

## Troubleshooting

### Common Issues

1. **Command not found**: Verify the install directory is in your PATH
2. **Permission denied**: Check execute permissions on the binary
3. **Version mismatch**: Clear pip cache and reinstall

### Getting Help

- Read the [troubleshooting guide](https://github.com/twardoch/phiton/wiki/Troubleshooting)
- File an issue on [GitHub](https://github.com/twardoch/phiton/issues)
- Ask in [Discussions](https://github.com/twardoch/phiton/discussions)

## Uninstall

### Binary Installation

```bash
# Remove the binary
rm ~/.local/bin/phiton  # or your custom install path

# Remove PATH modifications (edit your shell config file if needed)
```

### Pip Installation

```bash
pip uninstall phiton
```

### UV Installation

```bash
uv pip uninstall phiton
```