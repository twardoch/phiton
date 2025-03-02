# TODO

- [x] Add/update `dev` and `test` extras to `pyproject.toml`, 
- [x] Add/update an `all` extra that includes all dependencies
- [x] clean up `tests` folder
- [x] clean up `src/phiton/` folder, remove unused/unneeded files.

## New Tasks

- [ ] Fix linting issues:
  - [ ] Fix shebang issues (EXE001) - make files executable or remove shebangs
  - [ ] Update deprecated typing imports (UP035) - replace `typing.Dict` with `dict`, etc.
  - [ ] Fix module level imports not at top of file (E402)
  - [ ] Fix boolean-typed positional arguments (FBT001, FBT002) - make them keyword-only
  - [ ] Refactor complex functions (C901) - break down functions with complexity > 10
  - [ ] Fix functions with too many arguments (PLR0913)
  - [ ] Fix functions with too many branches (PLR0912)
  - [ ] Fix functions with too many statements (PLR0915)
  - [ ] Fix functions with too many return statements (PLR0911)
  - [ ] Fix blind exception catching (BLE001) - specify exception types
  - [ ] Fix shadowing of built-in names (A001) - rename variables like `iter` and `type`
  - [ ] Fix unnecessary `elif` after `return` statements (RET505)
  - [x] Add `__init__.py` to tests directory to fix implicit namespace package issues (INP001)
  - [ ] Fix variable naming conventions (N806) - use lowercase for variables

- [x] Fix pytest configuration:
  - [x] Resolve the conflict between pytest.ini and pyproject.toml pytest configuration
  - [ ] Fix the `--cov=phiton` argument (should be `--cov=src/phiton`)

## Completed Tasks

- Added comprehensive dependencies to `dev` and `test` extras in `pyproject.toml`
- Created an `all` extra that includes all dependencies
- Removed redundant requirements.txt from tests folder
- Moved test files (test1.py, test2.py, test_refactored.py, test1.phi) to tests directory
- Created examples directory and moved example files (example.py, example.phi) there
- Removed .DS_Store files
- Added `__init__.py` to tests directory to fix implicit namespace package issues
- Removed redundant pytest.ini file since the configuration is already in pyproject.toml