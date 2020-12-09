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
	cache = np.zeros((n, n), dtype=int)
	for i in range(n):
		minj = max(i - preamble_length, 0)
		for j in range(minj, i):
			print(i, j)
			cache[i, j] = sequence[i] + sequence[j]
	print(cache)
	return cache

def is_valid(cache, preamble_length, element_index, element_value):
	
	for i in range(element_index - preamble_length, element_index):
		for j in range(i, i+preamble_length):
			print(cache[i, j])


def main():
	sequence = parse_file("test.txt")
	preamble_length = 5
	cache = pre_compute(sequence, preamble_length)
	is_valid(cache, preamble_length, 5, 62)
if __name__ == '__main__':
	main()