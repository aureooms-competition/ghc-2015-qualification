
class Server :

	def __init__ ( self , id , capacity , size ) :

		self.id = id
		self.capacity = capacity
		self.size = size

class Interval :

	def __init__ ( self , row , start , size ) :

		self.row = row
		self.start = start
		self.size = size


class Affectation :

	def __init__ ( self , server , interval , position , group = -1 ) :

		self.server = server
		self.interval = interval
		self.position = position
		self.group = group

class Capacity :

	def __init__ ( self , total , guaranteed ) :

		self.total = total
		self.guaranteed = guaranteed
