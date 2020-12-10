import numpy as np
from collections import Counter

def parse_file(filename):
    with open(filename) as file:
        return list(map(int, file.readlines()))


def main():
    sequence = parse_file("input.txt")
    n = len(sequence)
    sorted_seq = [0] + sorted(sequence) 
    sorted_seq.append(sorted_seq[n] + 3)

    diffs =  [sorted_seq[i+1] - sorted_seq[i]  for i in range(n+1)] 
    c = Counter(diffs)
    print(c)
    print(c[1] * c[3])
        
    

if __name__ == '__main__':
    main()