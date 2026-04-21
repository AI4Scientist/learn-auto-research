"""
Sort function — starter implementation.
Goal: reduce execution time to under 0.5s on 1M integers.
Do NOT modify the function signature or return type.
"""
import random


def sort_numbers(numbers: list[int]) -> list[int]:
    """Sort a list of integers. Currently uses recursive quicksort."""
    if len(numbers) <= 1:
        return numbers
    pivot = numbers[len(numbers) // 2]
    left = [x for x in numbers if x < pivot]
    middle = [x for x in numbers if x == pivot]
    right = [x for x in numbers if x > pivot]
    return sort_numbers(left) + middle + sort_numbers(right)


if __name__ == "__main__":
    data = [random.randint(0, 10_000_000) for _ in range(1_000_000)]
    result = sort_numbers(data)
    print(f"Sorted {len(result)} integers")
    print(f"First 5: {result[:5]}")
    print(f"Last 5:  {result[-5:]}")
