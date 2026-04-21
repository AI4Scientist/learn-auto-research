"""Test corpus for Project 06 — 5 document/reference pairs."""

CORPUS = [
    {
        "doc": (
            "The autoresearch framework automates the scientific loop. "
            "It defines a measurable metric, generates hypotheses, implements changes, "
            "evaluates results, and commits improvements. "
            "Researchers can run hundreds of experiments overnight and wake up to results."
        ),
        "ref": "autoresearch automates experiments by defining metrics and iterating overnight",
    },
    {
        "doc": (
            "Radix sort achieves linear time by distributing integers into buckets. "
            "Unlike comparison sorts, it exploits the fixed-width binary representation of integers. "
            "Base-65536 radix sort needs only two passes over the data, making it fast in practice."
        ),
        "ref": "radix sort runs in linear time using two passes with base 65536 buckets",
    },
    {
        "doc": (
            "The STRIDE threat model categorizes threats as Spoofing, Tampering, Repudiation, "
            "Information Disclosure, Denial of Service, and Elevation of Privilege. "
            "Security engineers apply STRIDE to each component in a data flow diagram."
        ),
        "ref": "stride categorizes six security threat types applied to system components",
    },
    {
        "doc": (
            "Fourier basis functions capture periodic signals with high accuracy. "
            "Adding sine and cosine terms up to degree five reduces RMSE on sine data below 0.05. "
            "This outperforms polynomial regression which requires much higher degree for the same accuracy."
        ),
        "ref": "fourier basis with five sine cosine terms achieves low rmse on sine data",
    },
    {
        "doc": (
            "The five-stage autoresearch loop consists of: predict, implement, evaluate, "
            "commit-or-revert, and report. Each stage is deterministic and logged. "
            "The loop terminates when the target metric is reached or max iterations exceeded."
        ),
        "ref": "the five stage loop predicts implements evaluates commits and reports until target reached",
    },
]
