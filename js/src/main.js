
import { II , VND , best , first , first_or_equal , first_and_equal } from 'aureooms-js-metaheuristics' ;
import * as parse from 'aureooms-es-parse' ;
import { head , max , frame , range , list } from 'aureooms-js-itertools' ;
import { increasing , attr } from 'aureooms-js-compare' ;

import * as array from 'aureooms-js-array' ;
import * as random from 'aureooms-js-random' ;
import { issorted } from 'aureooms-js-sort' ;

import * as fs from 'fs' ;
import * as read from './read' ;

const data = fs.readFileSync( '../in/dc.in' , 'utf8' ) ;

let stream = parse.from.string( data ) ;
stream = parse.split( stream , ' \t\n' ) ;
stream = parse.map( parse.integer , stream ) ;

let problem = read.problem( parse.to.iterable( stream ) ) ;

/**
 * This test suite sorts a list
 * using different kinds of metaheuristics.
 */
function count_inversions ( solution ) {

	let n = solution.length ;
	let inversions = 0 ;

	for ( let i = 0 ; i < n ; ++i ) {

		for ( let j = i + 1 ; j < n ; ++j ) {

			if ( solution[i] > solution[j] ) inversions += 1 ;

		}

	}

	return inversions ;

}

function evaluate ( solution , mutation ) {

	let i = mutation[0] ;
	let j = mutation[1] ;
	let a = solution.slice( 0 ) ;

	a[i] = solution[j] ;
	a[j] = solution[i] ;

	return -count_inversions( a ) ;

}

function apply ( solution , mutation ) {

	let i = mutation[0] ;
	let j = mutation[1] ;
	let a = solution.slice( 0 ) ;

	let tmp = solution[i] ;
	solution[i] = solution[j] ;
	solution[j] = tmp ;

}

function walk ( solution ) {

	return frame( range( solution.length ) , 2 ) ;

}

function walk_1 ( solution ) {

	return frame( range( solution.length * 2 / 3 | 0 ) , 2 ) ;

}

function walk_2 ( solution ) {

	return frame( range( solution.length / 3 | 0 , solution.length ) , 2 ) ;

}

function init ( n ) {

	let solution = array.alloc( n ) ;
	array.iota( solution , 0 , n , 0 ) ;

	random.shuffle( solution , 0 , n ) ;

	let inversions = count_inversions( solution ) ;

	return [ solution , -inversions ] ;

}

let test_method = function ( name , method ) {

	console.log( 'sorting : ' + name ) ;

	let n = 20 ;

	let candidates = method( init( n ) ) ;

	let output = max( attr( increasing , 1 ) , candidates ) ;

	console.log( '> fitness is 0' , output[1] === 0 ) ;
	console.log( '> solution is sorted' , issorted( increasing , output[0] , 0 , n ) === n ) ;

} ;

test_method( 'II/best' , function ( x ) {
	return II( x , best , walk , evaluate , apply ) ;
} ) ;

test_method( 'II/first' , function ( x ) {
	return II( x , first , walk , evaluate , apply ) ;
} ) ;

test_method( 'II/first_or_equal' , function ( x ) {
	return II( x , first_or_equal , walk , evaluate , apply ) ;
} ) ;

test_method( 'II/first_and_equal' , function ( x ) {
	return II( x , first_and_equal , walk , evaluate , apply ) ;
} ) ;

test_method( 'VND/best' , function ( x ) {
	let neighborhoods = [
		{
			pivoting : best ,
			apply : apply ,
			walk : walk_1 ,
			evaluate : evaluate
		} ,
		{
			pivoting : best ,
			apply : apply ,
			walk : walk_2 ,
			evaluate : evaluate
		}
	] ;
	return VND( x , neighborhoods.length , neighborhoods ) ;
} ) ;

test_method( 'VND/first' , function ( x ) {
	let neighborhoods = [
		{
			pivoting : first ,
			apply : apply ,
			walk : walk_1 ,
			evaluate : evaluate
		} ,
		{
			pivoting : first ,
			apply : apply ,
			walk : walk_2 ,
			evaluate : evaluate
		}
	] ;
	return VND( x , neighborhoods.length , neighborhoods ) ;
} ) ;

test_method( 'VND/first_or_equal' , function ( x ) {
	let neighborhoods = [
		{
			pivoting : first_or_equal ,
			apply : apply ,
			walk : walk_1 ,
			evaluate : evaluate
		} ,
		{
			pivoting : first_or_equal ,
			apply : apply ,
			walk : walk_2 ,
			evaluate : evaluate
		}
	] ;
	return VND( x , neighborhoods.length , neighborhoods ) ;
} ) ;

test_method( 'VND/first_and_equal' , function ( x ) {
	let neighborhoods = [
		{
			pivoting : first_and_equal ,
			apply : apply ,
			walk : walk_1 ,
			evaluate : evaluate
		} ,
		{
			pivoting : first_and_equal ,
			apply : apply ,
			walk : walk_2 ,
			evaluate : evaluate
		}
	] ;
	return VND( x , neighborhoods.length , neighborhoods ) ;
} ) ;

