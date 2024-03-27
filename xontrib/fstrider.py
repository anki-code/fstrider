"""Xontrib for Strider."""

from pathlib import Path as _Path
from fstrider.fstrider import fstrider as _fstrider
from shutil import which as _which

__xonsh__._fstrider = None
_cmd = __xonsh__.env.get('XONTRIB_FSTRIDER_ALIAS', "fstrider" if _which("fs") else "fs")

@aliases.register(_cmd)
def _alias_strider(args):
    p = args[0] if args else None
    if __xonsh__._fstrider is None:
        __xonsh__._fstrider = _fstrider(p)
    __xonsh__._fstrider.run('.' if p is None else p)

