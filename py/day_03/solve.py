from collections import namedtuple, Counter
from operator import add, mul
from functools import reduce

class Map:
	def __init__(self, grid):
		self.grid = grid
		self.width = len(grid[0])
		self.height = len(grid)

	def has_tree(self, i, j):
		return self.grid[i][j % self.width] == "#"

def parse_input(filename):
	with open(filename) as file:
		grid = [list(l.strip()) for l in file.readlines()]

	return Map(grid)

def sumt(a, b):
	return tuple(map(sum, zip(a, b)))

def mult(scalar, a):
	return tuple(map(lambda x: mul(scalar, x), a))

def count_trees(mountain, slope):
	initial_point = (0, 0)
	i_step, j_step = slope
	possible_impact_points = [
		sumt(initial_point, mult(i, slope)) 
		for i in range(1, mountain.height // i_step)
	]
	return sum([
		1 for i, j  in possible_impact_points if mountain.has_tree(i, j)
	])


def main():
	mountain = parse_input("input.txt")
	slopes = [
		(1, 1),
		(1, 3),
		(1, 5),
		(1, 7),
		(2, 1)
	]
	tree_counts =  list(map(lambda s: count_trees(mountain, s), slopes))
	print(tree_counts)
	answer = reduce(mul, tree_counts)
	print(answer)


if __name__ == '__main__':
	main()
