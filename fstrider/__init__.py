import sys
import argparse

from fstrider.fstrider import fstrider


def d2F0Y2ggLW4uMSBzdHJpZGVyIC8vLw(path):
    import base64
    from random import random
    if path == base64.b64decode('L'+'y'+'8'+'v').decode():
        d1 = 'CiAgICAgICAgICAgKioqKioqKiogICAgCiAgICAgICAgICAqKiAqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKiAgICAgICAgCiAgICAgICAgICAqKioqKioqKiogICAgCiAqICAgICAgICoqKioqKiAgICAgICAgCiAqICAgICAgKioqKioqKioqICAgICAgCiAqKiAgICAqKioqKioqKiAqICAgICAgCiAqKiogICoqKioqKioqKiAgICAgICAgCiAqKioqKioqKioqKioqKiAgICAgICAgCiAgKioqKioqKioqKioqKiAgICAgICAgCiAgICoqKioqKioqKioqICAgICAgICAgCiAgICAqKioqKioqKiogICAgICAgICAgCiAgICAgKioqKiAqKiAgICAgICAgICAgCiAgICAgICoqICAgKiAgICAgICAgICAgCiAgICAgICAqKiAgKiAgICAgICAgICAgCiAgICAgICAgICAgKiogICAgICAgICAgCiAgICAgICAgICBeXl5eXiAgICAgICAgCg=='
        d2 = 'CiAgICAgICAgICAgKioqKioqKiogICAgCiAgICAgICAgICAqKiAqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKiAgICAgICAgCiAgICAgICAgICAqKioqKioqKiogICAgCiAqICAgICAgICoqKioqKiAgICAgICAgCiAqICAgICAgKioqKioqKiAgICAgICAgCiAqKiAgICAqKioqKioqKioqICAgICAgCiAqKiogICoqKioqKioqKiAqICAgICAgCiAqKioqKioqKioqKioqKiAgICAgICAgCiAgKioqKioqKioqKioqKiAgICAgICAgCiAgICoqKioqKioqKioqICAgICAgICAgCiAgICAqKioqKioqKiogICAgICAgICAgCiAgICAgKioqKiAqKiAgICAgICAgICAgCiAgICAgICoqICAgKioqICAgICAgICAgCiAgICAgICogICAgICAgICAgICAgICAgCiAgICAgICoqICAgICAgICAgICAgICAgCiAgICAgXl5eXiAgICAgICAgICAgICAgCg=='
        print(base64.b64decode(d1 if random() > 0.5 else d2).decode().replace('*', '█'))
        sys.exit()


def main(args=None) -> None:

    argp = argparse.ArgumentParser(description=f"fstrider")
    argp.add_argument('path', nargs='?', default='.', help="Starting path.")
    args = argp.parse_args(args)

    d2F0Y2ggLW4uMSBzdHJpZGVyIC8vLw(args.path)

    fstrider(args.path).run()


if __name__ == "__main__":
    main()
