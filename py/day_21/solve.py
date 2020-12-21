from collections import namedtuple, defaultdict
import re

Product = namedtuple("Product", ["ingredients", "known_allergens"])

def first(s):
    for e in s:
        break
    return e

def parse_product(line):
    product_regex = r"([\w ]+) \(contains ([\w ,]+)\)"
    match = re.search(product_regex, line)
    ingredients = set(match.group(1).split())
    allergens = set(match.group(2).split(", "))
    return Product(ingredients, allergens)

def parse_input(filename):
    with open(filename) as file:
        lines = file.readlines()
    return [parse_product(l) for l in lines]

def find_safe_ingredients(products):
    all_ingredients = set()
    suspects = dict()
    for p in products:
        for allerg in p.known_allergens:
            all_ingredients = all_ingredients | set(p.ingredients)
            if allerg not in suspects:
                suspects[allerg] = set(p.ingredients)
            else:
                suspects[allerg] = suspects[allerg] & set(p.ingredients)
    safe_ingr = set(all_ingredients)
    for allergen, suspects in suspects.items():
        safe_ingr = safe_ingr - suspects

    ingr = first(safe_ingr)
    count = 0
    for p in products:
        count += len(safe_ingr & p.ingredients)
    return count


def main():
    products = parse_input("input.txt")
    n = find_safe_ingredients(products)
    print(n)

if __name__ == '__main__':
    main()
