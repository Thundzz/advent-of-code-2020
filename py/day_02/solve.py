from collections import namedtuple, Counter

Input = namedtuple("Input", ["mini", "maxi", "letter", "password"])

def parse_one_record(line):
	"""
	Example record
	"13-14 f: fkpqnkfhvfssvhgqfm"
	"""
	condition, password = line.split(":")
	password = password[1:]
	ranges, letter = condition.split()
	mini, maxi = [int(i) for i in ranges.split("-")]
	return Input(mini,maxi, letter, password)

def parse_input(filename):
	with open(filename) as file:
		lines = [l.strip() for l in file.readlines()]

	return [parse_one_record(l) for l in lines]
	
def is_valid_1(case):
	c = Counter(case.password)
	res =  c[case.letter] >= case.mini and c[case.letter] <= case.maxi
	print(case, res)
	return res

def is_valid_2(case):
	cnt = 0
	for index in [case.mini-1, case.maxi-1]:
		if case.password[index] == case.letter:
			cnt += 1
	return cnt == 1
				

def main():
	inputs = parse_input("input.txt")
	s = sum([1 for item in inputs if is_valid_2(item)])
	print(s)

if __name__ == '__main__':
	main()
