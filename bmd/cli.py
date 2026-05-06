import argparse

import bmd.pipeline


def main():
    parser = argparse.ArgumentParser(description="Compile a .bmd file to HTML")
    parser.add_argument("-i", required=True, metavar="FILE", help="input .bmd file")
    parser.add_argument("-o", required=True, metavar="FILE", help="output HTML file")
    args = parser.parse_args()
    bmd.pipeline.compile(args.i, args.o)


if __name__ == "__main__":
    main()
