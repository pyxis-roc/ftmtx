# Feature Matrix

A library to encode and operate on binary relations that form a
bipartite graph.

## Installation

This package is in heavy development:

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

## Analyzing a feature matrix

To analyze a feature matrix represented as a JSON file, use the
`ftmtx.py` script.

```
ftmtx.py ftrmat.json
```

This will print out the features in descending frequency-of-occurrence
order, along with 3 sources that use this feature.
