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
		movieList = self.movieSearch(keyword.replace(" ",".*?"))
		print '[Found %d movies]'%len(movieList)
		
		filtered = keyword
		stopwords = ['who', 'is', 'what', 'it', 'be']
		for word in stopwords:
			filtered = filtered.replace(word, "")
		
		filtered = filtered.strip()
		
		print '[Searching People] '  + filtered
		personList = self.personSearch(filtered.replace(" ",".*?"))
		print '[Found %d people]'%len(personList)
		
		print '[Searching Characters]'
		charList = self.characterSearch(keyword.replace(" ",".*?"))
		print '[Found %d characters]'%len(charList)
		
		if(movieList and not personList):
			print '[No people found, searching based on movies]'
			personList = self.personSearch(None, keyword.replace(" ",".*?"))
		
		if(movieList and not charList):
			print '[No characters found, searching based on movies]'
			charList = self.characterSearch(None, keyword.replace(" ",".*?"))	
		
		if(not movieList and (personList or charList)):
			print '[No movies found, searching based on people]'
			movieList = self.movieSearch(None, filtered.replace(" ",".*?"))
		
		
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
		
		stopwords = ['the','in', 'on', 'by', 'is', 'of', 'has']
		
		sentence = sentence.lower()
		
		#TODO : aplly some kind of symNet
		
		#Split the sentence up in words
		words = word_tokenize(sentence)
		words = [word for word in words if word not in stopwords]
		
		if len(words) <= 1:
			return None
		
		(subjects, verbs, obj) =  self.getSearchElements(words)
		
		print str(subjects) + ":::" + str(verbs) + ":::" + str(obj)
		
		if not obj:
			return []
			
		obj = ".*?".join(obj)
		
		if not subjects: subjects = ["stub"]
		
		results = []
		
		for verb in verbs:
			for subject in subjects:
				query = """SELECT DISTINCT ?u ?n ?lprop ?obj ?lobj WHERE {
							?u <%s> ?obj .
							<%s> rdfs:label ?lprop .
							"""%(verb,verb)
							
				if(subject != 'stub'):
					query += '?u rdf:type <%s> .\n'%subject
							
				query += """	OPTIONAL { ?obj smdb:title ?lobj } .
								OPTIONAL { ?obj smdb:name ?lobj } .
								OPTIONAL { ?u smdb:title ?n } .
								OPTIONAL { ?u smdb:name ?n } . 
								FILTER ( regex( str(?obj), "%s", "i") ) .}""" %obj
				
				res = self.graph.query(query)
				
				
				for r in res:
					if not r[0]:
						continue
					if r[4]:
						results.append((r[0],r[1],r[2],r[4]))
					else:
						results.append((r[0],r[1],r[2],r[3]))
	
		return results
	
	def getSearchElements(self, words):
		
		stemmer = stem.porter.PorterStemmer()
		
		
		term_1 = self.translateSpecialCases(words[0])
		term_1 = stemmer.stem(term_1)
		
		term_2 = self.translateSpecialCases(words[1])
		term_2 = stemmer.stem(term_2)
		
		query = """SELECT DISTINCT ?u WHERE{
				?u rdf:type ?p .
				?u rdfs:label ?l .
				FILTER ( regex(str(?p), "%s", "i") ).
				FILTER ( regex(str(?l), "%s", "i") ).
				}"""
		
		queryClass = query%("class", term_1)
		
		classes = self.graph.query(queryClass)
		
		if not classes:
			queryProp = query%("property", term_1)
			
			props = self.graph.query(queryProp)
			
			if props:
				return (None, props, words[1:])
			else:
				return (None, None, None)
				
		else:
			if len(words) == 2: return (None, None, None)
			
			queryProp = query%("property", term_2)
			
			props = self.graph.query(queryProp)
			
			if props:
				return (classes, props, words[2:])
			else:
				return (None, None, None)
	
	
	def translateSpecialCases(self, word):
		specialCases = {"director" : "directed",
						"writer" : "wrote",
						"acted" : "performed",
						"actor" : "performed",
						"actress" : "performed",
						"date" : "released",
						"location" : "shot",
						"who" : "person"}
						
		if word in specialCases.keys():
			return specialCases[word]
		else:
			return word