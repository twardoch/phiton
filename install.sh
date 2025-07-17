#!/bin/bash
# this_file: install.sh
# 
# Installation script for Phiton
# Downloads and installs the appropriate binary for the current platform

set -e
set -u

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INSTALL]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to detect platform
detect_platform() {
    case "$(uname -s)" in
        Linux*)     echo "ubuntu-latest";;
        Darwin*)    echo "macos-latest";;
        CYGWIN*|MINGW*|MSYS*) echo "windows-latest";;
        *)          echo "unknown";;
    esac
}

# Function to get latest release info
get_latest_release() {
    local repo="$1"
    curl -s "https://api.github.com/repos/$repo/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/'
}

# Function to download binary
download_binary() {
    local platform="$1"
    local version="$2"
    local repo="$3"
    
    local binary_name="phiton-${platform}"
    if [ "$platform" = "windows-latest" ]; then
        binary_name="${binary_name}.exe"
    fi
    
    local download_url="https://github.com/$repo/releases/download/$version/$binary_name"
    
    print_status "Downloading $binary_name from $download_url"
    
    if ! curl -L -o "$binary_name" "$download_url"; then
        print_error "Failed to download binary"
        return 1
    fi
    
    if [ "$platform" != "windows-latest" ]; then
        chmod +x "$binary_name"
    fi
    
    echo "$binary_name"
}

# Function to install binary
install_binary() {
    local binary_file="$1"
    local install_dir="$2"
    
    # Create install directory if it doesn't exist
    mkdir -p "$install_dir"
    
    # Copy binary to install directory
    cp "$binary_file" "$install_dir/phiton"
    
    # Make sure it's executable
    chmod +x "$install_dir/phiton"
    
    print_success "Binary installed to $install_dir/phiton"
}

# Function to add to PATH
add_to_path() {
    local install_dir="$1"
    local shell_rc
    
    # Determine shell RC file
    if [ -n "${BASH_VERSION:-}" ]; then
        shell_rc="$HOME/.bashrc"
    elif [ -n "${ZSH_VERSION:-}" ]; then
        shell_rc="$HOME/.zshrc"
    else
        shell_rc="$HOME/.profile"
    fi
    
    # Check if already in PATH
    if echo "$PATH" | grep -q "$install_dir"; then
        print_status "Install directory already in PATH"
        return 0
    fi
    
    # Add to PATH in shell RC file
    echo "export PATH=\"$install_dir:\$PATH\"" >> "$shell_rc"
    export PATH="$install_dir:$PATH"
    
    print_success "Added $install_dir to PATH in $shell_rc"
    print_warning "Please restart your shell or run: source $shell_rc"
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Install Phiton binary for your platform"
    echo ""
    echo "Options:"
    echo "  --dir DIR       Install directory (default: ~/.local/bin)"
    echo "  --no-path       Don't add install directory to PATH"
    echo "  --repo REPO     GitHub repository (default: twardoch/phiton)"
    echo "  --version VER   Specific version to install (default: latest)"
    echo "  --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                           # Install latest version to ~/.local/bin"
    echo "  $0 --dir /usr/local/bin      # Install to /usr/local/bin"
    echo "  $0 --version v1.0.0          # Install specific version"
}

# Default values
INSTALL_DIR="$HOME/.local/bin"
ADD_TO_PATH=true
REPO="twardoch/phiton"
VERSION=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dir)
            INSTALL_DIR="$2"
            shift 2
            ;;
        --no-path)
            ADD_TO_PATH=false
            shift
            ;;
        --repo)
            REPO="$2"
            shift 2
            ;;
        --version)
            VERSION="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main installation process
print_status "Starting Phiton installation..."

# Check requirements
if ! command -v curl &> /dev/null; then
    print_error "curl is required but not installed"
    exit 1
fi

# Detect platform
PLATFORM=$(detect_platform)
if [ "$PLATFORM" = "unknown" ]; then
    print_error "Unsupported platform: $(uname -s)"
    exit 1
fi

print_status "Detected platform: $PLATFORM"

# Get version to install
if [ -z "$VERSION" ]; then
    print_status "Getting latest release information..."
    VERSION=$(get_latest_release "$REPO")
    if [ -z "$VERSION" ]; then
        print_error "Failed to get latest release information"
        exit 1
    fi
fi

print_status "Installing version: $VERSION"

# Create temporary directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Download binary
BINARY_FILE=$(download_binary "$PLATFORM" "$VERSION" "$REPO")

# Test binary
print_status "Testing binary..."
if ! ./"$BINARY_FILE" --version &> /dev/null; then
    print_error "Downloaded binary failed to run"
    exit 1
fi

print_success "Binary test passed"

# Install binary
install_binary "$BINARY_FILE" "$INSTALL_DIR"

# Add to PATH if requested
if [ "$ADD_TO_PATH" = true ]; then
    add_to_path "$INSTALL_DIR"
fi

# Clean up
cd /
rm -rf "$TEMP_DIR"

# Final test
print_status "Final installation test..."
if "$INSTALL_DIR/phiton" --version &> /dev/null; then
    print_success "Phiton installed successfully!"
    print_status "Try running: phiton --help"
else
    print_error "Installation test failed"
    exit 1
fi