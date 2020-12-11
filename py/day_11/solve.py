import numpy as np
from collections import defaultdict
import json

def next_state(tolerance, state, nb_neighbours):
    if state == 0 and nb_neighbours == 0:
        return 1
    elif state == 1 and nb_neighbours >= tolerance:
        return 0
    else:
        return state


def precompute_adjacent_neighbours(M, N):
    cache = defaultdict(lambda :[])
    for i in range(M):
        for j in range(N):
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ii = i+di
                    jj = j+dj
                    if (not (di == 0 and dj ==0)) and  0 <= ii < M and  0 <= jj < N:
                        cache[(i, j)].append((ii, jj))
    return cache

def precompute_distant_neighbours(m, M, N):
    cache = defaultdict(lambda :[])
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    for i in range(M):
        for j in range(N):
            for di, dj in directions:
                factor = 1
                ii = i + factor * di
                jj = j + factor * dj
                while 0 <= ii < M and  0 <= jj < N:
                    if m[ii, jj] != -1:
                        cache[(i, j)].append((ii, jj))
                        break
                    factor += 1
                    ii = i + factor * di
                    jj = j + factor * dj

    return cache


def count_neighbours(m, neighbours, i, j):
    count = 0
    for ii, jj in neighbours[(i, j)]:
        if m[ii, jj] == 1:
            count += 1
    return count

def next(state, neighbours, next_state_fn):
    m, n = state.shape
    new_state = np.zeros(state.shape)
    for i in range(m):
        for j in range(n):
            nb_neighbours = count_neighbours(state, neighbours, i, j)
            # print(i, j, nb_neighbours)
            new_state[i, j] = next_state_fn(state[i, j], nb_neighbours)
    return new_state

def parse_file(filename):
    mapping = {
        "L" : 0,
        "." : -1,
        "#" : 1
    }
    with open(filename) as file:
        return np.matrix([list(map(mapping.get, l.strip())) for l in file.readlines()])

def count_occupied(layout):
    ones = np.ones(layout.shape)
    return (layout == ones).sum()

def steps_to_convergence(layout, neighbours, next_state_fn):
    steps = 0
    while True:
        new_layout = next(layout, neighbours, next_state_fn)
        steps += 1
        if (new_layout == layout).all():
            break
        layout = new_layout

    return (steps - 1), layout
def main():
    layout = parse_file("input.txt")
    M, N = layout.shape
    intolerant_state_fn = lambda state, nb_neigh: next_state(4, state, nb_neigh)
    neighbours = precompute_adjacent_neighbours(M, N)
    nb_steps, final_state = steps_to_convergence(layout, neighbours, intolerant_state_fn)
    print(count_occupied(final_state))

    tolerant_state_fn = lambda state, nb_neigh: next_state(5, state, nb_neigh)
    neighbours = precompute_distant_neighbours(layout, M, N)
    nb_steps, final_state = steps_to_convergence(layout, neighbours, tolerant_state_fn)
    print(count_occupied(final_state))
        
    

if __name__ == '__main__':
    main()