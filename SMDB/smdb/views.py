from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django_rdf import graph

from smdb.semantic_models import *
from smdb import manager

from rdflib import Literal

def render(request,template,context={}):
	return render_to_response(template,context,context_instance=RequestContext(request))


def test(request):
	
	res = graph.query("""SELECT ?a ?b ?c WHERE {
				?a rdf:type smdb:Movie .
				?a smdb:title ?b .
				?a smdb:slug ?c .
			}""")
	
	return render(request, 'test.html', {'movie_list': res})
	
def movie_detail(request, slug):
	
	uri = graph.query_single("""SELECT ?u WHERE {
				?u rdf:type smdb:Movie .
				?u smdb:slug ?s .
			}""", initBindings={'s': Literal(slug)})
	
	movie = Movie(uri)
	
	return render(request, 'movie.html', {'movie': movie})
	
def user_detail(request, username):
	
	uri = graph.query_single("""SELECT ?u WHERE {
				?u rdf:type smdb:SMDBUser .
				?u smdb:username ?a .
			}""", initBindings={'a': Literal(username)})
	
	user = SMDBUser(uri)
	
	return render(request, 'user.html', {'user': user})