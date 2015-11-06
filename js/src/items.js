
export class Server {

	constructor ( id , capacity , size ) {

		this.id = id ;
		this.capacity = capacity ;
		this.size = size ;

	}

}

export class Interval {

	constructor ( id , row , start , size ) {

		this.id = id ;
		this.row = row ;
		this.start = start ;
		this.size = size ;

	}

}

export class Affectation {

	constructor ( server , interval , position , group = 0 ) {

		this.server = server ;
		this.interval = interval ;
		this.position = position ;
		this.group = group ;

	}

}


export class Problem {

	/**
	 * @param R number of rows
	 * @param S number of slots per row
	 * @param U number of unusable slots
	 * @param P number of ....
	 * @param M number of servers (Machines)
	 */
	constructor ( R , S , U , P , M , intervals , servers , rows ) {

		this.R = R ;
		this.S = S ;
		this.U = U ;
		this.P = P ;
		this.M = M ;
		this.intervals = intervals ;
		this.servers = servers ;
		this.rows = rows ;

	}

}


export class Solution {

	constructor ( affectations , groups , rows , objective ) {

		this.affectations = affectations ;
		this.groups = groups ;
		this.rows = rows ;
		this.objective = objective ;

	}

}


