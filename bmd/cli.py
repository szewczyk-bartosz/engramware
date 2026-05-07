import argparse
from tabnanny import check

import bmd.parser
import bmd.pipeline


def main():
    parser = argparse.ArgumentParser(description="Compile a .bmd file to HTML")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", metavar="FILE", help="validate a .bmd file and exit")
    mode.add_argument("-i", metavar="FILE", help="input .bmd file")
    parser.add_argument("-o", metavar="FILE", help="output HTML file")
    parser.add_argument("--engram", action="store_true", help="engram mode")
    args = parser.parse_args()

    if args.check:
        bmd.pipeline.verify(args.check)
        return

    if not args.o:
        parser.error("-o is required when using -i")

    if args.engram:
        bmd.pipeline.compile_engram(args.i, args.o)
        return

    bmd.pipeline.compile(args.i, args.o)


if __name__ == "__main__":
    main()
