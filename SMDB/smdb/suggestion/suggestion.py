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
	
	pprint(sorted_res[:5])
				
	return sorted_res[:5]
	
def seen_by_friends(request):
	pass
	
def recommended_movies(request):
	pass