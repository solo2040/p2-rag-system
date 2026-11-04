"""Ablation: bm25 with the 12 lab's plain tokenizer instead of "codes". Nothing else changes.

"lab" lower-cases and keeps runs of [a-z0-9], so a code such as 1926.652 splits into 1926 and 652;
"codes" keeps it whole and also indexes its parts.
"""

from p2.retrievers import bm25

NEEDS_CLAUDE = False
BASE = "bm25"


def build(corpus, cfg):
    return bm25.BM25(corpus, cfg.replace(tokenizer="lab"))
