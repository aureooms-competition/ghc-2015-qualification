from src import key
from src import item

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

