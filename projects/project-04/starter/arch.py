"""
Project 04: Architecture Decision Debate starter.
Two candidate architectures for a high-throughput event pipeline.
The loop uses /autoresearch:predict to score them across 5 expert perspectives.
"""

ARCHITECTURES = {
    "monolith": {
        "description": "Single process, in-memory queue, SQLite persistence",
        "throughput_rps": 1_200,
        "p99_latency_ms": 45,
        "ops_complexity": "low",
        "horizontal_scale": False,
        "fault_isolation": False,
    },
    "microservices": {
        "description": "3 services: ingest, process, store; Kafka queue; PostgreSQL",
        "throughput_rps": 18_000,
        "p99_latency_ms": 12,
        "ops_complexity": "high",
        "horizontal_scale": True,
        "fault_isolation": True,
    },
}


def score_architecture(name: str) -> dict:
    """Return a naive score dict for one architecture."""
    arch = ARCHITECTURES[name]
    return {
        "name": name,
        "throughput_score": min(arch["throughput_rps"] / 20_000, 1.0),
        "latency_score": max(1.0 - arch["p99_latency_ms"] / 100, 0.0),
        "ops_score": 1.0 if arch["ops_complexity"] == "low" else 0.3,
        "scale_score": 1.0 if arch["horizontal_scale"] else 0.0,
        "resilience_score": 1.0 if arch["fault_isolation"] else 0.0,
    }


def weighted_total(scores: dict, weights: dict) -> float:
    return sum(scores[k] * weights.get(k, 0) for k in scores if k != "name")
