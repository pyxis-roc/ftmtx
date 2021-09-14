import networkx as nx

class FeatureMatrix:
    """Implements an in-memory feature matrix"""

    def __init__(self):
        self.src2nid = {}
        self.ft2nid = {}
        self.edges = set()

        self.nid2src = {}
        self.nid2ft = {}

        self._nid = 0
        self._g = None

    def add_source(self, source):
        if source not in self.src2nid:
            self._nid +=1
            self.src2nid[source] = self._nid
            self.nid2src[self._nid] = source

        return self.src2nid[source]

    def add_feature(self, feature):
        if feature not in self.ft2nid:
            self._nid += 1
            self.ft2nid[feature] = self._nid
            self.nid2ft[self._nid] = feature

        return self.ft2nid[feature]

    def add_edge(self, source, feature):
        s = self.add_source(source)
        f = self.add_feature(feature)

        self.edges.add((s, f))

    def sources_for(self, feature):
        g = self.graph
        return [self.nid2src[x] for x in g.predecessors(self.ft2nid[feature])]

    def rank_features(self, ranking='degree'):
        g = self.graph
        fn = []
        # for n in g.nodes():
        #     if g.in_degree[n] > 0:
        #         if n not in self.nid2ft:
        #             import pdb
        #             pdb.set_trace()
        #         else:
        #             fn.append((self.nid2ft[n], g.in_degree[n]))

        fn = [(self.nid2ft[n], g.in_degree[n]) for n in g.nodes() if g.in_degree[n] > 0]
        return sorted(fn, key=lambda x: x[1], reverse=True)

    @property
    def graph(self):
        if self._g is None:
            self._g = nx.DiGraph()
            self._g.add_edges_from(self.edges)

        return self._g

    def __str__(self):
        return f"FeatureMatrix(sources={len(self.src2nid)}, features={len(self.ft2nid)}, relations={len(self.edges)})"

    __repr__ = __str__

    @staticmethod
    def from_array(a):
        x = FeatureMatrix()

        sc = 0
        fc = 0

        for l in a:
            for f in l['features']:
                x.add_edge(l['src'], f)

        return x
