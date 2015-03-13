
from src import groupchange


class Neighborhood ( object ) :

	def __init__ ( self , Walk , Eval , Apply ) :

		self.Walk = Walk
		self.Eval = Eval
		self.Apply = Apply

DICT = {

	"sgc" : Neighborhood( groupchange.ShuffledWalk , groupchange.Eval , groupchange.Apply ) ,
	"rgc" : Neighborhood( groupchange.RandomWalk , groupchange.Eval , groupchange.Apply )

}
