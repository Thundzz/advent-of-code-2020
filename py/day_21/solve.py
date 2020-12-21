from collections import namedtuple, defaultdict, Counter
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
    for allergen, sus in suspects.items():
        safe_ingr = safe_ingr - sus

    ingr = first(safe_ingr)
    count = 0
    for p in products:
        count += len(safe_ingr & p.ingredients)

    return count, suspects

def map_allergens(suspects):
    mapping = {}
    matched_suspects = set()
    while any(s for a, s in suspects.items() if len(s) >= 1):
        for allergen, sus in suspects.items():
            if len(sus) == 1:
                head = first(sus)
                mapping[allergen] = head
                matched_suspects.add(head)
        for allergen, sus in suspects.items():
            suspects[allergen] = sus - matched_suspects
    return mapping

def main():
    products = parse_input("input.txt")
    n, suspects = find_safe_ingredients(products)
    print(n)

    mapping = map_allergens(suspects)
    ordered = sorted(mapping.items(), key = lambda k: k[0])
    print(",".join([ingr for alle, ingr in ordered]))

if __name__ == '__main__':
    main()
