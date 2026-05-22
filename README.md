# dup‑renamer

A **single‑file** Python tool that scans a folder for duplicate files (hash‑based) and can automatically rename the duplicates to keep only one original.

## Features
- Detect duplicates via SHA‑256 hash.
- Dry‑run mode to preview changes.
- Auto‑rename duplicates with a configurable suffix.
- Zero‑config install: `pip install .`
- CI with GitHub Actions (lint + tests).

## Usage
```bash
# Scan and list duplicates (dry‑run)
python -m dup_renamer /path/to/dir

# Actually rename duplicates
python -m dup_renamer --rename /path/to/dir
```

## Development
```bash
# install dev dependencies
pip install -r requirements-dev.txt

# run tests
pytest
```

## License
MIT © 2026 TopherBot