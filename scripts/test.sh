#!/bin/bash
# this_file: scripts/test.sh
# 
# Test script for Phiton project
# Runs comprehensive test suite with coverage

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
    echo -e "${BLUE}[TEST]${NC} $1"
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
print_status "Installing test dependencies..."
uv sync

# Parse command line arguments
COVERAGE=${1:-""}
VERBOSE=${2:-""}

if [ "$COVERAGE" = "--coverage" ] || [ "$COVERAGE" = "-c" ]; then
    print_status "Running tests with coverage..."
    uv run python -m pytest tests/ -v --cov=src/phiton --cov=tests --cov-report=term-missing --cov-report=html --cov-report=xml
    print_status "Coverage report generated in htmlcov/"
elif [ "$VERBOSE" = "--verbose" ] || [ "$VERBOSE" = "-v" ]; then
    print_status "Running tests in verbose mode..."
    uv run python -m pytest tests/ -v --tb=long
else
    print_status "Running test suite..."
    uv run python -m pytest tests/ -v --tb=short
fi

# Show test results
if [ $? -eq 0 ]; then
    print_success "All tests passed!"
else
    print_error "Some tests failed!"
    exit 1
fi

# Run benchmark tests if available
if ls tests/test_benchmark.py &> /dev/null; then
    print_status "Running benchmark tests..."
    uv run python -m pytest tests/test_benchmark.py --benchmark-only -v
fi

print_success "Test suite completed successfully!"