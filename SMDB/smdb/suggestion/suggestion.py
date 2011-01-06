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
	pass