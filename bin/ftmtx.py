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
    p.add_argument("--cs", dest="completed_sources", help="JSON file containing list of sources whose features have been completed (in same format as feature matrix)", action="append", default=[])
    p.add_argument("--csnames", dest="completed_sources_names", help="FILE containing list of completed sources")

    args = p.parse_args()

    bg = json.load(open(args.ftrmatjson, "r"))
    mat = fm.FeatureMatrix.from_array(bg)
    g = mat.graph

    print(mat)

    completed = set()
    if args.completed_sources:
        for csf in args.completed_sources:
            with open(csf, "r") as f:
                cs = json.load(fp=f)
                mat2 = fm.FeatureMatrix.from_array(cs)

                for f in mat2.features:
                    if f in mat.features:
                        b = mat.complete_feature(f)
                        completed |= set(b)
                        for bb in b:
                            print("\t", bb)
        print("===")
        print(mat)

    if args.completed_sources_names:
        with open(args.completed_sources_names, "r") as f:
            for l in f:
                ls = l.strip()
                if ls != '':
                    if ls not in mat.sources:
                        print("WARNING: {ls} not found")
                    else:
                        mat.complete_source(ls)
                        completed.add(ls)

        print("===")
        print(mat)


    if args.rank == 'features':
        f = mat.rank_features()
        for ft, count in f:
            print(ft, count)
            for i, s in enumerate(mat.sources_for(ft)):
                print("\t", s)
                if i > 10: break

    elif args.rank == 'sources':
        s = mat.rank_sources()
        for src, count in s:
            if src not in completed:
                print(src, count)
                for f in mat.features_for(src):
                    print("\t", f)
    elif args.rank == 'complete_ft':
        f = mat.rank_features()
        complete_features(mat, f)
    elif args.rank == 'complete_src':
        s = reversed(mat.rank_sources())
        complete_sources(mat, s)
