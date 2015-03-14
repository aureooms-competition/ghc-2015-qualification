from src import eval

class Walk ( object) :

	def __init__ ( self , problem ) : pass

	def __call__ ( self , solution ) :

		affectations = solution.affectations

		for ax in affectations :

			for ay in affectations :

				if ax.server.capacity == ay.server.capacity :

					yield ax , ay

class Eval ( object ) :

	def __init__ ( self , problem ) : pass

	def __call__ ( self , solution , mutation ) :

		ax , ay = mutation

		apply( solution , ( ax , ay ) )

		obj = eval.objective( solution.groups , solution.rows )

		apply( solution , ( ay , ax ) )

		return obj

class Apply ( object ) :

	def __init__ ( self , problem ) : pass

	def __call__ ( self , solution , mutation ) :

		apply( solution , mutation )

def apply ( solution , mutation ) :

	groups = solution.groups
	rows = solution.rows

	ax , ay = mutation

	rows[ax.interval.row][ax.group] -= ax.server.capacity
	rows[ay.interval.row][ay.group] -= ay.server.capacity

	groups[ax.group] -= ax.server.capacity
	groups[ay.group] -= ay.server.capacity

	ax.server , ay.server = ay.server , ax.server
	ax.group , ay.group = ay.group , ax.group

	rows[ax.interval.row][ax.group] += ax.server.capacity
	rows[ay.interval.row][ay.group] += ay.server.capacity

	groups[ax.group] += ax.server.capacity
	groups[ay.group] += ay.server.capacity

