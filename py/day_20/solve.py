import numpy as np
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

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
            res[v].append(k)
    return res

def to_int(side):
    return int("".join(map(str, np.array(side).flatten())), 2)

def rotate(tile):
    return np.rot90(tile, k=1, axes=(0, 1))

def fliph(tile):
    return np.flipud(tile)

def flipv(tile):
    return np.fliplr(tile)

def are_borders_top_left(tile, rm):
    top = tile[0,:]
    left = tile[:, 0]
    topi = to_int(top)
    lefti = to_int(left)
    return len(rm[topi]) == 1 and len(rm[lefti]) == 1

def are_aligned(tile, other_tile, direction):
    """
    direction == "horizontal" or "vertical"
    will compare that other_tile is below or at the right of tile
    """
    n = tile.shape[0]
    if direction == "horizontal":
        right_t = tile[:, n-1]
        left_ot = other_tile[:, 0]
        return (right_t == left_ot).all()
    if direction == "vertical":
        bottom_t = tile[n-1, :]
        top_ot = other_tile[0, :]
        return (bottom_t == top_ot).all()

def align_first_tile(tile_id, tiles, profiles, rm):
    m = fliph(tiles[tile_id])
    transforms = [
        rotate, rotate, rotate, rotate,
        fliph,
        rotate, rotate, rotate, rotate,
        flipv,
        rotate, rotate, rotate, rotate,
    ]
    tile = tiles[tile_id]
    while not are_borders_top_left(tile, rm):
        f = transforms.pop()
        tile = f(tile)
    return tile

def align_tiles(tile, other_tile, direction):
    transforms = [
        rotate, rotate, rotate, rotate,
        fliph,
        rotate, rotate, rotate, rotate,
        flipv,
        rotate, rotate, rotate, rotate,
    ]
    while not are_aligned(tile, other_tile, direction):
        f = transforms.pop()
        other_tile = f(other_tile)
    return other_tile

def find_neighbouring_tile(tile_id, tiles, profiles, rm, direction):
    tile = tiles[tile_id]
    n = tile.shape[0]
    if direction == "right":
        common_side = tile[:, n-1]
    elif direction == "down":
        common_side = tile[n-1:]
    else:
        raise Exception("Unexpected direction")

    common_side_id = to_int(common_side)
    return next(i for i in rm[common_side_id] if i != tile_id)

def reconstruct_image(tiles, profiles, rm):
    image_size = int(np.sqrt(len(tiles)))
    tile_size = list(tiles.values())[0].shape[0]
    image = np.zeros((image_size, image_size))
    border_profiles = set(k for k, v in rm.items() if len(v) == 1)
    corner_tiles = [
        t for t, profile in profiles.items()
        if len(set(profile) & border_profiles) >= 4
    ]
    first_tile = corner_tiles[0]

    aligned_tile = align_first_tile(first_tile, tiles, profiles, rm)
    tiles[first_tile] = aligned_tile
    image[0, 0] = first_tile

    for i in range(1, image_size):
        current_tile_id = image[i-1, 0]
        neighbour_id = find_neighbouring_tile(current_tile_id, tiles, profiles, rm, "down")
        neighbour = tiles[neighbour_id]
        current_tile = tiles[current_tile_id]
        aligned_neighour = align_tiles(current_tile, neighbour, direction="vertical")
        tiles[neighbour_id] = aligned_neighour
        image[i, 0] = neighbour_id

    for i in range(0, image_size):
        for j in range(1, image_size):
            current_tile_id = image[i, j-1]
            neighbour_id = find_neighbouring_tile(current_tile_id, tiles, profiles, rm, "right")
            neighbour = tiles[neighbour_id]
            current_tile = tiles[current_tile_id]
            aligned_neighour = align_tiles(current_tile, neighbour, direction="horizontal")
            tiles[neighbour_id] = aligned_neighour
            image[i, j] = neighbour_id

    tsm1 = tile_size - 2
    fullsize = image_size * tsm1
    full_picture = np.zeros((fullsize, fullsize))
    for i in range(image_size):
        for j in range(image_size):
            full_picture[i*tsm1:(i+1)*tsm1, j*tsm1:(j+1)*tsm1] = tiles[image[i, j]][1:-1, 1:-1]

    return full_picture


def monster_offsets():
    monster_pattern = np.matrix([
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1],
        [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0]
    ])
    m, n = monster_pattern.shape
    coords = []
    for i in range(m):
        for j in range(n):
            if monster_pattern[i, j] == 1:
                coords.append((i, j))
    return coords, (m, n)

def matches(picture, i, j, coords):
    return all([
        picture[i + ii, j + jj] == 1 for ii, jj in coords
    ])

def save_map(picture):
    plt.imshow(picture)
    plt.savefig("monsters.png", dpi=800)

def find_sea_monsters(picture):
    monster_off, (m, n) = monster_offsets()
    M, N = picture.shape
    monster_count = 0
    transforms = [
        rotate, rotate, rotate, rotate,
        fliph,
        rotate, rotate, rotate, rotate,
        flipv,
        rotate, rotate, rotate, rotate,
    ]
    while monster_count == 0:
        for i in range(M - m):
            for j in range(N - n):
                if matches(picture, i, j, monster_off):
                    monster_count += 1
                    for ii, jj in monster_off:
                        picture[i +ii, j +jj] = 9
        if monster_count == 0:
            f = transforms.pop()
            picture = f(picture)

    water_roughness = 0
    for i in range(M):
        for j in range(N):
            if picture[i, j] == 1:
                water_roughness += 1

    return water_roughness

def solve(tiles):
    profiles = {tid: compute_profile(t) for tid, t in tiles.items()}
    rm = reverse_mapping(profiles)
    picture = reconstruct_image(tiles, profiles, rm)
    roughness = find_sea_monsters(picture)
    print(roughness)


def main():
    tiles = parse_input("input.txt")
    solve(tiles)


if __name__ == '__main__':
    main()
