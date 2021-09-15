#!/usr/bin/env python3

import featurematrix as fm
import argparse
import json
import sys

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Search a JSON feature matrix file")
    p.add_argument("ftrmatjson", help="A JSON file contain a feature matrix")
    p.add_argument("features", nargs="+", help="Search for sources with features, prefix ^ to exclude features")


    args = p.parse_args()

    bg = json.load(open(args.ftrmatjson, "r"))
    mat = fm.FeatureMatrix.from_array(bg)
    g = mat.graph

    has_pf = set()
    has_nf = set()
    for f in args.features:
        negate = f[0] == '^'
        if negate: f = f[1:]

        if f not in mat.features:
            print(f"ERROR: Feature {f} does not exit")

            sys.exit(1)

        srcs = mat.sources_for(f)

        if negate:
            has_nf = has_nf | set(srcs)
        else:
            has_pf = has_pf | set(srcs)

    srcs = has_pf - has_nf

    srcs = sorted(srcs, key=lambda x: mat.graph.out_degree(x))

    for s in srcs:
        print(s, mat.graph.out_degree(s))
