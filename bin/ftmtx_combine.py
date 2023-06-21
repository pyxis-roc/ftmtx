#!/usr/bin/env python
# SPDX-FileCopyrightText: 2021,2023 University of Rochester
#
# SPDX-License-Identifier: MIT
#
# SPDX-Contributor: Sreepathi Pai

import argparse
import json
import sys

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Combine JSON feature matrix files")
    p.add_argument("ftrmatjson", nargs="+", help="A JSON file contain a feature matrix")
    p.add_argument("-o", dest="output", help="Output JSON file")
    p.add_argument("-l", dest="list", action="store_true", help="Input files contain lists of JSON files to be combined")

    args = p.parse_args()
    out = []

    if args.list:
        for f in args.ftrmatjson:
            with open(f, "r") as ff:
                for lf in ff:
                    lf = lf.strip()
                    with open(lf, "r") as flf:
                        bg = json.load(flf)
                        out.extend(bg)
    else:
        for f in args.ftrmatjson:
            bg = json.load(open(f, "r"))
            out.extend(bg)

    if args.output is None:
        o = sys.stdout
    else:
        o = open(args.output, "w")

    json.dump(out, fp=o, indent=2)
