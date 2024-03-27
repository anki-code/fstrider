"""Xontrib for Strider."""

import fstrider as _fstrider
from shutil import which as _which

_cmd = __xonsh__.env.get('XONTRIB_FSTRIDER_ALIAS', "fstrider" if _which("fs") else "fs")

@aliases.register(_cmd)
def _alias_strider(args):
    _fstrider.main(args)
