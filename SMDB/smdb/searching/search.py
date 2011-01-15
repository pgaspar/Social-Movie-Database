#!/usr/bin/env python
# encoding: utf-8
"""
search.py

Created by Miguel Tavares on 2011-01-03.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from nltk import stem, pos_tag, word_tokenize
from copy import deepcopy

class Search:
	
	def __init__(self, graph):
		self.graph = graph


	def keywordSearch(self, keyword):
		
		print '[Searching Movies]'
		movieList = self.movieSearch(keyword)
		print '[Found %d movies]'%len(movieList)
		
		filtered = keyword
		stopwords = ['who', 'is', 'what', 'it', 'be']
		for word in stopwords:
			filtered = filtered.replace(word, "")
		
		print '[Searching People]'
		personList = self.personSearch(filtered)
		print '[Found %d people]'%len(personList)
		
		print '[Searching Characters]'
		charList = self.characterSearch(keyword)
		print '[Found %d characters]'%len(charList)
		
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
			
	
	def semanticSearch(self, sentence):
		
		stopwords = ['the','in', 'on', 'by', 'is', 'of']
		
		sentence = sentence.lower()
		
		stemmer = stem.porter.PorterStemmer()
		
		#Split the sentence up in words
		words = word_tokenize(sentence)
		words = [word for word in words if word not in stopwords]
		
		if len(words) <= 1:
			return None
		
		#Tag to identify triples
		tagged = pos_tag(words)
		tagged2 = deepcopy(tagged)
		
		subject = ""
		verb = ""
		obj = ""
		
		#One of the options, based on the tags, second option follows
		while not tagged[0][1].startswith('V'):
			subject += stemmer.stem(tagged.pop(0)[0]) + " "
		subject = subject.strip()
		
		while tagged[0][1].startswith('V'):
			verb += stemmer.stem(tagged.pop(0)[0]) + " "
		verb = verb.strip()
		
		if verb != "":
			for tag in tagged:
				obj += tag[0] + " "
			obj = obj.strip()
		else:
			subject = stemmer.stem(words[0])
			obj = " ".join(words[1:])
		
		print subject + ":::" + verb + ":::" + obj
		
		query = """SELECT DISTINCT ?s ?n ?v ?o WHERE{
					?s ?v ?uri .
					?s rdfs:label ?n.
					OPTIONAL {?uri rdfs:label ?o .} .
					OPTIONAL {?uri rdfs:name ?o } .
					OPTIONAL {?uri rdfs:title ?o } .
				"""
		
		if subject:
			query += """FILTER( regex(str(?n), "%s", "i") ) .
					"""%(subject)
					
		if verb:
			query += """?v rdfs:label ?prop .
						FILTER( regex(str(?prop), "%s", "i") ) .
					"""%(verb)
					
		query += """FILTER( regex(str(?o), "%s", "i") ) .
					}
				"""%(obj)
		
		results = self.graph.query(query)
		
		print len(results)
		
		if not results and (len(words) >=3) :
			#Second option, taking only first arg as subject, second arg as verb
			subject = stemmer.stem(tagged2.pop(0)[0])
			verb = stemmer.stem(tagged2.pop(0)[0])
			rest = [tag[0] for tag in tagged2]
			obj = " ".join(rest)
		
			print subject + ":::" + verb + ":::" + obj
		
		return results