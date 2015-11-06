
import { head , range , frame } from 'aureooms-js-itertools' ;

import { increasing } from 'aureooms-js-compare' ;

import { Problem , Interval , Server } from './items' ;

export function problem ( tokens ) {

	const [ R , S , U , P , M ] = head( tokens , 5 ) ;

	const rows = [ for ( i of range( R ) ) [ 0 , S ] ] ;

	const servers = [ ] ;

	const intervals = [ ] ;

	for ( const i of range( U ) ) {

		// for each non available emplacement

		const [ r , s ] = head( tokens , 2 ) ;

		rows[r].push( s ) ;

	}

	let id = -1 ;

	for ( const r of range( R ) ) {

		rows[r].sort( increasing ) ;

		for ( const [ left , right ] of frame( rows[r] , 2 ) ) {

				const size = right - left - 1 ;

				if ( size <= 0 ) continue ;

				const interval = new Interval( ++id , r , left , size ) ;

				intervals.push( interval ) ;

		}

	}

	for ( const m of range( M ) ) {

		// for each server

		const [ z , c ] = head( tokens , 2 ) ;

		const server = new Server( m , c , z ) ;

		servers.push( server ) ;

	}

	return new Problem( R , S , U , P , M , intervals , servers , rows ) ;

}
