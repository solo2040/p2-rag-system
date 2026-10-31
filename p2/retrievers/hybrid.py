"""Hybrid retriever (stage 1): reciprocal rank fusion of bm25 and dense.

Each item scores the sum of 1 / (RRF_K + rank) over the two rankings, with ranks counted from 1.
Full rankings are fused, not top-10 lists, so an item that is 11th in both can still reach the fused top 10.
"""

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False

RRF_K = 60
PARTS = ("bm25", "dense")


def rrf(rankings, k=RRF_K):
    """Fuse ranked lists of ids into (id, score) pairs, best first."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking, 1):
            scores[item] = scores.get(item, 0.0) + 1 / (k + rank)
    return order(scores.items())


class Hybrid:
    model = None

    def __init__(self, corpus, cfg):
        self.parts = [retrievers.build(name, corpus, cfg) for name in PARTS]
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(self.parts[0].chunks)

    def search(self, text: str, k: int):
        rankings = [[d for d, _ in p.search(text, self.n_docs)] for p in self.parts]
        return rrf(rankings)[:k]

    def search_chunks(self, text: str, k: int):
        rankings = [[c for c, _ in p.search_chunks(text, self.n_chunks)] for p in self.parts]
        return rrf(rankings)[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
