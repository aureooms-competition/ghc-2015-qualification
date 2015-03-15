
def id ( item ) :

	return item.id

def serverid ( item ) :

	return item.server.id

def capacity ( item ) :

	return item.capacity

def size ( item ) :

	return item.size

def row ( item ) :

	return item.row

def intervalrow ( item ) :

	return item.interval.row

def position ( item ) :

	return item.position

def second ( item ) :

	return item[1]

def affectation ( item ) :

	return ( item.interval.id , item.server.id , item.group )
