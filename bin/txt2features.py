#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2021,2023 University of Rochester
#
# SPDX-License-Identifier: MIT
#
# SPDX-Contributor: Sreepathi Pai

import argparse
import json

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Convert individual text files to feature maps")
    p.add_argument("--src", dest="source", help="Set name of source, default is feature filename")
    p.add_argument("features", help="File containing features, one per line")
    p.add_argument("output", help="JSON output for ftmtx.py")

    args = p.parse_args()

    if args.source is None:
        args.source = args.features

    features = list(set([x.strip() for x in open(args.features, "r").readlines()]))

    with open(args.output, "w") as f:
        f.write(json.dumps([{'src': args.source,
                             'features': features}], indent='  '))
