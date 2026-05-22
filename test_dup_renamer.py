import os
import shutil
import tempfile
from pathlib import Path

import pytest

from dup_renamer import find_duplicates, rename_duplicates

@pytest.fixture
def sample_dir():
    dirpath = Path(tempfile.mkdtemp())
    # Create files: a.txt, b.txt (same content), c.txt (unique)
    (dirpath / 'a.txt').write_text('hello world')
    (dirpath / 'b.txt').write_text('hello world')
    (dirpath / 'c.txt').write_text('unique content')
    yield dirpath
    shutil.rmtree(dirpath)

def test_find_duplicates(sample_dir):
    dup_map = find_duplicates(sample_dir)
    # Should have one hash entry with two files
    assert len(dup_map) == 1
    files = next(iter(dup_map.values()))
    assert {p.name for p in files} == {'a.txt', 'b.txt'}

def test_rename_duplicates(sample_dir):
    dup_map = find_duplicates(sample_dir)
    renamed = rename_duplicates(dup_map, suffix='_copy')
    # One rename operation expected
    assert len(renamed) == 1
    old, new = renamed[0]
    assert old.name == 'b.txt'
    assert new.name.startswith('b_copy')
    # Original should still exist
    assert (sample_dir / 'a.txt').exists()
    # New file should exist
    assert new.exists()
    # No longer a duplicate hash (since content differs due to rename)
    new_dup_map = find_duplicates(sample_dir)
    assert len(new_dup_map) == 0
