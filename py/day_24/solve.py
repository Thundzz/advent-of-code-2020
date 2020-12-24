from collections import defaultdict, Counter

def parse_input(filename):
    with open(filename) as file:
        return [parse_instruction_line(l.strip()) for l in file.readlines()]

def parse_instruction_line(line):
    rev = list(reversed(line))
    instr = []
    while rev:
        cs = []
        c = rev.pop()
        cs.append(c)
        if c == "s" or c == "n":
            c2 = rev.pop()
            cs.append(c2)
        instr.append("".join(cs))
    return instr

def addt(t1, t2):
    x1, y1 = t1
    x2, y2 = t2
    return (x1 + x2, y1 + y2)


def flip(t):
    return "w" if t == "b" else "b"

def neighbour_offsets():
    return [ (1, 0), (0, -1), (1, -1), (-1, 0), (-1, 1), (0, 1) ]

def move(instructions, origin):
    axial_directions = {
        "e" : (1, 0),
        "nw" : (0, -1),
        "ne" : (1, -1),
        "w" : (-1, 0),
        "sw" : (-1, 1),
        "se" : (0, 1)
    }
    current = origin
    for instr in instructions:
        current = addt(current, axial_directions[instr])

    return current

def next_state(state):
    to_check = set()
    offsets = neighbour_offsets()
    for coords, tile_state in state.items():
        if tile_state == "b":
            to_check.add(coords)
            for coord in map(lambda off : addt(coords, off), offsets):
                to_check.add(coord)
    new_state = defaultdict(lambda :"w", state)
    for tile in to_check:
        nb_black_neighbours = len([
            1 for off in offsets if state[addt(tile,off)] == "b"
        ])
        if state[tile] == "b" and (nb_black_neighbours == 0 or nb_black_neighbours > 2):
            new_state[tile] = "w"
        elif state[tile] == "w" and nb_black_neighbours == 2:
            new_state[tile] = "b"

    return new_state


def count_black_tiles(all_instru):
    state = defaultdict(lambda :"w")
    origin = (0, 0)
    for instrs in all_instru:
        coords = move(instrs, origin)
        state[coords] = flip(state[coords])
    return state

def main():
    all_instru = parse_input("input.txt")
    state = count_black_tiles(all_instru)
    print(Counter(state.values())["b"])

    for i in range(100):
        state = next_state(state)

    # print(state)
    print(Counter(state.values())["b"])

if __name__ == '__main__':
    main()
