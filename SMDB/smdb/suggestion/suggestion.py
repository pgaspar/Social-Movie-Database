from django_rdf import graph
from smdb.utils import sort_by_count
from rdflib import Literal, URIRef
from pprint import pprint

def movies_of_the_year():
	pass
	
def popular_movies():
				
	res = graph.query("""SELECT ?m ?t ?u WHERE {
				?m rdf:type smdb:Movie .
				?m smdb:title ?t .
				OPTIONAL{ ?u smdb:hasSeen ?m . }
				}""", initBindings={})
	
	#pprint(res)
	
	sorted_res = sort_by_count(res, [0,1], 2)
	sorted_res = sorted_res[:5]
	sorted_res = [ el[0] + (el[1],) for el in sorted_res ]	# Flatten the results so that it's (uri, title, score)
	
	#pprint(sorted_res)
	
	return sorted_res
	
def seen_by_friends(request):
	pass
	
def recommended_movies(request):
	
	userURI = request.user.get_profile().uri
	related = dict()
	
	#favGenres = get_favorite_genres(userURI)
	#favDirectors = get_favorite_directors(userURI)
	#favWriters = get_favorite_writers(userURI)
	print userURI
	#userURI = URIRef("/user/pgaspar/")
	
	query = """SELECT DISTINCT ?m ?f ?u WHERE {
						?m rdf:type smdb:Movie .
						OPTIONAL{ ?f smdb:hasSeen ?m .
								  ?f smdb:isFriendsWith <%s> .
								  } .
						OPTIONAL{ ?u smdb:hasSeen ?m .
								  FILTER( ?u = <%s>) . 
								  } .
						}""" % (userURI, userURI)
	
	print query
	
	notSeen = graph.query(query)
	
	for movie in notSeen:
		if not movie[2]:
			if movie[0] in related.keys():
				related[movie[0]] += 1
			else:
				if movie[1]:
					related[movie[0]] = 1
				else:
					related[movie[0]] = 0
	
	for movie in zip(related.keys(), related.values()):
		print movie
	
	genreQuery = """SELECT DISTINCT ?m ?g WHERE {
					?m rdf:type smdb:Movie . 
					?m smdb:isOfGenre ?g . 
					}"""
					
	allGenres = graph.query(genreQuery)	
	
	
	directorQuery = """SELECT DISTINCT ?m ?p WHERE {
					?m rdf:type smdb:Movie .
					?p smdb:directed ?m .
					}"""
	
	allDirectors = graph.query(directorQuery)
	
	
	writerQuery = """SELECT DISTINCT ?m ?p WHERE {
					?m rdf:type smdb:Movie .
					?p smdb:wrote ?m .
					}"""
	
	allDirectors = graph.query(writerQuery)
	
	return None
	
	for movie in allGenres:
		if movie[1] in favGenres.keys() and movie[0] in related.keys():
			related[movie[0]] += favGenres[movie[1]]
	
	for movie in allDirectos:
		if movie[1] in favDirectors.keys() and movie[0] in related.keys():
			related[movie[0]] += favDirectors[movie[1]]

	for movie in allGenres:
		if movie[1] in favWriters.keys() and movie[0] in related.keys():
			related[movie[0]] += favWriters[movie[1]]
	
	
	
	related = zip(related.keys(), related.values())
	
	sortedResults = sorted(related, key = lambda pair : pair[1] )
	
	for result in sortedResults:
		print result
