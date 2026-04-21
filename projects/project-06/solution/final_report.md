# Final Report — Project 06

## Summary
Starting from a naive first-N-sentences baseline (ROUGE-1 = 0.28), the loop discovered
TF-IDF extractive summarization in 3 iterations, reaching ROUGE-1 = 0.63.

## Key Finding
Position bias (first sentence) only works when documents follow inverted-pyramid structure.
The test corpus uses academic/technical style where key terms appear throughout.
TF-IDF scores sentences by information density, selecting the most content-rich ones
regardless of position.

## Ship Checklist
- [x] evaluate.py passes (score >= 0.60)
- [x] research.md history complete
- [x] final_report.md written
- [x] git log shows clean iteration history
