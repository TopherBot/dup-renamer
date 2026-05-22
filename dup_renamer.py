import argparse
import hashlib
import os
import sys
from pathlib import Path

def file_hash(path: Path, chunk_size: int = 8192) -> str:
    """Return SHA‑256 hash of file contents."""
    h = hashlib.sha256()
    try:
        with path.open('rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                h.update(chunk)
    except OSError as e:
        print(f"[WARN] Unable to read {path}: {e}", file=sys.stderr)
        return ''
    return h.hexdigest()

def find_duplicates(root: Path) -> dict:
    """Return a mapping of hash → list of paths that share that hash (size>1)."""
    hashes = {}
    for path in root.rglob('*'):
        if path.is_file():
            h = file_hash(path)
            if h:
                hashes.setdefault(h, []).append(path)
    # Keep only duplicates
    return {h: paths for h, paths in hashes.items() if len(paths) > 1}

def rename_duplicates(dup_map: dict, suffix: str = '_dup'):
    """Rename all but the first file in each duplicate set.
    Returns a list of (old_path, new_path) tuples.
    """
    renamed = []
    for paths in dup_map.values():
        original = paths[0]
        for dup in paths[1:]:
            new_name = dup.stem + suffix + dup.suffix
            new_path = dup.with_name(new_name)
            counter = 1
            # Ensure we don't clash with existing files
            while new_path.exists():
                new_path = dup.with_name(f"{dup.stem}{suffix}{counter}{dup.suffix}")
                counter += 1
            dup.rename(new_path)
            renamed.append((dup, new_path))
    return renamed

def main():
    parser = argparse.ArgumentParser(description='Detect and optionally rename duplicate files by content hash.')
    parser.add_argument('directory', type=Path, help='Root directory to scan')
    parser.add_argument('--rename', action='store_true', help='Actually rename duplicates')
    parser.add_argument('--suffix', default='_dup', help='Suffix added to renamed files')
    args = parser.parse_args()

    if not args.directory.is_dir():
        print('Error: provided path is not a directory', file=sys.stderr)
        sys.exit(1)

    dup_map = find_duplicates(args.directory)
    if not dup_map:
        print('No duplicates found.')
        return

    print('Duplicate sets found:')
    for h, paths in dup_map.items():
        print(f'Hash {h[:8]}...:')
        for p in paths:
            print(f'  {p}')

    if args.rename:
        renamed = rename_duplicates(dup_map, suffix=args.suffix)
        print('\nRenamed files:')
        for old, new in renamed:
            print(f'{old} → {new}')
    else:
        print('\nRun with --rename to automatically rename duplicates.')

if __name__ == '__main__':
    main()
