
def groupchange ( solution , mutation ) :

	groups = solution.groups
	rows = solution.rows

	affectation , grp = mutation

	old = affectation.group
	affectation.group = grp

	capacity = affectation.server.capacity

	groups[old] -= capacity
	groups[grp] += capacity

	rows[affectation.interval.row][old] -= capacity
	rows[affectation.interval.row][grp] += capacity
