import numpy as np

def parse_file(filename):
    with open(filename) as file:
        return list(map(int, file.readlines()))

def pre_compute(sequence, preamble_length):
    """
    This could be done on the fly row by row, which would be more efficient.
    It's much more convenient though to just precompute everything first
    """
    n = len(sequence)
    cache = np.zeros((n, n), dtype="int64")
    for i in range(n):
        minj = max(i - preamble_length, 0)
        for j in range(minj, i):
            cache[i, j] = sequence[i] + sequence[j]
    return cache

def is_valid(cache, preamble_length, element_index, element_value):
    for i in range(element_index - preamble_length, element_index):
        minj = max(i - preamble_length, 0)
        for j in range(minj, i):
            if cache[i, j] == element_value:
                return True
    return False

def find_invalid(sequence, preamble_length):
    cache = pre_compute(sequence, preamble_length)
    for idx, elem in list(enumerate(sequence))[preamble_length+1:]:
        iv = is_valid(cache, preamble_length, idx, elem)
        if not iv:
            return elem

def bruteforce_range(sequence, target):
    """
    Again not my proudest achievement, it's obviously not optimized enough...
    But at least I have my second gold star and can go to sleep :)
    """
    n = len(sequence)
    for start in range(n):
        for length in range(1, n-start):
            if target == sum(sequence[start:start+length]):
                mini = min(sequence[start:start+length])
                maxi = max(sequence[start:start+length])
                return (mini + maxi)

def main():
    sequence = parse_file("input.txt")
    preamble_length = 25
    invalid = find_invalid(sequence, preamble_length)
    print(invalid)
    res = bruteforce_range(sequence, invalid)
    print(res)

if __name__ == '__main__':
    main()