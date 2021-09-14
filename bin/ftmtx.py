#!/usr/bin/env python


import featurematrix as fm
import argparse
import json

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Process a JSON feature matrix file")
    p.add_argument("ftrmatjson", help="A JSON file contain a feature matrix")
    p.add_argument("rank", choices=["features", "sources", "completion", "completion_src"])
    p.add_argument("--cs", dest="completed_sources", help="JSON file containing list of sources whose features have been completed (in same format as feature matrix)")

    args = p.parse_args()

    bg = json.load(open(args.ftrmatjson, "r"))
    mat = fm.FeatureMatrix.from_array(bg)
    g = mat.graph

    print(mat)

    if args.completed_sources:
        with open(args.completed_sources, "r") as f:
            cs = json.load(fp=f)
            for c in cs:
                print(c['src'])
                mat.complete_source(c['src'])

    if args.rank == 'features':
        f = mat.rank_features()
        for ft, count in f:
            print(ft, count)
            for s in mat.sources_for(ft)[:3]:
                print("\t", s)
    elif args.rank == 'sources':
        s = mat.rank_sources()
        for src, count in s:
            print(src, count)
            for f in mat.features_for(src):
                print("\t", f)
    elif args.rank == 'completion':
        f = mat.rank_features()
        for ft, count in f:
            print(ft, count)
            for s in mat.sources_for(ft):
                if len(mat.features_for(s)) == 1:
                    print("\t", s)

            mat.complete_feature(ft)
    elif args.rank == 'completion_src':
        s = reversed(mat.rank_sources())
        for src, count in s:
            for f in mat.features_for(src):
                print(f)
                mat.complete_feature(f)

            assert mat.is_source_completed(src)
            print("\t", src)
