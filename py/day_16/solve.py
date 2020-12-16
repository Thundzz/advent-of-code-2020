import re
from collections import namedtuple
import numpy as np

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
    other_tickets = list(map(parse_ticket, nearby_tickets.strip().split("\n")[1:]))

    return (rules, own_ticket, other_tickets)

def is_compatible(value, rule):
    are_valid = [start <= value <= end for start, end in rule.ranges]
    return any(are_valid)

def is_invalid(value, rules):
    for rule in rules:
        if is_compatible(value, rule):
            return False

    return True

def scan_invalid_tickets(tickets, rules):
    invalid = []
    valid_tickets = []
    for ticket in tickets:
        valid = True
        for value in ticket:
            if is_invalid(value, rules):
                invalid.append(value)
                valid = False
        if valid:
            valid_tickets.append(ticket)

    return sum(invalid), valid_tickets

def compatibility_matrix(rules, tickets):
    """
    Generates a compatibility matrix between rules and ticket positions.
    [[0. 1. 0.]
     [1. 1. 0.]
     [1. 1. 1.]]
    Is the matrix generated for the second star example.
    The matrix is read as M[ticket_position, rule_index] == 1 if the  ticketposition is compatible
    with rule at index rule_index.
    """
    nb_pos = len(tickets[0])
    ticket_matrix = np.matrix(tickets)
    compat_matrix = np.zeros((nb_pos, len(rules)))
    for position in range(nb_pos):
        for rule_idx, rule in enumerate(rules):
            items = ticket_matrix[:, position].flatten().tolist()[0]
            v = 1 if all(is_compatible(item, rule) for item in items) else 0
            compat_matrix[position, rule_idx] = v
    return compat_matrix

def sorted_positions(n, compat):        
    return sorted(range(n), key= lambda pos: np.count_nonzero(compat[pos, :] == 1))

def find_mapping(rules, tickets):
    compat = compatibility_matrix(rules, tickets)
    n = len(tickets[0])
    positions = sorted_positions(n, compat)
    solution = np.full(n, -1)
    candidate_rules = set(range(len(rules)))
    last_solution = []
    def backtrack():
        for position in positions:
            if solution[position] == -1:
                for rule_idx in candidate_rules:
                    if compat[position, rule_idx] == 1:
                        solution[position] = rule_idx
                        candidate_rules.remove(rule_idx)
                        # print(solution)
                        backtrack()
                        solution[position] = -1
                        candidate_rules.add(rule_idx)
                return 
        last_solution.append(np.array(solution).tolist())
    backtrack()
    return last_solution[0]


def solve(rules, valid_tickets, my_ticket):
    sol = find_mapping(rules, valid_tickets)
    departure_rule_indices = [idx for idx, rule in enumerate(rules) if "departure " in rule.name]
    m = 1
    for rule_index in departure_rule_indices:
        rule_position = sol.index(rule_index)
        m *= my_ticket[rule_position]
    return m


def main():
    rules, my_ticket, nearby_tickets = parse_input("input.txt")
    srr, valid_tickets = scan_invalid_tickets(nearby_tickets, rules)
    print(srr)
    valid_tickets.append(my_ticket)
    s = solve(rules, valid_tickets, my_ticket)
    print(s)

if __name__ == '__main__':
    main()