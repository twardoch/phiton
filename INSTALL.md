# Installation Guide

This guide covers various ways to install Phiton on your system.

## Quick Installation

### Using the install script (Recommended)

```bash
curl -sSf https://raw.githubusercontent.com/twardoch/phiton/main/install.sh | bash
```

This will automatically detect your platform and install the latest binary to `~/.local/bin`.

### Using pip/uv

```bash
# Using pip
pip install phiton

# Using uv (recommended)
uv pip install phiton
```

### Using precompiled binaries

Download the appropriate binary for your platform from the [latest release](https://github.com/twardoch/phiton/releases/latest):

- **Linux**: `phiton-ubuntu-latest`
- **Windows**: `phiton-windows-latest.exe`
- **macOS**: `phiton-macos-latest`

Make the binary executable and run:

```bash
# Linux/macOS
chmod +x phiton-ubuntu-latest
./phiton-ubuntu-latest --help

# Windows
phiton-windows-latest.exe --help
```

## Detailed Installation Methods

### 1. Install Script Options

The install script supports several options:

```bash
# Install to specific directory
curl -sSf https://raw.githubusercontent.com/twardoch/phiton/main/install.sh | bash -s -- --dir /usr/local/bin

# Install specific version
curl -sSf https://raw.githubusercontent.com/twardoch/phiton/main/install.sh | bash -s -- --version v1.0.0

# Don't add to PATH
curl -sSf https://raw.githubusercontent.com/twardoch/phiton/main/install.sh | bash -s -- --no-path

# Show help
curl -sSf https://raw.githubusercontent.com/twardoch/phiton/main/install.sh | bash -s -- --help
```

### 2. Manual Binary Installation

1. Go to the [releases page](https://github.com/twardoch/phiton/releases)
2. Download the binary for your platform
3. Move it to a directory in your PATH:

```bash
# Linux/macOS
sudo mv phiton-ubuntu-latest /usr/local/bin/phiton
sudo chmod +x /usr/local/bin/phiton

# Or to user directory
mkdir -p ~/.local/bin
mv phiton-ubuntu-latest ~/.local/bin/phiton
chmod +x ~/.local/bin/phiton
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Development Installation

For development or to get the latest features:

```bash
# Clone the repository
git clone https://github.com/twardoch/phiton.git
cd phiton

# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install
uv venv --python 3.12
source .venv/bin/activate
uv sync

# Install in development mode
uv pip install -e .

# Run tests
./scripts/test.sh

# Build the project
./scripts/build.sh
```

### 4. Docker Installation

```bash
# Build Docker image
docker build -t phiton .

# Run Phiton in container
docker run --rm -v $(pwd):/workspace phiton example.py
```

## Verification

After installation, verify that Phiton is working correctly:

```bash
# Check version
phiton --version

# Test basic functionality
echo "def hello(): print('Hello, world!')" | phiton

# Get help
phiton --help
```

## Platform-Specific Notes

### Linux

The binary is built on Ubuntu and should work on most Linux distributions. If you encounter issues:

1. Ensure glibc is available (most modern distributions include it)
2. Try installing from source using pip/uv
3. Check that the binary has execute permissions

### macOS

The binary is built on the latest macOS runner. For older macOS versions:

1. Try installing from source using pip/uv
2. Ensure you have the latest Xcode command line tools
3. You may need to allow the binary in System Preferences > Security

### Windows

The binary is built for Windows 10/11. For older Windows versions:

1. Try installing from source using pip/uv
2. Ensure you have the latest Microsoft Visual C++ Redistributable
3. Run from Command Prompt or PowerShell

## Troubleshooting

### Common Issues

1. **Command not found**: Make sure the install directory is in your PATH
2. **Permission denied**: Ensure the binary has execute permissions
3. **Version mismatch**: Clear pip cache and reinstall

### Getting Help

- Check the [troubleshooting guide](https://github.com/twardoch/phiton/wiki/Troubleshooting)
- Open an issue on [GitHub](https://github.com/twardoch/phiton/issues)
- Ask questions in [Discussions](https://github.com/twardoch/phiton/discussions)

## Uninstall

### Binary Installation

```bash
# Remove binary
rm ~/.local/bin/phiton  # or wherever you installed it

# Remove from PATH (edit your shell rc file)
# Remove the export PATH line you added
```

### Pip Installation

```bash
pip uninstall phiton
```

### UV Installation

```bash
uv pip uninstall phiton
```