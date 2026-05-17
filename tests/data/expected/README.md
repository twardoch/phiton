# Expected Output Files

This directory contains expected output files for Phiton conversion testing.

## File Naming Convention

Files follow this naming pattern:

- `{source_file_name}_level{compression_level}.phi`

Examples:
- `simple_level1.phi`: Output for `simple.py` with compression level 1
- `simple_level5.phi`: Output for `simple.py` with compression level 5

## Adding New Test Cases

1. Create a Python file in the parent directory
2. Run Phiton conversion with the desired compression level
3. Save output here using the naming convention
4. Update tests to reference the new file

## Updating Existing Files

Update expected files when the Phiton algorithm changes:

1. Run conversion on source files with current algorithm
2. Compare new output to existing expected files
3. Replace expected files if changes are intentional