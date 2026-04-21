"""
Project 06: End-to-End Research Pipeline starter.
A text summarization quality scorer.
Goal: improve ROUGE-1 recall above 0.60 on the test corpus.
"""

def tokenize(text: str) -> list:
    """Simple whitespace tokenizer."""
    return text.lower().split()


def summarize(text: str, max_sentences: int = 2) -> str:
    """Baseline: return the first N sentences."""
    sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
    return ". ".join(sentences[:max_sentences]) + ("." if sentences[:max_sentences] else "")


def rouge1_recall(hypothesis: str, reference: str) -> float:
    """Compute ROUGE-1 recall between hypothesis and reference."""
    hyp_tokens = set(tokenize(hypothesis))
    ref_tokens = set(tokenize(reference))
    if not ref_tokens:
        return 0.0
    overlap = hyp_tokens & ref_tokens
    return len(overlap) / len(ref_tokens)
