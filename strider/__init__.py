import sys
import argparse

from strider.strider import Strider


def d2F0Y2ggLW4uMSBzdHJpZGVyIC8vLw(path):
    import base64
    from random import random
    if path == base64.b64decode('L'+'y'+'8'+'v').decode():
        d1 = 'CiAgICAgICAgICAgKioqKioqKiogICAgCiAgICAgICAgICAqKiAqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKiAgICAgICAgCiAgICAgICAgICAqKioqKioqKiogICAgCiAqICAgICAgICoqKioqKiAgICAgICAgCiAqICAgICAgKioqKioqKioqICAgICAgCiAqKiAgICAqKioqKioqKiAqICAgICAgCiAqKiogICoqKioqKioqKiAgICAgICAgCiAqKioqKioqKioqKioqKiAgICAgICAgCiAgKioqKioqKioqKioqKiAgICAgICAgCiAgICoqKioqKioqKioqICAgICAgICAgCiAgICAqKioqKioqKiogICAgICAgICAgCiAgICAgKioqKiAqKiAgICAgICAgICAgCiAgICAgICoqICAgKiAgICAgICAgICAgCiAgICAgICAqKiAgKiAgICAgICAgICAgCiAgICAgICAgICAgKiogICAgICAgICAgCiAgICAgICAgICBeXl5eXiAgICAgICAgCg=='
        d2 = 'CiAgICAgICAgICAgKioqKioqKiogICAgCiAgICAgICAgICAqKiAqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKiAgICAgICAgCiAgICAgICAgICAqKioqKioqKiogICAgCiAqICAgICAgICoqKioqKiAgICAgICAgCiAqICAgICAgKioqKioqKiAgICAgICAgCiAqKiAgICAqKioqKioqKioqICAgICAgCiAqKiogICoqKioqKioqKiAqICAgICAgCiAqKioqKioqKioqKioqKiAgICAgICAgCiAgKioqKioqKioqKioqKiAgICAgICAgCiAgICoqKioqKioqKioqICAgICAgICAgCiAgICAqKioqKioqKiogICAgICAgICAgCiAgICAgKioqKiAqKiAgICAgICAgICAgCiAgICAgICoqICAgKioqICAgICAgICAgCiAgICAgICogICAgICAgICAgICAgICAgCiAgICAgICoqICAgICAgICAgICAgICAgCiAgICAgXl5eXiAgICAgICAgICAgICAgCg=='
        print(base64.b64decode(d1 if random() > 0.5 else d2).decode().replace('*', '█'))
        sys.exit()


def main() -> None:

    argp = argparse.ArgumentParser(description=f"Strider.")
    argp.add_argument('path', nargs='?', default='.', help="Starting path.")
    args = argp.parse_args()

    d2F0Y2ggLW4uMSBzdHJpZGVyIC8vLw(args.path)

    Strider(args.path)


if __name__ == "__main__":
    main()