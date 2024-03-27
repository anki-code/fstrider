from pathlib import Path
from fstrider.fstrider import fstrider

def test_fstrider_init():
    fs = fstrider()
    assert fs.current_path == Path('.').absolute()
