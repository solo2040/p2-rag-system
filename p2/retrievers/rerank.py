"""Reranker (stage 1): ask Claude to reorder hybrid's top 20 candidates, one claude -p call per query.

A document is shown as its best chunk in hybrid's chunk ranking, because a whole document is too long to
show twenty of. Claude replies with the passage numbers best first; a reply that is not each number once
keeps hybrid's order and prints a warning. The candidates below the 20 keep their hybrid order underneath.
"""

import sys

from p2 import claude, retrievers
from p2.corpus import docid_of
from p2.runfile import order

NEEDS_CLAUDE = True

CANDIDATES = 20

SCHEMA = {
    "type": "object",
    "properties": {
        "order": {
            "type": "array",
            "items": {"type": "integer", "minimum": 1, "maximum": CANDIDATES},
            "minItems": CANDIDATES,
            "maxItems": CANDIDATES,
        }
    },
    "required": ["order"],
}

PROMPT = """Below are {n} passages from the US federal mine safety and health regulations (30 CFR), numbered 1 to {n}, and a search query.
Order the passages from the most useful for answering the query to the least useful.
Reply with all {n} passage numbers, each exactly once, best first.

Query: {query}

{passages}"""


class Rerank:
    def __init__(self, corpus, cfg):
        self.cfg = cfg
        self.model = cfg.model
        self.first = retrievers.build("hybrid", corpus, cfg)
        self.text = {c.id: c.text for c in self.first.parts[0].chunks}

    def _rerank(self, query, candidates):
        """candidates: [(item id, chunk id)], best first. Returns the item ids in the new order."""
        n = len(candidates)
        passages = "\n\n".join(f"[{i}] {self.text[chunk]}" for i, (_, chunk) in enumerate(candidates, 1))
        prompt = PROMPT.format(n=n, query=query, passages=passages)
        if n != CANDIDATES:  # fewer than 20 candidates exist: the corpus is tiny, keep the order
            return [item for item, _ in candidates]
        reply = claude.call(prompt, SCHEMA, model=self.cfg.model, cache_dir=claude.cache_folder(self.cfg))
        got = reply.output.get("order") if reply.output else None
        if reply.error or not isinstance(got, list) or sorted(got) != list(range(1, n + 1)):
            print(f"WARNING: rerank kept hybrid's order for {query!r}: {reply.error or got}", file=sys.stderr)
            return [item for item, _ in candidates]
        return [candidates[i - 1][0] for i in got]

    def search_chunks(self, text, k):
        ranked = self.first.search_chunks(text, max(k, CANDIDATES))
        top = self._rerank(text, [(c, c) for c, _ in ranked[:CANDIDATES]])
        return _scored(top + [c for c, _ in ranked[CANDIDATES:]])[:k]

    def search(self, text, k):
        n_chunks = self.first.n_chunks
        best = {}  # docid -> its best chunk in hybrid's chunk ranking
        for chunk, _ in self.first.search_chunks(text, n_chunks):
            best.setdefault(docid_of(chunk), chunk)
        ranked = [d for d, _ in self.first.search(text, max(k, CANDIDATES))]
        top = self._rerank(text, [(d, best[d]) for d in ranked[:CANDIDATES]])
        return _scored(top + ranked[CANDIDATES:])[:k]


def _scored(ids):
    """Best first, with descending scores so the order survives ties and rounding."""
    n = len(ids)
    return order((i, (n - rank) / n) for rank, i in enumerate(ids))


def build(corpus, cfg):
    return Rerank(corpus, cfg)
