import os
from pathlib import Path
from fstrider.fstrider import fstrider


def test_init():
    fs = fstrider()
    assert fs.current_path == Path('.').absolute()


def test_env():
    os.environ["FSTRIDER_OS_PATH_CHANGE"] = 'False'
    fs = fstrider()
    assert fs.env['os_path_change'] is False

    os.environ["FSTRIDER_OS_PATH_CHANGE"] = 'True'
    fs = fstrider()
    assert fs.env['os_path_change'] is True
