from src import key
from src import item
from src import eval
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

def affect_group_local_search(affectations, R, P):
	score = 0
	for i in range(len(affectations)):
		grp = randint(0, P-1)
		affectations[i].group = grp
	total = 100000
	i = 0
	while i < total:
		if i % (total/100) == 0:
			print(100*i/total,"%","   score = ",score)
		aff1 = randint(0, len(affectations)-1)
		aff2 = randint(0, len(affectations)-1)
		grp1 = randint(0, P-1)
		grp2 = randint(0, P-1)
		old1 = affectations[aff1].group
		old2 = affectations[aff2].group
		affectations[aff1].group = grp1
		affectations[aff2].group = grp2
		res = eval.all(R,P,affectations)
		if res >= score:
			score = res
		else:
			affectations[aff1].group = old1
			affectations[aff2].group = old2
		i+=1
	print ("Final score : ", score)
	return affectations

