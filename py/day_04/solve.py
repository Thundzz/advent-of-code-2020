from collections import namedtuple, Counter
from operator import add, mul
from functools import reduce

def parse_field(raw_field):
	return raw_field.split(":")

def parse_input(filename):
	with open(filename) as file:
		lines = [l.strip() for l in file.readlines()]

	passports = []
	passport = {}
	for line in lines:
		if not line:
			passports.append(passport)
			passport = {}
		else:
			fields = dict([parse_field(rf) for rf in line.split()])
			passport = { **passport, **fields }
	
	passports.append(passport)
	return passports

def has_mandatory_fields(passport, mandatory_fields):
	return all([
		field in passport
		for field in mandatory_fields
	])

ValidationRule = namedtuple("ValidationRule", ["parsing_fn", "validation_fn"])
Height = namedtuple("Height", ["value", "unit"])

def validate_rule(value, validation_rule):
	parsed = None
	try:
		parsed = validation_rule.parsing_fn(value)
	except Exception as e:
		print("parsing error", value, validation_rule)
		return False
	if parsed:
		return validation_rule.validation_fn(parsed)

def validates_rules(passport, rules):
	return all([
		fieldName in passport and validate_rule(passport[fieldName], rule)
		for fieldName, rule in rules
	])

def parse_year(data):
	digits = set(map(str, range(10)))
	assert(len(data) == 4)
	assert(all([d in digits for d in data]))

	return int(data)

def parse_height(data):
	digits = set(map(str, range(10)))
	unit = data[-2:]
	value = data[:-2]

	assert(unit in {"cm", "in"})
	assert(all([(d in digits) for d in value]))
	return Height(int(value), unit)

def validate_height(height):
	if height.unit == "cm":
		return 150 <= height.value <= 193
	elif height.unit == "in":
		return 59 <= height.value <= 76
	else:
		raise Exception("This should not happen")


def validate_eye_color(data):
	valid_clrs = { "amb","blu","brn","gry","grn","hzl","oth" }
	return data in valid_clrs

def validate_hair_color(haircolor):
	valid_chars = set(list(range(10)) + ["a", "b", "c", "d", "e", "f"])
	chars_are_valid = all([c in valid_chars for c in list(haircolor[1:])])
	return  haircolor[0] == "#" 

def validate_cid(cid):
	digits = set(map(str, range(10)))
	return len(cid) == 9 and all([d in digits for d in cid])

def main():
	passports = parse_input("input.txt")
	mandatory_fields = [ "byr","iyr","eyr","hgt","hcl","ecl","pid" ]
	identity = lambda x: x

	rules = {
		"byr" : ValidationRule(parse_year, lambda x:  1920 <= x <= 2002),
		"iyr" : ValidationRule(parse_year, lambda x:  2010 <= x <= 2020),
		"eyr" : ValidationRule(parse_year, lambda x:  2020 <= x <= 2030),
		"hgt" : ValidationRule(parse_height, validate_height),
		"hcl" : ValidationRule(identity, validate_hair_color),
		"ecl" : ValidationRule(identity, validate_eye_color),
		"pid" : ValidationRule(identity, validate_cid)
	}
	valid_passports_simple = [ 
		passport for passport in passports
		if has_mandatory_fields(passport, mandatory_fields)
	]

	valid_passports_complex = [ 
		passport for passport in passports
		if validates_rules(passport, rules.items())
	]
	# print(passports[0])
	# for x, rule in rules.items():
	# 	res = validate_rule(passports[0][x], rule)
	# 	print(x, rule, res)

	print(len(valid_passports_simple))
	print(len(valid_passports_complex))
	
	


if __name__ == '__main__':
	main()
