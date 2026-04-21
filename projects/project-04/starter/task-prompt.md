# Task — Project 04: Architecture Decision Debate

## Goal
Use `/autoresearch:predict` to evaluate two architectures and recommend the better one.
The weighted score of the recommended architecture must reach **≥ 0.65**.

## Current State
`arch.py` defines two candidate architectures.
The naive scoring gives monolith ≈ 0.41, microservices ≈ 0.71.

## What to Explore
- Adjust the `ARCHITECTURES` dict to add a third hybrid option
- Refine the weight vector in `evaluate.py` to reflect your team's priorities
- Use the predict command to get 5-expert forecasts for each option

## Metric
`weighted_score` — maximize — target `>= 0.65`

## Expert Perspectives to Simulate
1. Staff SRE — reliability, ops burden
2. Principal engineer — scalability, tech debt
3. Product manager — time-to-market, cost
4. Security engineer — attack surface, blast radius
5. Data engineer — throughput, latency guarantees
