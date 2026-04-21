"""
Correctness tests for sort_numbers.
DO NOT MODIFY — this is the guard file.
"""
import pytest
from sort import sort_numbers


def test_empty():
    assert sort_numbers([]) == []


def test_single():
    assert sort_numbers([42]) == [42]


def test_sorted():
    assert sort_numbers([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_reverse_sorted():
    assert sort_numbers([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_duplicates():
    assert sort_numbers([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]) == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]


def test_negative():
    assert sort_numbers([-3, -1, -4, -1, -5]) == [-5, -4, -3, -1, -1]


def test_mixed():
    assert sort_numbers([-2, 0, 3, -1, 2]) == [-2, -1, 0, 2, 3]


def test_large_correctness():
    import random
    data = [random.randint(-1000, 1000) for _ in range(10000)]
    result = sort_numbers(data)
    assert result == sorted(data)
