import re
from collections import namedtuple
from functools import lru_cache

Or = namedtuple("Or", ["key", "left", "right"])
Leaf = namedtuple("Leaf", ["key", "character"])
Simple = namedtuple("Simple", ["key", "expr"])

def parse_rule(raw_rule):
    or_regex = r"(\d+): ([\d ]+) \| ([\d ]+)"
    simple_regex = r'(\d+): ([\d ]+)'
    leaf_regex = r'(\d+): "(.*)"'

    if '"' in raw_rule:
        match = re.search(leaf_regex, raw_rule)
        key = int(match.group(1))
        value = match.group(2)
        return Leaf(key, value)
    elif '|' in raw_rule:
        match = re.search(or_regex, raw_rule)
        key = int(match.group(1))
        left = tuple(map(int, match.group(2).split()))
        right = tuple(map(int, match.group(3).split()))
        return Or(key, left, right)
    else:
        match = re.search(simple_regex, raw_rule)
        key = int(match.group(1))
        values = tuple(map(int, match.group(2).split()))
        return Simple(key, values)

def parse_input(filename):
    with open(filename) as file:
        raw_rules, raw_messages = file.read().split("\n\n")

    rules = [parse_rule(rule.strip()) for rule in raw_rules.split("\n")]
    rules = { r.key : r for r in rules }
    messages = [msg.strip() for msg in raw_messages.split("\n")]
    return (rules, messages)

def wrap(r):
    return f"(?:{r})"

def gen_regex(rules, patched):
    @lru_cache(maxsize=100)
    def go(origin):
        rule = rules[origin]
        if patched: 
            if rule.key == 8:
                return wrap(wrap(go(42)) + "+")

            if rule.key == 11:
                equally_repeated = [wrap(wrap(go(42))+f"{{{i}}}" + wrap(go(31))+f"{{{i}}}") for i in range(1, 10)]
                return wrap("|".join(equally_repeated))

        if type(rule) == Simple:
            children = [go(child) for child in rule.expr]
            return wrap("".join(children))

        elif type(rule) == Or:
            left = [go(child) for child in rule.left]
            lefts = "".join(left)
            right = [go(child) for child in rule.right]
            rights = "".join(right)
            return wrap("|".join([lefts, rights]))
        elif type(rule) == Leaf:
            return rule.character
        else:
            raise Exception(f"Unexpected rule type : {rule}")

    reg = go(0)
    return f"^{reg}$"
    

def main():
    rules, messages = parse_input("input.txt")

    r = gen_regex(rules, patched = False)
    valid = [msg for msg in messages if re.match(r, msg)]
    print(len(valid))


    r = gen_regex(rules, patched = True)
    valid = [msg for msg in messages if re.match(r, msg)]
    print(len(valid))


if __name__ == '__main__':
    main()
