
from random import randint

from src import key

def random ( args , problem , affectations ) :

	for affectation in affectations :

		affectation.group = randint( 0 , problem.P - 1 )

def uniform ( args , problem , affectations ) :

	affectations = sorted( affectations , key = key.intervalrow )

	for i , affectation in enumerate( affectations ) :

		affectation.group = i % problem.P

def clever ( args , problem , affectations ) :

	rows = [ [ 0 ] * problem.P for i in range( problem.R ) ]

	groups = [ 0 ] * problem.P

	affectations = sorted( affectations , key = key.intervalrow )

	for i , affectation in enumerate( affectations ) :

		r = affectation.interval.row

		g , _ = min( ( ( g , _ ) for ( g , _ ) in enumerate( groups ) if rows[r][g] == 0 ) , key = key.second )

		rows[r][g] += affectation.server.capacity

		groups[g] += affectation.server.capacity

		affectation.group = g

DICT = {

	"random"  : random ,
	"uniform" : uniform ,
	"clever" : clever

}
