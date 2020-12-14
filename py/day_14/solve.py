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

def apply_v1(value, mask):
    bin_val = format(value, '#038b')[2:]
    st = "".join(map(combine_mask, bin_val, mask))
    return st


def simulate_decoder_v1(instructions):
    mem = { }
    current_mask = None
    for instr in instructions:
        if type(instr) == Mask:
            current_mask = instr.value
        else:
            mem[instr.addr] = apply_v1(instr.value, current_mask)
    s = 0
    for addr, value in mem.items():
        s += int(value, 2)
    return s

def combine_mask_v2(c1, m):
    if m == '0':
        return c1
    if m == '1':
        return '1'
    if m == 'X':
        return 'X'

def get_addresses(mask, value):
    n = len([c for c in mask if c == "X"])
    fb_combinations = map(lambda num: list(format(num, f'#0{n+2}b')[2:]), range(2**n))
    bin_value = format(value, f'#038b')[2:]
    base_addr = list(map(combine_mask_v2, bin_value, mask))
    floating_bits_positions =  [idx for idx, bit in enumerate(base_addr) if bit == 'X' ]
    addresses = []
    for combination in fb_combinations:
        copy = list(base_addr)
        for idx, fb_pos in enumerate(floating_bits_positions):
            copy[fb_pos] = combination[idx]

        int_addr = int("".join(copy), 2)
        addresses.append(int_addr)
    return addresses

def simulate_decoder_v2(instructions):
    mem = { }
    current_mask = None
    for instr in instructions:
        if type(instr) == Mask:
            current_mask = instr.value
        else:
            addresses = get_addresses(current_mask, instr.addr)
            for addr in addresses:
                mem[addr] = instr.value
    s = 0
    for addr, value in mem.items():
        s += value
    return s

def main():
    instructions = parse_file("input.txt")
    s = simulate_decoder_v1(instructions)
    print(s)
    s = simulate_decoder_v2(instructions)
    print(s)


if __name__ == '__main__':
    main()
