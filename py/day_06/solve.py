from collections import namedtuple
from functools import reduce
import string

def parse_input(filename):
    with open(filename) as file:
        content = file.read()
    return [ g.strip().split("\n") for g in content.split("\n\n")]

def distinct_questions(group):
    return reduce(lambda s, person: s.union(list(person)), group, set())

def common_questions(group):
    return reduce(lambda s, person: s & set(list(person)), group, set(string.ascii_lowercase))

def main():
    groups = parse_input("input.txt")
    dqs = [distinct_questions(group) for group in groups]
    cqs = [common_questions(group) for group in groups]
    
    print(sum([len(dq) for dq in dqs]))
    print(sum([len(cq) for cq in cqs]))


if __name__ == '__main__':
    main()
