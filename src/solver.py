from src import key
from src import item
from src import eval
from random import randint
from random import shuffle

from src.item import Affectation


def affect ( servers , intervals ) :

	intervals = sorted( intervals , key = key.row )

	affectations = []

	available = [ interval.size for interval in intervals ]

	for server in servers :

		for i , interval in enumerate( intervals ) :

			if available[i] >= server.size :

				available[i] -= server.size
				affectation = Affectation( server , interval , available[i] )
				affectations.append( affectation )
				break

	return affectations


def scoreAffectations( affectations ) :

	return sum( affectation.server.capacity for affectation in affectations )


def first_fit( servers , intervals , iterations = 1 ) :

	best = []
	res = []

	bestScore = 0
	score = 0

	shuffle( servers )

	for i in range( iterations ) :

		res = affect(servers, intervals)
		score = scoreAffectations(res)
		if score > bestScore:
			print("number of affectations : ", len(res))
			best = res
			bestScore = score

	return best

def affect_group_local_search(affectations, R, P):
	score = 0
	for i in range(len(affectations)):
		grp = randint(0, P-1)
		affectations[i].group = grp
	total = 200000
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

