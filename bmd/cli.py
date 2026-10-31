import argparse
import sys

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

    if args.i and not args.o:
        parser.error("-o is required when using -i")

    try:
        if args.check:
            bmd.pipeline.verify(args.check)
        elif args.engram:
            bmd.pipeline.compile_engram(args.i, args.o)
        else:
            bmd.pipeline.compile(args.i, args.o)
    except bmd.pipeline.BMDError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
