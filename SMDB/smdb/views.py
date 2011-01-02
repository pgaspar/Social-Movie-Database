from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import Http404

from django_rdf import graph
from rdflib import Literal, URIRef

from smdb.semantic_models import *
from smdb import manager


# Util Functions

def render(request,template,context={}):
	return render_to_response(template,context,context_instance=RequestContext(request))

def get_object_or_404(Model, uri):
	try: return Model(uri)
	except TypeError: raise Http404
	

# Detail Pages

def movie_detail(request, slug):
	
	uri = request.path
	
	movie = get_object_or_404(Movie, uri)
	
	return render(request, 'movie.html', {'movie': movie})
	
def user_detail(request, username):
	
	uri = request.path
	user = get_object_or_404(SMDBUser, uri)
	
	return render(request, 'user.html', {'user': user})
	
def person_detail(request, slug):
	
	uri = request.path
	person = get_object_or_404(Person, uri)
	
	return render(request, 'person.html', {'person': person})
	
def character_detail(request, slug):
	
	uri = request.path
	character = get_object_or_404(Character, uri)
	
	return render(request, 'character.html', {'character': character})
	

# Browsing

def browse_movies(request):
	
	initBindings = {}
	
	year = request.GET.get('year', None)
	director = request.GET.get('director', None)
	
	print 'Year:', year
	print 'Director:', director
	
	f = Movie.getFilterList(year, director)
	
	query = """SELECT ?a ?b ?y WHERE {
				?a rdf:type smdb:Movie .
				?a smdb:title ?b .
				?a smdb:releaseDate ?y .
				"""
	
	if year: query += """ FILTER( ?y = "%s" ) .""" % Literal(year)
	
	if director:
		query += '?d smdb:directed ?a .'
		initBindings.update( {'d': URIRef(director)} )
	
	res = graph.query(query + "}", initBindings=initBindings)
	
	return render(request, 'browse.html', {'f':f, 'movie_list': res})
	
def browse_people(request):
	
	res = graph.query("""SELECT ?a ?b WHERE {
					?a rdf:type smdb:Person .
					?a smdb:name ?b .
				}""")
	
	return render(request, 'browse.html', {'people_list': res})