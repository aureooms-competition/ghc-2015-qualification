
from random import randint

def random ( P , affectations ) :

	for affectation in affectations :

		affectation.group = randint( 0 , P - 1 )

