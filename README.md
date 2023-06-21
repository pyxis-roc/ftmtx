# Feature Matrix

A library to encode and operate on binary relations that form a
bipartite graph.

## Installation

This package is in heavy development, so install using `develop`:

```
python3 setup.py develop
```

## Feature matrix background

A feature matrix is a bipartite graph containing a "source" and a
"feature". Both "source" and "feature" are opaque strings to this
library.

The most common way to represent this bipartite graph to encode it as
a JSON file, listing the edges of a source:

```
[
  {
    "src": "source-id-1",
    "features": ["feature1", "feature2", ...]
  },
  ...
```

## Preparing feature matrix files

To prepare a feature matrix JSON file from a flat text file containing
a list of features, use the `txt2features.py` script.

## Combining feature matrix files

Use the `ftmtx_combine.py` script to combine different JSON files into
a single file for analysis.

## Analyzing a feature matrix

To analyze a feature matrix represented as a JSON file, use the
`ftmtx.py` script.

### Feature analysis

```
ftmtx.py ftrmat.json features
```

This will print out the features in descending frequency-of-occurrence
order, along with sources that use this feature.

### Source analysis

```
ftmtx.py ftrmat.json sources
```

This will print out the sources in increasing order of "feature
weight". The feature weight captures the number of sources that also
use the features used by a source.

### Completion analysis

```
ftmtx.py ftrmat.json complete_ft|complete_src
```

These two options will print out a list of features to be implemented
in order to reach "completion" of sources. The `complete_ft` prints
out features in order of increasing frequency. The `complete_src`
prints out features present in sources of high shared weight.

Empirically, the `complete_ft` order of feature completion leads to a
higher number of completed _sources_ in a given amount of time,
compared to `complete_src`.

The `--cs` option provides a feature matrix whose features are deemed
completed.

## Searching feature matrix files

The `ftsearch.py` script allows search feature matrix JSON files for
sources that contain a list of features, including excluding features.


## Copyright

SPDX-FileCopyrightText: 2021,2023 University of Rochester

SPDX-License-Identifier: MIT

