
class Server ( object ) :

	def __init__ ( self , id , capacity , size ) :

		self.id = id
		self.capacity = capacity
		self.size = size

	def __str__( self ) :

		return "S %(id)s %(capacity)s %(size)s" % self.__dict__

class Interval ( object ) :

	def __init__ ( self , row , start , size ) :

		self.row = row
		self.start = start
		self.size = size

	def __str__( self ) :

		return "I %(row)s %(start)s %(size)s" % self.__dict__

class Affectation ( object ) :

	def __init__ ( self , server , interval , position , group = -1 ) :

		self.server = server
		self.interval = interval
		self.position = position
		self.group = group

	def __str__( self ) :

		return "A %(server)s %(interval)s %(position)s %(group)s" % self.__dict__
