
def apply ( solution , mutation ) :

	groups = solution.groups
	rows = solution.rows

	ax , ay = mutation

	rows[ax.interval.row][ax.group] -= ax.server.capacity
	rows[ay.interval.row][ay.group] -= ay.server.capacity

	groups[ax.group] -= ax.server.capacity
	groups[ay.group] -= ay.server.capacity

	ax.group , ay.group = ay.group , ax.group

	rows[ax.interval.row][ax.group] += ax.server.capacity
	rows[ay.interval.row][ay.group] += ay.server.capacity

	groups[ax.group] += ax.server.capacity
	groups[ay.group] += ay.server.capacity
