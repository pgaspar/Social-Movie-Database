from django_rdf import graph
from smdb.utils import sort_by_count
from rdflib import Literal, URIRef

from smdb.semantic_models import SMDBUser

from pprint import pprint
import datetime

def movie_suggestions(uri):
	
	related = dict()
	titles = dict()
	
	query = """SELECT DISTINCT ?m ?t ?g WHERE{
				<%s> smdb:isOfGenre ?g .
				?m smdb:isOfGenre ?g .
				?m smdb:title ?t .
				FILTER( ?m != <%s> ).
				}
			""" % (uri,uri)


	sameGenre = graph.query(query)
	
	for movie in sameGenre:
		if movie[0] in related.keys():
			related[movie[0]] += 1
		else:
			related[movie[0]] = 1
			titles[movie[0]] = movie[1]
	
	query = """SELECT DISTINCT ?m ?p ?t WHERE{
				?p ?r1 <%s> .
				?p ?r ?m .
				?m smdb:title ?t .
				?r rdfs:subPropertyOf smdb:participatedInMovie .
				?r1 rdfs:subPropertyOf smdb:participatedInMovie .
				FILTER( ?m != <%s> ) .
				}
			""" % (uri, uri)
	
			
	samePeople = graph.query(query)
	
	
	for movie in samePeople:
		if movie[0] in related.keys():
			related[movie[0]] += 1
		else:
			related[movie[0]] = 1
			titles[movie[0]] = movie[2]
	
	
	results = [ [uri, titles[uri], related[uri]] for uri in related.keys() ]
	
	sortedResults = sorted(results, key = lambda pair : pair[2], reverse = True )
	
	#for result in sortedResults:
	#	print result
		
	return sortedResults[:5]


def person_suggestions(uri):
	
	score = dict()
	name = dict()
	
	query = """SELECT DISTINCT ?p ?n ?m WHERE {
				?m rdf:type smdb:Movie .
				<%s> ?r ?m .
				?r rdfs:subPropertyOf smdb:participatedInMovie .
				?p ?r1 ?m .
				?r1 rdfs:subPropertyOf smdb:participatedInMovie .
				?p smdb:name ?n .
				FILTER( ?p != <%s> ) .
			}
			""" % (uri,uri)
	
	relatedPeople = graph.query(query)
	
	for person in relatedPeople:
		if person[0] in score.keys():
			score[person[0]] += 1
		else:
			score[person[0]] = 1
			name[person[0]] = person[1]
		
	
	results = [ [uri, name[uri], score[uri]] for uri in score.keys() ]
	
	sortedResults = sorted(results, key = lambda pair : pair[2], reverse = True )
	
	#for result in sortedResults[:5]:
	#	print results
	
	return sortedResults[:5]


def movies_of_the_year():
	# This is popular_movies filtered by the current year
	
	year = datetime.datetime.now().year
	
	res = graph.query("""SELECT ?m ?t ?u WHERE {
				?m rdf:type smdb:Movie .
				?m smdb:title ?t .
				?m smdb:releaseDate "%s" .
				OPTIONAL{ ?u smdb:hasSeen ?m . }
				}""" % Literal(year), initBindings={})
	
	#pprint(res)
	
	sorted_res = sort_by_count(res, [0,1], 2)
	sorted_res = sorted_res[:5]
	sorted_res = [ el[0] + (el[1],) for el in sorted_res ]	# Flatten the results so that it's (uri, title, score)
	
	#pprint(sorted_res)
	
	return sorted_res
	
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
	
	userUri = URIRef( request.user.get_profile().uri )
	
	seen_by_me = graph.query("""SELECT ?m WHERE {
				?me smdb:hasSeen ?m .
				}""", initBindings={'me': userUri})
	
	res = graph.query("""SELECT ?m ?t ?f WHERE {
				?m rdf:type smdb:Movie .
				?m smdb:title ?t .
				?f smdb:hasSeen ?m .
				?f smdb:isFriendsWith ?me .
				}""", initBindings={'me': userUri})
	
	#pprint(res)
	
	res = [ (m, t, f) for (m, t, f) in res if m not in seen_by_me]
	
	sorted_res = sort_by_count(res, [0,1], 2)
	sorted_res = sorted_res[:5]
	sorted_res = [ el[0] + (el[1],) for el in sorted_res ]	# Flatten the results so that it's (uri, title, friend, score)
	
	#pprint(sorted_res)
	
	return sorted_res
	
