"""Xontrib for Strider."""

import strider as _strider

@aliases.register("s")
def _alias_strider(args):
    _strider.main(args)