import re
from collections import namedtuple


Mask = namedtuple("Mask", ["value"])
Memwrite = namedtuple("Memwrite", ["addr", "value"])

def parse_line(line):
    mask_regexp = r"mask = (\w+)"
    mem_regexp =  r"mem\[(\d+)\] = (\d+)"
    mask_match = re.search(mask_regexp, line)
    if mask_match:
        return Mask(mask_match.group(1))
    else:
        mem_match = re.search(mem_regexp, line)
        address = int(mem_match.group(1))
        value = int(mem_match.group(2))
        return Memwrite(address, value)


def parse_file(filename):
    with open(filename) as file:
        lines = file.readlines()
    return [ parse_line(line.strip()) for line in lines ]


def combine_mask(c1, m):
    if m == "X":
        return c1
    else:
        return m

def apply(value, mask):
    bin_val = format(value, '#038b')[2:]
    st = "".join(map(combine_mask, bin_val, mask))
    return st


def simulate(instructions):
    mem = { }
    current_mask = None
    for instr in instructions:
        if type(instr) == Mask:
            current_mask = instr.value
        else:
            mem[instr.addr] = apply(instr.value, current_mask)
    s = 0
    for addr, value in mem.items():
        s += int(value, 2)
    return s

def main():
    instructions = parse_file("input.txt")
    s = simulate(instructions)
    print(s)


if __name__ == '__main__':
    main()
