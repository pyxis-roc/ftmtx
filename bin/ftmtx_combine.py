#!/usr/bin/env python

import argparse
import json
import sys

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Combine JSON feature matrix files")
    p.add_argument("ftrmatjson", nargs="+", help="A JSON file contain a feature matrix")
    p.add_argument("-o", dest="output", help="Output JSON file")

    args = p.parse_args()
    out = []

    for f in args.ftrmatjson:
        bg = json.load(open(f, "r"))
        out.extend(bg)

    if args.output is None:
        o = sys.stdout
    else:
        o = open(args.output, "w")

    json.dump(out, fp=o, indent=2)
