import argparse
import sys

from strider.strider import Strider


def main() -> None:

    argp = argparse.ArgumentParser(description=f"Strider.")
    argp.add_argument('path', nargs='?', default='.', help="Starting path.")
    args = argp.parse_args()

    if args.path == '///':
        import base64
        from random import random
        d1 = 'CiAgICAgICAgICAgKioqKioqKiogICAgCiAgICAgICAgICAqKiAqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKiAgICAgICAgCiAgICAgICAgICAqKioqKioqKiogICAgCiAqICAgICAgICoqKioqKiAgICAgICAgCiAqICAgICAgKioqKioqKioqICAgICAgCiAqKiAgICAqKioqKioqKiAqICAgICAgCiAqKiogICoqKioqKioqKiAgICAgICAgCiAqKioqKioqKioqKioqKiAgICAgICAgCiAgKioqKioqKioqKioqKiAgICAgICAgCiAgICoqKioqKioqKioqICAgICAgICAgCiAgICAqKioqKioqKiogICAgICAgICAgCiAgICAgKioqKiAqKiAgICAgICAgICAgCiAgICAgICoqICAgKiAgICAgICAgICAgCiAgICAgICAqKiAgKiAgICAgICAgICAgCiAgICAgICAgICAgKiogICAgICAgICAgCiAgICAgICAgICBeXl5eXiAgICAgICAgCg=='
        d2 = 'CiAgICAgICAgICAgKioqKioqKiogICAgCiAgICAgICAgICAqKiAqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKioqKioqICAgCiAgICAgICAgICAqKioqKiAgICAgICAgCiAgICAgICAgICAqKioqKioqKiogICAgCiAqICAgICAgICoqKioqKiAgICAgICAgCiAqICAgICAgKioqKioqKiAgICAgICAgCiAqKiAgICAqKioqKioqKioqICAgICAgCiAqKiogICoqKioqKioqKiAqICAgICAgCiAqKioqKioqKioqKioqKiAgICAgICAgCiAgKioqKioqKioqKioqKiAgICAgICAgCiAgICoqKioqKioqKioqICAgICAgICAgCiAgICAqKioqKioqKiogICAgICAgICAgCiAgICAgKioqKiAqKiAgICAgICAgICAgCiAgICAgICoqICAgKioqICAgICAgICAgCiAgICAgICogICAgICAgICAgICAgICAgCiAgICAgICoqICAgICAgICAgICAgICAgCiAgICAgXl5eXiAgICAgICAgICAgICAgCg=='
        print(base64.b64decode(d1 if random() > 0.5 else d2).decode())
        sys.exit(0)

    Strider(args.path)


if __name__ == "__main__":
    main()