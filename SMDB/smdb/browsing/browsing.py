from django_rdf import graph
from rdflib import Literal, URIRef

from smdb.semantic_models import *
from smdb.utils import merge_results


def browse_movies(year, director, genre, location, rating):
	initBindings = {}
	
	f = Movie.getFilterList(year, director, genre, location, rating)
	
	query = """SELECT ?a ?b ?y WHERE {
				?a rdf:type smdb:Movie .
				?a smdb:title ?b .
				?a smdb:releaseDate ?y .
				"""
	
	# Query additions
	if director: query += '?d smdb:directed ?a .\n'
	if genre: query += '?a smdb:isOfGenre ?g .\n'
	if location: query += '?a smdb:shotIn ?l .\n'
	if rating: query += '?a smdb:hasRating ?r .\n'
	
	# Filters	
	if year: query += """FILTER(?y = "%s") .\n""" % Literal(year)
	if director: query += """FILTER(?d = <%s>) .\n""" % URIRef(director)
	if genre: query += """FILTER(?g = <%s>) .\n""" % graph.ontologies['smdb'][genre]
	if location: query += """FILTER(?l = "%s") .\n""" % Literal(location)
	if rating: query += """FILTER(?r = <%s>) .\n""" % URIRef(rating)
	
	res = graph.query(query + "} ORDER BY ?y", initBindings=initBindings)
	
	return [f, res]

def browse_people(occupations):
	initBindings = {}
	
	occupationToQuery = { 'writer': '?u smdb:wrote ?m1 .\n',
						  'actor': '?u smdb:performedIn ?m2 .\n',
						  'director': '?u smdb:directed ?m3 .\n',
						}
	
	
	f = Person.getFilterList(occupations)
	
	query = """SELECT DISTINCT ?u ?n WHERE {
				?u rdf:type smdb:Person .
				?u smdb:name ?n .
				"""
	
	for o in occupations:
		if o in occupationToQuery: query += occupationToQuery[o]
	
	res = graph.query(query + "}", initBindings=initBindings)
	return [f, res]
	
def browse_users(filters, user):
	userUri = URIRef(user.get_profile().uri)
	
	initBindings = {}
	
	filterToQuery = { 'similar': '<%s> smdb:hasSeen ?m1 .\n ?u smdb:hasSeen ?m1 .\n' % userUri,
					  'foaf': '<%s> smdb:isFriendsWith ?u1 .\n ?u smdb:isFriendsWith ?u1 .\n' % userUri,
					  'reviewer': '?r1 smdb:writtenByUser ?u .\n',
					}
	
	f = SMDBUser.getFilterList(user.is_authenticated(), filters)
	
	query = """SELECT DISTINCT ?u ?m1 ?u1 WHERE {
				?u rdf:type smdb:SMDBUser .
				?u smdb:username ?un . 
			"""
	
	for o in filters:
		if o in filterToQuery: query += filterToQuery[o]
	
	if 'similar' in filters or 'foaf' in filters: query += """FILTER(?u != <%s>) .\n""" % userUri
	
	res = graph.query(query + "OPTIONAL { ?u smdb:fullName ?fn . }}", initBindings=initBindings)
	res = merge_results(res)
	
	return [f, res]