from collections import defaultdict

def play(starting_numbers, until):
    memory = defaultdict(list)
    for key in memory:
        memory[key] = []

    for idx, num in enumerate(starting_numbers):
        memory[num].append(idx + 1)

    current = starting_numbers[-1]
    current_turn = len(starting_numbers) + 1

    while current_turn <= until:
        last_history = memory[current]
        length = len(last_history)
        if length == 1:
            current = 0
        else:
            current = last_history[length-1] - last_history[length-2]
        memory[current].append(current_turn)
        current_turn += 1
    print(current)

def main():
    starting_numbers = [12,20,0,6,1,17,7]
    until = 2020
    play(starting_numbers, until)

    until = 30000000
    play(starting_numbers, until)
    

if __name__ == '__main__':
    main()