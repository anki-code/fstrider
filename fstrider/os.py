"""Function to work with operation system (OS)."""

import json
import subprocess
from pathlib import Path
from xonsh.platform import ON_LINUX, ON_DARWIN

def open_in_os(filename: Path, app_name: str = None):
    if app_name:
        return subprocess.call(('open', '-a', app_name, '-F', filename))
    else:
        return subprocess.call(('open', '-F', filename))


def get_os_applications():
    if ON_DARWIN:
        apps = [a.name.replace('.app', '').replace('.pkg', '') for a in Path('/Applications').glob('*') if
                not str(a.name).startswith('.')]
    else:
        raise Exception('Unsupported platform.')

    apps = sorted(apps, key=lambda s: s.lower())
    return apps

def load_app_associations(file):
    """Load file associations."""
    if Path(file).exists():
        with open(file, 'r') as f:
            return json.load(f)
    else:
        return {
            '.py': 'PyCharm CE',
            '.txt': 'kate',
        }

# def open_in_terminal(filename: Path):
#     subprocess.call(('vim', filename))
