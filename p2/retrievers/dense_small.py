"""Ablation: dense with 100-word chunks instead of 300. Nothing else changes (same model, same 50-word overlap)."""

from p2.retrievers import dense

NEEDS_CLAUDE = False
BASE = "dense"


def build(corpus, cfg):
    return dense.Dense(corpus, cfg.replace(chunk_words=100))
