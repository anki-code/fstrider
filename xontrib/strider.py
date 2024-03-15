from pathlib import Path
import strider

@aliases.register("s")
def _strider():
    strider.main()