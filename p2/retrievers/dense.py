"""Dense retriever (stage 1): embed every chunk once, embed the query, and rank chunks by cosine similarity.

The model comes from [dense] model in p2.toml and defaults to bge-small-en-v1.5, the lab's "bge" arm.
Chunk vectors are cached by p2.embed, and every vector has length 1, so one matrix product gives all the cosines.
"""

from p2 import embed
from p2.retrievers import ChunkScorer

NEEDS_CLAUDE = False


class Dense(ChunkScorer):
    def __init__(self, corpus, cfg):
        super().__init__(corpus, cfg)
        self.model = cfg.table("dense").get("model", embed.BGE)
        self.embedder = embed.load(self.model)
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)

    def score_chunks(self, text: str):
        if not len(self.vectors):
            return []
        query = self.embedder.encode([text])[0]
        return self.vectors @ query


def build(corpus, cfg):
    return Dense(corpus, cfg)
