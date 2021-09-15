import networkx as nx

class FeatureMatrix:
    """Implements an in-memory feature matrix"""

    def __init__(self):
        self._nid = 0
        self._g = nx.DiGraph()
        self.sources = set()
        self.features = set()

    @property
    def graph(self):
        return self._g

    def add_source(self, source):
        self.sources.add(source)
        self.graph.add_node(source, type='source')

    def add_feature(self, feature):
        self.features.add(feature)
        self.graph.add_node(feature, type='feature')

    def add_edge(self, source, feature):
        self.add_source(source)
        self.add_feature(feature)

        self.graph.add_edge(source, feature)

    def _get_src_node(self, src):
        g = self.graph
        assert g.nodes[src]['type'] == 'source'
        return src

    def _get_feature_node(self, feature):
        g = self.graph
        assert g.nodes[feature]['type'] == 'feature'
        return feature

    def is_source_completed(self, src):
        """Check if all features a source requires are completed"""

        src = self._get_src_node(src)
        return g.out_degree(src) == 0

    def unique_features(self, src):
        """Return the number of features that are unique to src.

        Shared features are then out_degree(src) - unique_features"""

        g = self.graph
        src = self._get_src_node(src)

        u = 0
        for p in g.successors(src):
            assert g.node[p]['type'] == 'feature', f"Inconsistent graph: not a feature node {p}"

            if g.in_degree(p) == 1:
                u += 1

        return u

    def feature_wt(self, feature):
        """A feature's weight is the number of sources it is connected to.

        Ranges from 1 to N where the graph has 2N nodes."""

        g = self.graph
        feature = self._get_feature_node(feature)

        return g.in_degree(feature)

    def shared_feature_wt(self, src):
        """Return the weight of shared features.

        The higher the weight, the more nodes share a feature"""

        g = self.graph
        src = self._get_src_node(src)

        wt = 0
        for p in g.successors(src):
            assert g.nodes[p]['type'] == 'feature', f"Inconsistent graph: not a feature node {p}"

            wt += self.feature_wt(p) - 1

        return wt

    def complete_source(self, src):
        g = self.graph
        src = self._get_src_node(src)
        succ = list(g.successors(src))

        for f in succ:
            self.complete_feature(f, get_completed = False)

    def complete_feature(self, feature, get_completed = True):
        g = self.graph
        feature = self._get_feature_node(feature)

        completed = None
        if get_completed:
            completed = []
            for src in g.predecessors(feature):
                if g.out_degree(src) == 1:
                    completed.append(src)

        self.features.remove(feature)
        g.remove_node(feature)
        return completed

    def sources_for(self, feature):
        return self.graph.predecessors(self._get_feature_node(feature))

    def features_for(self, src):
        return self.graph.successors(self._get_src_node(src))

    def rank_sources(self, ranking='weight'):
        g = self.graph

        if ranking == 'weight':
            out = []
            for n in self.sources:
                assert g.nodes[n]['type'] == 'source'
                weight = self.shared_feature_wt(n)
                out.append((n, weight))
        elif ranking == 'degree':
            out = []
            for n in self.sources:
                assert g.nodes[n]['type'] == 'source'
                out.append((n, g.out_degree(n)))
        else:
            raise NotImplementedError(f"Ranking {ranking} is not implemented.")

        out = sorted(out, key=lambda x: x[1])
        return out

    def rank_features(self, ranking='degree'):
        g = self.graph
        fn = []

        if ranking == 'degree':
            fn = [(n, self.feature_wt(n)) for n in self.features]
            fn = sorted(fn, key=lambda x: x[1], reverse=True)
        else:
            raise NotImplementedError(f"Ranking {ranking} is not implemented.")

        return fn

    @property
    def graph(self):
        return self._g

    def __str__(self):
        return f"FeatureMatrix(sources={len(self.sources)}, features={len(self.features)}, relations={self.graph.size()})"

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
