"""Xontrib for Strider."""

import strider

@aliases.register("s")
def _strider(args):
    strider.main(args)