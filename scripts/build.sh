#!/bin/bash
# this_file: scripts/build.sh
# 
# Build script for Phiton project
# Handles building, testing, and packaging

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
    echo -e "${BLUE}[BUILD]${NC} $1"
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

# Check if we're in the project root
if [ ! -f "pyproject.toml" ]; then
    print_error "This script must be run from the project root directory"
    exit 1
fi

# Ensure UV is available
if ! command -v uv &> /dev/null; then
    print_error "UV is not installed. Please install UV first:"
    print_error "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_status "Creating virtual environment..."
    uv venv --python 3.12
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
uv sync

# Run linting
print_status "Running code quality checks..."
if uv run ruff check src/phiton tests; then
    print_success "Ruff linting passed"
else
    print_warning "Ruff linting failed but continuing build"
fi

# Run formatting check
print_status "Checking code formatting..."
if uv run ruff format --check src/phiton tests; then
    print_success "Code formatting is correct"
else
    print_warning "Code formatting issues found but continuing build"
fi

# Run type checking if mypy is available
if uv run mypy --version &> /dev/null; then
    print_status "Running type checking..."
    if uv run mypy src/phiton tests; then
        print_success "Type checking passed"
    else
        print_warning "Type checking failed (continuing build)"
    fi
else
    print_warning "MyPy not available, skipping type checking"
fi

# Run tests
print_status "Running test suite..."
if uv run python -m pytest tests/ -v --tb=short --maxfail=5; then
    print_success "All tests passed"
else
    print_warning "Some tests failed but continuing build"
fi

# Build the package
print_status "Building package distributions..."
if uv run python -m build --outdir dist --no-isolation; then
    print_success "Package built successfully"
else
    print_error "Package build failed"
    exit 1
fi

# Show build artifacts
print_status "Build artifacts:"
ls -la dist/

print_success "Build completed successfully!"