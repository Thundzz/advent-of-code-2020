import numpy as np
from collections import Counter, defaultdict

def parse_block(block):
    to_int = lambda c: 1 if c == "#" else 0
    lines = block.split("\n")
    tile_id = int(lines[0][5:9])
    data = [
        list(map(to_int, list(l.strip())))
        for l in lines[1:]
    ]
    return (tile_id, np.matrix(data))



def parse_input(filename):
    with open(filename) as file:
        blocks = file.read().strip().split("\n\n")
    return dict([parse_block(b) for b in blocks])

def compute_profile(tile):
    n = tile.shape[0]
    top = tile[0,:]
    bottom = tile[n-1,:]
    left = tile[:, 0]
    right = tile[:, n-1]
    res = []
    for side in [top, right, bottom, left]:
        arr = "".join(map(str, np.array(side).flatten()))
        res.append(int(arr, 2))
        res.append(int(arr[::-1], 2))
    return res

def reverse_mapping(d):
    res = defaultdict(lambda: list())
    for k, vs in d.items():
        for v in vs:
            print(v, k)
            res[v].append(k)
    return res

def solve(tiles):
    profiles = {tid: compute_profile(t) for tid, t in tiles.items()}
    # values = np.array(profiles).flatten()
    # c = Counter(values)
    # print(c)
    rm = reverse_mapping(profiles)
    border_profiles = set(k for k, v in rm.items() if len(v) == 1)
    corner_tiles = [
        t for t, profile in profiles.items()
        if len(set(profile) & border_profiles) >= 4
    ]

    print(corner_tiles)

def main():
    tiles = parse_input("test.txt")
    # for id, tile in tiles.items():
    #     print(id, tile)
    solve(tiles)
    # print(tiles)


if __name__ == '__main__':
    main()
