from operator import mul
from functools import reduce, lru_cache

def parse_input(filename):
    with open(filename) as file:
        door_pk, card_pk = map(int, file.readlines())
    return door_pk, card_pk

def get_base_powers(base, modulus, count):
    base_powers = [base]
    current = base*base % modulus
    for i in range(count):
        base_powers.append(current)
        current = (current * current) % modulus
    return base_powers

def compute_powermod(base, exponent, modulus, base_powers):
    """
    I got the idea of this implementation from this page:
    http://www.math.stonybrook.edu/~scott/blair/Powers_modulo_prime.html.

    This could be made faster easily by unwrapping everything into loops.
    """
    bin_expo = list(reversed(list(map(int, bin(exponent)[2:]))))
    factors = [base_powers[idx] for idx, b in enumerate(bin_expo) if b == 1]
    return reduce(mul, factors) % modulus


def find_loop_size(subject_number, target, modulus, base_powers):
    """
    This operation is called computing the discrete logarithm of a number.
    This is certainly not very efficient.
    An online calculator can be found here : https://www.alpertron.com.ar/DILOG.HTM
    """
    loop_size = 1
    res = compute_powermod(subject_number, loop_size, modulus, base_powers)
    while res != target:
        loop_size += 1
        res = compute_powermod(subject_number, loop_size, modulus, base_powers)
    return loop_size

def main():
    subject_number = 7
    modulus = 20201227
    base_powers = get_base_powers(subject_number, modulus, 30)
    door_pk, card_pk = parse_input("input.txt")
    door_ls = find_loop_size(subject_number, door_pk, modulus, base_powers)
    print(door_ls)
    card_ls = find_loop_size(subject_number, card_pk, modulus, base_powers)
    print(card_ls)
    base_powers = get_base_powers(card_pk, modulus, 30)
    res = compute_powermod(card_pk, door_ls, modulus, base_powers)
    print(res)

if __name__ == '__main__':
    main()