def recommended_movies(request):
	
	userURI = request.user.get_profile().uri
	related = dict()
	titles = dict()
	
	favGenres = get_favorite_genres(userURI)
	favDirectors = get_favorite_directors(userURI)
	favWriters = get_favorite_writers(userURI)
	
	#for director in zip(favDirectors.keys(), favDirectors.values()): print director
		
	#for writer in zip(favWriters.keys(), favWriters.values()): print writer
			
	#for genre in zip(favGenres.keys(), favGenres.values()): print genre
	
	query = """SELECT DISTINCT ?m ?f ?u ?t WHERE {
						?m rdf:type smdb:Movie .
						?m smdb:title ?t .
						OPTIONAL{ ?f smdb:hasSeen ?m .
								  ?f smdb:isFriendsWith <%s> .
								  } .
						OPTIONAL{ ?u smdb:hasSeen ?m .
								  FILTER( ?u = <%s>) . 
								  } .
						}""" % (userURI, userURI)
	
	#print query
	
	notSeen = graph.query(query)
	
	for movie in notSeen:
		if not movie[2]:
			if movie[0] in related.keys():
				related[movie[0]] += 1
			else:
				titles[movie[0]] = movie[3]
				if movie[1]:
					related[movie[0]] = 1
				else:
					related[movie[0]] = 0
	
	#for movie in zip(related.keys(), related.values()):
	#	print movie
	
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
	
	
	for movie in allGenres:
		if movie[1] in favGenres.keys() and movie[0] in related.keys():
			related[movie[0]] += favGenres[movie[1]]
	
	for movie in allDirectors:
		if movie[1] in favDirectors.keys() and movie[0] in related.keys():
			related[movie[0]] += favDirectors[movie[1]]

	for movie in allGenres:
		if movie[1] in favWriters.keys() and movie[0] in related.keys():
			related[movie[0]] += favWriters[movie[1]]
	
	
	
	results = [ [uri, titles[uri], related[uri]] for uri in related.keys() ]
	
	sortedResults = sorted(results, key = lambda pair : pair[2], reverse = True )
	
	#for result in sortedResults: print result
		
	return sortedResults[:5]


def recommended_users(request):
	userUri = URIRef(request.user.get_profile().uri)
	
	friends = graph.query("""SELECT ?u WHERE {
					?u smdb:isFriendsWith ?me .
					}""", initBindings={'me': userUri})

	res = graph.query("""SELECT ?u ?f WHERE {
					?u rdf:type smdb:SMDBUser .
					?u smdb:hasSeen ?m .
					?me smdb:hasSeen ?m .
					OPTIONAL{ ?me smdb:isFriendsWith ?f . ?u smdb:isFriendsWith ?f } .
					FILTER( ?u != ?me) .
					}""", initBindings={'me': userUri})
					

	res = [ (SMDBUser(u), f) for (u, f) in res if u and u not in friends]
	
	sorted_res = sort_by_count(res, [0], 1)
	sorted_res = sorted_res[:4]
	sorted_res = [ el[0] + (el[1],) for el in sorted_res ]	# Flatten the results so that it's (uri, title, friend, score)
	
	#for r in sorted_res: print r
	
	return sorted_res
	
	
# Helper methods

def get_favorite_genres(user):
	res = dict()
	
	query = """SELECT DISTINCT ?m ?g WHERE{
				?m rdf:type smdb:Movie .
				<%s> smdb:hasSeen ?m .
				?m smdb:isOfGenre ?g .
				}""" % user
				
	genres = graph.query(query)
	
	for genre in genres:
		if genre[1] in res.keys():
			res[genre[1]] += 1
		else:
			res[genre[1]] = 1
	
	return res


def get_favorite_directors(user):
	res = dict()

	query = """SELECT DISTINCT ?m ?p WHERE{
				?m rdf:type smdb:Movie .
				<%s> smdb:hasSeen ?m .
				?p smdb:directed ?m .
				}""" % user

	directors = graph.query(query)

	for director in directors:
		if director[1] in res.keys():
			res[director[1]] += 1
		else:
			res[director[1]] = 1

	return res

def get_favorite_writers(user):
	res = dict()

	query = """SELECT DISTINCT ?m ?p WHERE{
				?m rdf:type smdb:Movie .
				<%s> smdb:hasSeen ?m .
				?p smdb:wrote ?m .
				}""" % user

	writers = graph.query(query)

	for writer in writers:
		if writer[1] in res.keys():
			res[writer[1]] += 1
		else:
			res[writer[1]] = 1

	return res
