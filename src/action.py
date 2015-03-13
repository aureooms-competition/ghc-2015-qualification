
from argparse import Action

class Dict ( Action ) :

	def __call__( self , parser , namespace , values , option_string = None ) :

		setattr( namespace , self.dest , self.choices[ values ] )
