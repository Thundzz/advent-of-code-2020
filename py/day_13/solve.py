from operator import mul
from functools import reduce

def parse_file(filename):
    with open(filename) as file:
        lines = file.readlines()
    timestamp = int(lines[0])
    buses_str = lines[1].strip().split(",")
    buses_non_cancelled = [b for b in buses_str if b != "x"]
    bus_ids = list(map(int, buses_non_cancelled))
    return timestamp, bus_ids, buses_str

def find_next(timestamp, bus_ids):
    next_stops = [((timestamp // bid) + 1) * bid for bid in bus_ids]
    closest_next_stop = min(next_stops)
    bus_index = next_stops.index(closest_next_stop)
    bus_id_shortest = bus_ids[bus_index]
    return (closest_next_stop -timestamp) * bus_id_shortest

def euclide(a, b):
    """
    cf: https://fr.wikipedia.org/wiki/Algorithme_d%27Euclide_%C3%A9tendu
    """
    if b == 0:
        return (a, 1, 0)
    else:
        div, mod = divmod(a, b)
        (dp, up, vp) = euclide(b, mod)
        return (dp, vp, up - div*vp)

def check_sol(sol, buses):
    for offset, busid in buses:
        assert(((sol + offset) %  busid) == 0)

def find_synced(all_buses):
    """
    I noticed that busids were all 2 by 2 coprime.
    This solution is based on the chinese remainder theorem :
    https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    """
    constraints = [(idx, int(bus)) for idx, bus in enumerate(all_buses)  if bus != "x"]
    n = reduce(mul, [bus for _, bus in constraints])
    eis = []
    for offset, bus in constraints:
        (d, u, v) = euclide(bus, n // bus)
        e = v * (n // bus)
        eis.append(e)
    ais = [-idx for idx, bus in constraints]
    x = sum(map(lambda xs: xs[0] * xs[1], zip(ais, eis)))
    sol = x % n
    check_sol(sol, constraints)
    return sol


def main():
    timestamp, bus_ids, all_buses = parse_file("input.txt")
    next_timestamp = find_next(timestamp, bus_ids)
    print(next_timestamp)
    sol = find_synced(all_buses)
    print(sol)


if __name__ == '__main__':
    main()
