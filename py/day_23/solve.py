
def as_list(input_str):
	return list(map(int, list(input_str)))

def play_move_new(state, current_cup, mini, maxi):
	current = current_cup
	picked = []
	for _ in range(3):
		prev, nex = state[current]
		picked.append(nex)
		current = nex
	pi, ni = state[current_cup]
	pl, nl = state[current]
	state[current_cup] = (pi, nl)

	picked_set = set(picked)

	destination_cup = current_cup - 1
	while destination_cup in picked_set or not (mini <= destination_cup <= maxi):
		if destination_cup < mini:
			destination_cup = maxi
		else:
			destination_cup = destination_cup - 1

	pd, nd = state[destination_cup]
	_, nnd = state[nd]
	state[destination_cup] = (pd, picked[0])
	state[nd] = (picked[2], nnd)
	state[picked[0]] = (destination_cup, picked[1])
	state[picked[2]] = (picked[1], nd)

	return state, state[current_cup][1]

def compute_label(state):
	c = state[1][1]
	l = []
	while c != 1:
		l.append(c)
		p, n = state[c]
		c = n
	return "".join(map(str, l))

def struct(l):
	n = len(l)
	s = {}
	for i in range(n):
		prev = l[(i-1) % n]
		nex = l[(i+1) % n]
		s[l[i]] = (prev, nex)
	return s

def simulate(l, nb_iter):
	mini = min(l)
	maxi = max(l)
	state = struct(l)
	current_cup = l[0]
	elements_set = set(l)
	for i in range(nb_iter):
		state, current_cup = play_move_new(state, current_cup, mini, maxi)
	return state

def main():
	test_input = as_list("389125467")
	real_input = as_list("389547612")

	crabbed_test_input = test_input + list(range(10, 1000001))
	crabbed_real_input = real_input + list(range(10, 1000001))

	state = simulate(test_input, 10)
	label = compute_label(state)
	print(label)

	state = simulate(test_input, 100)
	label = compute_label(state)
	print(label)

	state = simulate(real_input, 100)
	label = compute_label(state)
	print(label)

	s = simulate(crabbed_real_input, 10000000)
	_, nx = s[1]
	_, nnx = s[nx]
	print(nx, nnx, nx * nnx)

if __name__ == '__main__':
    main()
