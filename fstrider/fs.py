"""Function to work with file system (FS)."""

import os
import shutil
from pathlib import Path


def has_read_access(path):
    """Check that file or dir has read access."""
    return os.access(path, os.R_OK)


def access_type(path):
    """Get access type."""
    p = Path(path)
    p_access = has_read_access(path)
    try:
        p_exists = p.exists()
    except PermissionError:
        p_exists = None

    if p_exists is None:
        return 'noaccess'
    else:
        if p_exists:
            if p_access:
                return 'exist_access'
            else:
                return 'exist_noaccess'
        else:
            return 'notexist'


def create_path_if_needed(path):
    """Create path if it's not exists."""
    if not (path := Path(path)).exists():
        path.mkdir(parents=True, exist_ok=True)

def copy_path(source_path: Path, target_path: str):
    """Copying path."""
    targetp = Path(target_path).expanduser().absolute()
    move = {}
    result = 'unknown'
    if source_path.is_dir():
        if target_path.endswith('/'):
            # If target_path='/target/path/'. Copy `/source/dir` to /target/path/dir`.
            tp = targetp / source_path.name
        else:
            # If target_path='/target/path'. Copy `/source/dir/*` to /target/path/` with replacement.
            tp = targetp

        if tp == source_path:
            move = {
                'p': tp.parent,
                'selected_by_value': tp,
                'file_msg': {tp: 'Copying is not needed'}
            }
        else:
            if tp.exists():
                msg = 'Merged with'
                result = 'merge'
            else:
                msg = 'Copied from'
                result = 'copy'
            create_path_if_needed(tp)
            result_path = shutil.copytree(source_path, tp, dirs_exist_ok=True)
            move = {
                'p': tp.parent,
                'selected_by_value': tp,
                'file_msg': {tp: f'{msg} {source_path}'}
            }
    else:
        if target_path.endswith('/'):
            # If target_path = '/target/path/'. Copy `/source/file` to /target/path/file`.
            tp = targetp / source_path.name
        else:
            # If target_path = '/target/new_filename'. Copy `/source/file` to /target/new_filename`.
            tp = targetp

        if tp == source_path:
            move = {
                'p': tp.parent,
                'selected_by_value': tp,
                'file_msg': {tp: f'Copying is not needed'}
            }
            result = 'nocopy'
        else:
            create_path_if_needed(tp.parent)
            if tp.exists():
                msg = 'Overwritten by'
                result = 'merge'
            else:
                msg = 'Copied from'
                result = 'copy'
            result_path = shutil.copy(source_path, tp)
            move = {
                'p': tp.parent,
                'selected_by_value': tp,
                'file_msg': {tp: f'{msg} {source_path}'}
            }

    return {
        'move': move,
        'result': result
    }