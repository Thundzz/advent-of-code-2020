import re
from operator import add, mul

def parse_input(filename):
    with open(filename) as file:
        return [l.strip() for l in file.readlines()]

def eval_flat(simple):
    splitted = simple.split()
    current = int(splitted[0])
    op = None
    for token in splitted[1:]:
        if token == "+":
            op = add
        elif token == "*":
            op = mul
        else:
            current = op(int(token), current)
    return current

def eval_plus_more_precedence(simple):
    expr = simple
    sum_regex = r"\d+ \+ \d+"
    while "+" in expr:
        summ = re.findall(sum_regex, expr)[0]
        res = eval_flat(summ)
        expr = expr.replace(summ, str(res))
    return eval_flat(expr)

def evaluate(expr, eval_fn):
    simple_paren = r"\(\d[\d\+\* ]+\)"
    while "(" in expr:
        for simple_expr in re.findall(simple_paren, expr):
            res = eval_fn(simple_expr[1:-1])
            expr = expr.replace(simple_expr, str(res))
    return eval_fn(expr)

def main():
    exprs = parse_input("input.txt")
    s = sum(evaluate(expr, eval_flat) for expr in exprs)
    print(s)

    sols = [evaluate(expr, eval_plus_more_precedence) for expr in exprs]
    s = sum(sols)
    print(s)


if __name__ == '__main__':
    main()
