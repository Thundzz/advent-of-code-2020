

def parse_line(line):
    splitted = line.strip().split()
    instruction, count = splitted[0], int(splitted[1])
    return instruction, count

def parse_input(filename):
    with open(filename) as file:
        lines = file.readlines()

    return [parse_line(l) for l in lines]

def evaluate_til_repeat(instructions):
    seen_instructions_idx = set()
    program_length = len(instructions)
    instruction_counter = 0
    acc = 0
    while instruction_counter < program_length:
        if instruction_counter in seen_instructions_idx:
            return "Failed", acc
        seen_instructions_idx.add(instruction_counter)

        instr, count = instructions[instruction_counter]
        # print(instr, count, acc)
        if instr == "nop":
            instruction_counter += 1
        elif instr == "jmp":
            instruction_counter += count
        elif instr == "acc":
            instruction_counter += 1
            acc += count
    return "Succeeded", acc



def swapped(instructions, idx):
    swap = lambda i: "nop" if i == "jmp" else "jmp"
    instr, count = instructions[idx]
    copy = list(instructions)
    copy[idx] = (swap(instr), count)
    return copy

def bruteforce(instructions):
    """
    It's kinda lame that I had to resort to this.
    I would have preferd to find some more clever solution 
    which does not involve simulating every possible program
    but I'm too tired today to search for a more elaborate solution.

    Maybe if I have the energy, I will do that for the scala version.
    """
    swappable_instructions = [
        idx for idx, (instr, c) in enumerate(instructions)
        if instr == "jmp" or instr == "nop"
    ]
    for idx in swappable_instructions:
        status, acc = evaluate_til_repeat(swapped(instructions, idx))
        if status == "Succeeded":
            return acc

def main():
    instructions = parse_input("input.txt")
    status, acc = evaluate_til_repeat(instructions)
    print(acc)
    acc = bruteforce(instructions)
    print(acc)


if __name__ == '__main__':
    main()