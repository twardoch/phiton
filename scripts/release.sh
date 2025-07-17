#!/bin/bash
# this_file: scripts/release.sh
# 
# Release script for Phiton project
# Creates releases with git tags and uploads to PyPI

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
    echo -e "${BLUE}[RELEASE]${NC} $1"
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

# Function to validate version format
validate_version() {
    local version="$1"
    if [[ ! "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$ ]]; then
        print_error "Invalid version format: $version"
        print_error "Expected format: X.Y.Z or X.Y.Z-suffix (e.g., 1.0.0, 1.0.0-beta1)"
        return 1
    fi
    return 0
}

# Function to check if tag exists
tag_exists() {
    local tag="$1"
    if git tag | grep -q "^${tag}$"; then
        return 0
    else
        return 1
    fi
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS] VERSION"
    echo ""
    echo "Create a release with git tag and optional PyPI upload"
    echo ""
    echo "Arguments:"
    echo "  VERSION       Version number (e.g., 1.0.0, 1.0.0-beta1)"
    echo ""
    echo "Options:"
    echo "  --dry-run     Show what would be done without making changes"
    echo "  --no-pypi     Don't upload to PyPI"
    echo "  --force       Force tag creation even if it exists"
    echo "  --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 1.0.0                    # Create v1.0.0 tag and upload to PyPI"
    echo "  $0 1.0.0-beta1 --no-pypi    # Create v1.0.0-beta1 tag, no PyPI upload"
    echo "  $0 1.0.1 --dry-run          # Show what would be done for v1.0.1"
}

# Parse command line arguments
DRY_RUN=false
NO_PYPI=false
FORCE=false
VERSION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --no-pypi)
            NO_PYPI=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        -*)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            if [ -z "$VERSION" ]; then
                VERSION="$1"
            else
                print_error "Multiple versions specified: $VERSION and $1"
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Check if version is provided
if [ -z "$VERSION" ]; then
    print_error "Version number is required"
    show_help
    exit 1
fi

# Validate version format
if ! validate_version "$VERSION"; then
    exit 1
fi

# Check if we're in the project root
if [ ! -f "pyproject.toml" ]; then
    print_error "This script must be run from the project root directory"
    exit 1
fi

# Check if git is clean
if [ "$DRY_RUN" = false ] && ! git diff --quiet; then
    print_error "Git working directory is not clean. Please commit all changes first."
    exit 1
fi

# Create tag with v prefix
TAG="v$VERSION"

# Check if tag exists
if tag_exists "$TAG"; then
    if [ "$FORCE" = true ]; then
        print_warning "Tag $TAG already exists, will overwrite due to --force"
    else
        print_error "Tag $TAG already exists. Use --force to overwrite or choose a different version."
        exit 1
    fi
fi

# Show what will be done
print_status "Release plan for version $VERSION:"
echo "  - Tag: $TAG"
echo "  - PyPI upload: $([ "$NO_PYPI" = true ] && echo "No" || echo "Yes")"
echo "  - Dry run: $([ "$DRY_RUN" = true ] && echo "Yes" || echo "No")"
echo ""

if [ "$DRY_RUN" = true ]; then
    print_status "DRY RUN - No changes will be made"
    exit 0
fi

# Confirm release
read -p "Proceed with release? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status "Release cancelled"
    exit 0
fi

# Run build and test first
print_status "Running build and test..."
if ! ./scripts/build.sh; then
    print_error "Build failed. Cannot proceed with release."
    exit 1
fi

# Create git tag
print_status "Creating git tag $TAG..."
if [ "$FORCE" = true ]; then
    git tag -f "$TAG" -m "Release $VERSION"
else
    git tag "$TAG" -m "Release $VERSION"
fi

# Push tag to remote
print_status "Pushing tag to remote..."
if [ "$FORCE" = true ]; then
    git push origin "$TAG" --force
else
    git push origin "$TAG"
fi

print_success "Tag $TAG created and pushed successfully!"

# Upload to PyPI if requested
if [ "$NO_PYPI" = false ]; then
    print_status "Uploading to PyPI..."
    
    # Check if twine is available
    if ! uv run twine --version &> /dev/null; then
        print_status "Installing twine..."
        uv add twine
    fi
    
    # Upload to PyPI
    if uv run twine upload dist/* --verbose; then
        print_success "Package uploaded to PyPI successfully!"
    else
        print_error "PyPI upload failed"
        exit 1
    fi
fi

# Show final status
print_success "Release $VERSION completed successfully!"
print_status "GitHub Actions will now:"
print_status "  - Run tests and builds"
print_status "  - Create GitHub release"
print_status "  - Upload release artifacts"

# If not uploaded to PyPI manually, GitHub Actions will handle it
if [ "$NO_PYPI" = true ]; then
    print_status "PyPI upload skipped. You can trigger it manually or let GitHub Actions handle it."
fi