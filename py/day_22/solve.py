from functools import lru_cache
from operator import mul

def parse_decks(filename):
    with open(filename) as file:
        player1_raw, player2_raw = file.read().split("\n\n")

    p1 = list(map(int, player1_raw.split("\n")[1:]))
    p2 = list(map(int, player2_raw.split("\n")[1:]))
    return p1, p2

def play_combat(p1, p2):
    while p1 and p2:
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)
    return p1, p2

def play_recursive_combat(p1, p2, depth=0):
    current_cache=set()
    p1 = list(p1)
    p2 = list(p2)
    while p1 and p2:
        if (tuple(p1), tuple(p2)) in current_cache:
            return (1, p1, p2)
        current_cache.add((tuple(p1), tuple(p2)))
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        if len(p1) >= c1 and len(p2) >= c2:
            winner, _, _ = play_recursive_combat(tuple(p1[:c1]), tuple(p2[:c2]), depth=depth+1)
            if winner == 1:
                p1.append(c1)
                p1.append(c2)
            else:
                p2.append(c2)
                p2.append(c1)
        else:
            if c1 > c2:
                p1.append(c1)
                p1.append(c2)
            else:
                p2.append(c2)
                p2.append(c1)
    return (1, p1, p2) if p1 else (2, p1, p2)

def get_score(deck):
    n = len(deck)
    l = map(mul, deck, reversed(range(1, n+1)))
    return sum(l)

def main():
    p1, p2 = parse_decks("input.txt")

    p1cpy, p2cpy = list(p1), list(p2)

    play_combat(p1cpy, p2cpy)
    winner = p1cpy if p1cpy else p2cpy
    score = get_score(winner)
    print(score)

    p1cpy, p2cpy = tuple(p1), tuple(p2)
    winner, p1final, p2final = play_recursive_combat(p1cpy, p2cpy)
    score = get_score(p1final) if winner == 1 else  get_score(p2final)
    print(score)


if __name__ == '__main__':
    main()
