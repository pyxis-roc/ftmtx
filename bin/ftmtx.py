#!/usr/bin/env python


import featurematrix as fm
import argparse
import json

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Process a JSON feature matrix file")
    p.add_argument("ftrmatjson", help="A JSON file contain a feature matrix")

    args = p.parse_args()

    bg = json.load(open(args.ftrmatjson, "r"))
    mat = fm.FeatureMatrix.from_array(bg)
    g = mat.graph
    print(mat)
    f = mat.rank_features()
    for ft, count in f:
        print(ft, count)
        for s in mat.sources_for(ft)[:3]:
            print("\t", s)
