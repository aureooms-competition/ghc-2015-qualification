
from src import groupchange , serverswap , slotswap


class Neighborhood ( object ) :

	def __init__ ( self , Walk , Eval , Apply ) :

		self.Walk = Walk
		self.Eval = Eval
		self.Apply = Apply

DICT = {

	"sgc" : Neighborhood( groupchange.ShuffledWalk , groupchange.Eval , groupchange.Apply ) ,
	"rgc" : Neighborhood( groupchange.RandomWalk , groupchange.Eval , groupchange.Apply ) ,
	"ses" : Neighborhood( serverswap.Walk , serverswap.Eval , serverswap.Apply ) ,
	"sls" : Neighborhood( slotswap.Walk , slotswap.Eval , slotswap.Apply ) ,

}
