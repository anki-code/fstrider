"""Xontrib for Strider."""

import fstrider as _fstrider

@aliases.register("fs")
def _alias_strider(args):
    _fstrider.main(args)