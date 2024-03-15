from strider.strider import Strider

@aliases.register("a")
def _strider():
    # argp = argparse.ArgumentParser(description=f"Strider.")
    # argp.add_argument('path', nargs='?', default='.', help="Starting path.")
    # args = argp.parse_args()

    strider = Strider(current_path=Path('.') )
    strider.stride()
    del strider