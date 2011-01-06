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
		
		print '[Searching Movies]'
		movieList = self.movieSearch(keyword)
		print '[Searching People]'
		personList = self.personSearch(keyword)
		print '[Searching Characters]'
		charList = self.characterSearch(keyword)
		
		if(movieList and not personList):
			print '[No people found, searching based on movies]'
			personList = self.personSearch(None, keyword)
		
		if(movieList and not charList):
			print '[No characters found, searching based on movies]'
			charList = self.characterSearch(None, keyword)	
		
		if(not movieList and (personList or charList)):
			print '[No movies found, searching based on people]'
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
						?r rdfs:label ?l .
						?m smdb:title ?n ."""
		
		var = '?b' if name else '?n'	
		query += 'FILTER( regex(str('+ var +'), "%s", "i") ) .' % keyword
		
		#print query
		
		people = self.graph.query(query + '} ORDER BY ?a')
		
		
		#Stupid hack to make everything look better =D
		if movie:
			prev = [None]
			distinctPeople = []
			for person in people:
				#Go through the movies, looking for duplicates
				if prev[0] == person[0]:
					prev[2].append(person[2])
					prev[3].append(person[3])
				else:
					if prev[0]:
						prev[2] = zip(prev[2],prev[3])
						prev.pop(3)
						distinctPeople.append(prev)
	
					prev = list(person)
					prev[2] = [prev[2]]
					prev[3] = [prev[3]]
					
			#Another silliness to avoid the last one not being included
			if prev not in distinctPeople and prev[0]:
				prev[2] = zip(prev[2],prev[3])
				prev.pop(3)
				distinctPeople.append(prev)
				
			
			#print distinctMovies
			
			return distinctPeople
			
		else:
			return people
		
		
	def characterSearch(self, name, movie = None):
		keyword = name if name else movie
		
		query = """SELECT ?a ?b ?l ?n WHERE{
					?a rdf:type smdb:Character .
					?a smdb:name ?b .
					"""
		if movie:
			query += """?a smdb:inMovie ?m.
						smdb:inMovie rdfs:label ?l .
						?m smdb:title ?n ."""
		
		var = '?b' if name else '?n'	
		query += 'FILTER( regex(str('+ var +'), "%s", "i") ) .' % keyword
		
		#print query
		
		chars = self.graph.query(query + '} ORDER BY ?a')
		
		
		#Stupid hack to make everything look better =D
		if movie:
			prev = [None]
			distinctChars = []
			for char in chars:
				#Go through the movies, looking for duplicates
				if prev[0] == char[0]:
					prev[2].append(char[2])
					prev[3].append(char[3])
				else:
					if prev[0]:
						prev[2] = zip(prev[2],prev[3])
						prev.pop(3)
						distinctChars.append(prev)
						
					prev = list(char)
					prev[2] = [prev[2]]
					prev[3] = [prev[3]]
					
			#Another silliness to avoid the last one not being included
			if prev not in distinctChars and prev[0]:
				prev[2] = zip(prev[2],prev[3])
				prev.pop(3)
				distinctChars.append(prev)
				
			
			#print distinctMovies
			
			return distinctChars
			
		else:
			return chars
		
		
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
						?r owls:inverseOf ?r2 .
						?r2 rdfs:label ?l .
						?p smdb:name ?n .
						"""
		
		var = '?b' if title else '?n'	
		query += 'FILTER( regex(str('+ var +'), "%s", "i") ) .' % keyword
		
		#print query
		
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
						prev[3] = zip(prev[3],prev[4])
						prev.pop(4)
						distinctMovies.append(prev)
						
					prev = list(movie)
					prev[3] = [prev[3]]
					prev[4] = [prev[4]]
			#Another silliness to avoid the last one not being included
			if prev not in distinctMovies and prev[0]:
				prev[3] = zip(prev[3],prev[4])
				prev.pop(4)
				distinctMovies.append(prev)
				
			
			#print distinctMovies
			
			return distinctMovies
			
		else:
			return movies
		