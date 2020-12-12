import numpy as np
from collections import defaultdict
import json

class Ship:
    def __init__(self):
        """
        0 degrees facing east
        """
        self.x = 0
        self.y = 0
        self.rotation = 0

    def apply(self, instr, value):
        if instr == "L":
            self.rotation += value
        elif instr == "R":
            self.rotation -= value
        elif instr == "F":
            mapping = { 0 : "E", 90 : "N",  180 : "W", 270: "S" }
            self.move(mapping[self.rotation % 360], value)
        else:
            self.move(instr, value)


    def move(self, direction, value):
        direction_offsets = {
            "N" : (0, 1),
            "S" : (0, -1),
            "E" : (1, 0),
            "W" : (-1, 0)
        }
        multiplicator = lambda x: value * x
        dx, dy = map(multiplicator, direction_offsets[direction])
        self.x += dx
        self.y += dy

    def distance(self):
        return abs(self.x) + abs(self.y)

class WayPointShip:
    def __init__(self):
        """
        0 degrees facing east
        """
        self.position = complex(0, 0)
        self.waypoint = complex(10, 1)

    def apply(self, instr, value):
        if instr == "L":
            self.waypoint = self.waypoint * (complex(0, 1) ** (value/90))
        elif instr == "R":
            self.waypoint = self.waypoint * (complex(0, -1) ** (value/90))
        elif instr == "F":
            mapping = { 0 : "E", 90 : "N",  180 : "W", 270: "S" }
            self.position += value * self.waypoint
        else:
            self.move(instr, value)


    def move(self, direction, value):
        direction_offsets = {
            "N" : complex(0, 1),
            "S" : complex(0, -1),
            "E" : complex(1, 0),
            "W" : complex(-1, 0)
        }
        self.waypoint += value * direction_offsets[direction]

    def distance(self):
        return abs(self.position.real) + abs(self.position.imag)

def parse_file(filename):
    with open(filename) as file:
        lines = file.readlines()
    return [(line[0], int(line[1:])) for line in lines]

def main():
    instructions = parse_file("input.txt")
    ship = Ship()
    for instr, value in instructions:
        ship.apply(instr, value)

    print(ship.distance())
    ship = WayPointShip()
    for instr, value in instructions:
        ship.apply(instr, value)

    print(ship.distance())


if __name__ == '__main__':
    main()