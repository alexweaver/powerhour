from random import randint

def get_random_ordering(n):
	order = list(range(n))
	while n > 0:
		n -= 1
		i = randint(0, n)
		order[i], order[n] = order[n], order[i]
	return order