#!/usr/bin/env python
# encoding: utf-8
"""
search.py

Created by Miguel Tavares on 2011-01-03.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os


class Search:
	
	def __init__(self, graph):
		self.graph = graph


	def keywordSearch(self, keyword):
		
		movieList = self.movieSearch(keyword)
		personList = self.personSearch(keyword)
		charList = self.characterList(keyword)
		
		if(movieList and not personList and not charList):
			personList = self.personSearch(None, keyword)
			charList = self.characterSearch(None, keyword)
			
		if(not movieList and (personList or charList)):
			movieList = self.movieSearch(None, keyword)
		
		return (movieList, personList, charList)
		
	
	def semanticSearch(self, sentence):
		pass
		
	
	def personSearch(self, name, movie = None):
		
		keyword = name if name else movie
		
		query = """SELECT ?a ?b ?l ?n WHERE{
					?a rdf:type smdb:Person .
					?a smdb:name ?b .
					"""
		if movie:
			query += """?a ?r ?m .
						?r rdfs:subPropertyOf smdb:participatedInMovie .
						?m smdb:title ?n ."""
		
		
	def characterSearch(self, name, movie = None):
		pass
		
		
	def movieSearch(self, title, person = None):
		
		keyword = title if title else person
		

		query = """SELECT DISTINCT ?a ?b ?d ?l ?n WHERE{
						?a rdf:type smdb:Movie .
						?a smdb:title ?b .
						?a smdb:releaseDate ?d .
						"""
		if person:
			query += """?p ?r ?a .
						?r rdfs:subPropertyOf smdb:participatedInMovie .
						?r owl:inverseOf ?r2 .
						?r2 rdfs:label ?l .
						?p rdf:type smdb:Person .
						?p smdb:name ?n .
						"""
		
		var = '?b' if title else '?n'	
		query += 'FILTER( regex(str('+ var +'), "%s", "i") ) .' % keyword
		
		print query
		
		movies = self.graph.query(query + '} ORDER BY ?a')
		
		
		#Stupid hack to make everything look better =D
		if person:
			prev = [None]
			distinctMovies = []
			for movie in movies:
				#Go through the movies, looking for duplicates
				if prev[0] == movie[0]:
					prev[3].append(movie[3])
					prev[4].append(movie[4])
				else:
					if prev[0]:
						distinctMovies.append(prev)
					prev = list(movie)
					prev[3] = [prev[3]]
					prev[4] = [prev[4]]
			#Another silliness to avoid the last one not being included
			if prev not in distinctMovies and prev[0]:
				distinctMovies.append(prev)
			
			print distinctMovies
			
			return distinctMovies
			
		else:
			return movies
		