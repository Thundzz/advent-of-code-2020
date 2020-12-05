from collections import namedtuple

def parse_input(filename):
	with open(filename) as file:
		return [l.strip() for l in file.readlines()]

def to_index(size, bsp_mapping):
	def aux(mini, maxi, mapping):
		middle = (mini + maxi) // 2
		if not mapping:
			assert(mini == maxi == middle)
			return middle
		head = mapping.pop(0)
		if head == 0:
			return aux(mini, middle, mapping)
		else:
			return aux(middle+1, maxi, mapping)

	return aux(0,size-1, bsp_mapping)

def parse_bsp_site(bsp_seat):
	to_bit = lambda c: 0 if c in {"F", "L"} else 1
	row, col = list(map(to_bit,bsp_seat[:7])), list(map(to_bit, bsp_seat[7:]))
	return row, col

def main():
	NB_ROWS = 128
	NB_COL = 8

	boarding_passes = parse_input("input.txt")
	bp_as_bsp = [parse_bsp_site(bp) for bp in boarding_passes]
	bp_as_indices = [(to_index(NB_ROWS, rowbp), to_index(NB_COL, colbp)) for rowbp, colbp in bp_as_bsp]

	seat_ids = [(row * NB_COL) +  col for row, col in bp_as_indices]
	print(max(seat_ids))
	
	NB_SEATS = NB_ROWS*(NB_COL+1)

	empty_or_missing_s = set(range(NB_SEATS)) - set(seat_ids)
	empty_or_missing = sorted(list(empty_or_missing_s))

	print(next(s for s in empty_or_missing if not ({ s-1, s+2 } & empty_or_missing_s)))

if __name__ == '__main__':
	main()
