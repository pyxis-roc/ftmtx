#!/usr/bin/env python


import featurematrix as fm
import argparse
import json
import sys

def complete_features(mat, ftorder):
    src_completed = 0
    a = []
    for ft, count in ftorder:
        print(ft, count, src_completed)
        a.append(src_completed)

        srcs = mat.complete_feature(ft)

        for s in srcs:
            print("\t", s)

        src_completed += len(srcs)

    if len(a):
        print(sum(a)/len(a))

def complete_sources(mat, srcorder):
    src_completed = 0
    a = []
    for src, wt in srcorder:
        for f in mat.features_for(src):
            print(f, src_completed)
            a.append(src_completed)

        src_completed += 1
        print("\t", src)
        mat.complete_source(src)

    if len(a):
        print(sum(a)/len(a))

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Process a JSON feature matrix file")
    p.add_argument("ftrmatjson", help="A JSON file contain a feature matrix")
    p.add_argument("rank", choices=["features", "sources", "complete_ft", "complete_src"])
    p.add_argument("--cs", dest="completed_sources", help="JSON file containing list of sources whose features have been completed (in same format as feature matrix)")

    args = p.parse_args()

    bg = json.load(open(args.ftrmatjson, "r"))
    mat = fm.FeatureMatrix.from_array(bg)
    g = mat.graph

    print(mat)

    if args.completed_sources:
        with open(args.completed_sources, "r") as f:
            cs = json.load(fp=f)
            mat2 = fm.FeatureMatrix.from_array(cs)

            for f in mat2.features:
                if f in mat.features:
                    mat.complete_feature(f)

    if args.rank == 'features':
        f = mat.rank_features()
        for ft, count in f:
            print(ft, count)
            for s in mat.sources_for(ft):
                print("\t", s)
    elif args.rank == 'sources':
        s = mat.rank_sources()
        for src, count in s:
            print(src, count)
            for f in mat.features_for(src):
                print("\t", f)
    elif args.rank == 'complete_ft':
        f = mat.rank_features()
        complete_features(mat, f)
    elif args.rank == 'complete_src':
        s = reversed(mat.rank_sources())
        complete_sources(mat, s)
