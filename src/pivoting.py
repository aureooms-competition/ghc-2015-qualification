
def best ( solution , walk , eval ) :

	best = solution.objective

	candidate = None

	for mutation in walk( solution ) :

		objective = eval( solution , mutation )

		if objective >= best :

			candidate = mutation
			best = objective

	return candidate , best


def first ( solution , walk , eval ) :

	current = solution.objective

	for mutation in walk( solution ) :

		objective = eval( solution , mutation )

		if objective > current :

			return mutation , objective

	return None , current


def firstandeq ( solution , walk , eval ) :

	current = solution.objective

	for mutation in walk( solution ) :

		objective = eval( solution , mutation )

		if objective >= current :

			return mutation , objective

	return None , current


def firstoreq ( solution , walk , eval ) :

	best = solution.objective

	candidate = None

	for mutation in walk( solution ) :

		objective = eval( solution , mutation )

		if objective > best :

			return mutation , objective

		if objective == best :

			candidate = mutation
			best = objective


	return candidate , best


DICT = { "best" : best , "first" : first , "firstandeq" : firstandeq , "firstoreq" : firstoreq }

