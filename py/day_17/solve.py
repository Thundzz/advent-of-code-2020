import numpy as np
from functools import reduce, lru_cache
from itertools import product

def to_int(c):
    return 1 if c == "#" else 0

def parse_file(filename):
    with open(filename) as file:
        m = [list(map(to_int , list(l.strip()))) for l in file.readlines()]

    return np.matrix(m)

def distance(coords, o_coords):
    diffs = map(lambda x1, x2: abs(x1 - x2), coords, o_coords)
    return max(diffs)

def sumt(t1, t2):
    return list(map(lambda x: x[0] + x[1], zip(t1, t2)))

def get_offsets_3d():
    return [
        off for off in product([-1, 0, 1], repeat=3)
        if distance(off, (0, 0, 0)) == 1
    ]

def get_offsets_4d():
    return [
        off for off in product([-1, 0, 1], repeat=4)
        if distance(off, (0, 0, 0, 0)) == 1
    ]

@lru_cache(maxsize=100000)
def get_neighbours_3d(i, j, k):
    offsets = get_offsets_3d()
    return [ sumt((i, j, k), offset) for offset in offsets ]

@lru_cache(maxsize=10000000)
def get_neighbours_4d(i, j, k, l):
    """
    ALLOCATE ALL THE MEMORIES
    """
    offsets = get_offsets_4d()
    return [ sumt((i, j, k, l), offset) for offset in offsets ]

def next_state(current_state, nb_neighbors):
    if current_state == 1:
        if nb_neighbors == 2 or nb_neighbors == 3:
            return 1
        else:
            return 0
    else:
        if nb_neighbors == 3:
            return 1
        else:
            return 0

def count_active_neighbours_3d(m, i, j, k):
    neighs = get_neighbours_3d(i, j, k)
    return len([1 for ii, jj, kk in neighs if m[ii, jj, kk] == 1])

def count_active_neighbours_4d(m, i, j, k, l):
    neighs = get_neighbours_4d(i, j, k, l)
    return len([1 for ii, jj, kk, ll in neighs if m[ii, jj, kk, ll] == 1])


def next_3d(matrix):
    new = matrix.copy()
    n = matrix.shape[0]
    for i in range(1, n-1):
        for j in range(1, n-1):
            for k in range(1, n-1):
                active_neighs = count_active_neighbours_3d(matrix, i, j, k)
                new[i, j, k] = next_state(matrix[i, j, k], active_neighs)
    return new

def next_4d(matrix):
    new = matrix.copy()
    n = matrix.shape[0]
    cnt = 0
    to_update = set()

    for i in range(1, n-1):
        for j in range(1, n-1):
            for k in range(1, n-1):
                for l in range(1, n-1):
                    if matrix[i, j, k, l] == 1:
                        to_update.add((i, j, k, l))
                        for (ii, jj, kk, ll) in get_neighbours_4d(i, j, k, l):
                            to_update.add((ii, jj, kk, ll))

    for i, j, k, l in to_update:
        active_neighs = count_active_neighbours_4d(matrix, i, j, k, l)
        new[i, j, k, l] = next_state(matrix[i, j, k, l], active_neighs)
    return new

def main():
    m = parse_file("input.txt")
    n = m.shape[0]
    size = n + 15
    matrix = np.zeros((size, size, size))
    mid = size // 2
    mini = size//2- n//2
    maxi = (size//2)+ n//2 + (1 if n % 2 == 1 else 0)
    matrix[mid, mini:maxi, mini:maxi] = m
    for i in range(6):
        matrix = next_3d(matrix)

    print(np.count_nonzero(matrix == 1))

    size = n + 14
    matrix = np.zeros((size, size, size, size))
    mid = size // 2
    mini = size//2- n//2
    maxi = (size//2)+ n//2 + (1 if n % 2 == 1 else 0)
    matrix[mid, mid, mini:maxi, mini:maxi] = m

    for i in range(6):
        matrix = next_4d(matrix)
    print(np.count_nonzero(matrix == 1))

if __name__ == '__main__':
    main()
