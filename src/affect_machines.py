from src import key
from src import item
from random import randint

def first_fit(servers, intervals, num_rows):
	sorted_intervals = sorted(intervals, key=key.row)
	pos_left = []
	res = []
	for i in sorted_intervals :
		pos_left.append(i.size)
	while len(servers) > 0:
		s = servers.pop()
		for i in range(len(sorted_intervals)):
			if(pos_left[i] >= s.size):
				res.append(item.Affectation(s, sorted_intervals[i], sorted_intervals[i].size - pos_left[i]))
				pos_left[i] -= s.size
				break 
	return res

def affect_group_local_search(affectations, nbr_groups):
	score = 0
	for i in range(10000):
		aff = randint(0, len(affectations)-1)
		grp = randint(0, nbr_groups-1)
		old = affectations[var].group
		affectations[aff].group = grp
		# test
		if res >= score:
			score = res
		else:
			affectations[aff].group = old
	return affectations

