from operator import mul
def parse_decks(filename):
    with open(filename) as file:
        player1_raw, player2_raw = file.read().split("\n\n")

    p1 = list(map(int, player1_raw.split("\n")[1:]))
    p2 = list(map(int, player2_raw.split("\n")[1:]))
    return p1, p2

def play(p1, p2):
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

def get_score(deck):
    n = len(deck)
    l = map(mul, deck, reversed(range(1, n+1)))
    return sum(l)

def main():
    p1, p2 = parse_decks("input.txt")
    play(p1, p2)

    winner = p1 if p1 else p2
    score = get_score(winner)
    print(score)


if __name__ == '__main__':
    main()
