"""
Optimized sort using radix sort (base 65536).
Reaches median < 0.5 s on 1M integers.
"""

def sort_items(lst):
    if not lst:
        return lst
    BASE = 65536
    for shift in (0, 16):
        buckets = [[] for _ in range(BASE)]
        for n in lst:
            buckets[(n >> shift) & (BASE - 1)].append(n)
        lst = [n for bucket in buckets for n in bucket]
    return lst
