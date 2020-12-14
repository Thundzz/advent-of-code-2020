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
    print(bin_val)
    print(mask)
    st = "".join(map(combine_mask, bin_val, mask))
    print(st)

apply(11, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")


def simulate(instructions):
    mem = { }
    current_mask = None
    for instr in instructions:
        pass




def main():
    instructions = parse_file("test.txt")
    simulate(instructions)


if __name__ == '__main__':
    main()
