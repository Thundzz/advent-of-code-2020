import re
from collections import namedtuple

Rule = namedtuple("Rule",["name", "ranges"])


def parse_rules(rules_block):
    lines = rules_block.split("\n")
    rule_regex = r"((?:[a-z]+ ?)+): (\d+-\d+) or (\d+-\d+)"
    rules = []
    for line in lines:
        match = re.match(rule_regex, line)
        rule_name = match.group(1)
        fst_range = tuple(map(int,match.group(2).split("-")))
        snd_range = tuple(map(int,match.group(3).split("-")))
        rules.append(Rule(rule_name, [fst_range, snd_range]))
    return rules

def parse_ticket(line):
    return list(map(int, line.split(",")))

def parse_input(filename):
    with open(filename) as file:
        rules, my_ticket, nearby_tickets = file.read().split("\n\n")
    rules = parse_rules(rules)
    own_ticket = parse_ticket(my_ticket.split("\n")[1])
    other_tickets = list(map(parse_ticket, nearby_tickets.split("\n")[1:]))

    return (rules, own_ticket, other_tickets)


def main():
    rules, my_ticket, nearby_tickets = parse_input("test.txt")
    print(rules, my_ticket, nearby_tickets)

if __name__ == '__main__':
    main()