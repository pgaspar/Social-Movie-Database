from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import Http404

from django_rdf import graph
from rdflib import Literal, URIRef

from smdb.semantic_models import *
from smdb import manager

from smdb.searching.search import Search

from smdb.utils import split_array
from django.conf import settings

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
	genre = request.GET.get('genre', None)
	location = request.GET.get('location', None)
	rating = request.GET.get('rating', None)
	
	print 'Year:', year; print 'Director:', director; print 'Genre:', genre; print 'Location:', location; print 'Rating:', rating
	
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
	count = len(res)
	
	return render(request, 'browsing/movies.html', {'filter_list':f, 'result_list': split_array(res, settings.ITEMS_PER_PAGE), 'res_count': count})
	
def browse_people(request):
	
	initBindings = {}
	
	occupationToQuery = { 'writer': '?u smdb:wrote ?m1 .\n',
						  'actor': '?u smdb:performedIn ?m2 .\n',
						  'director': '?u smdb:directed ?m3 .\n',
						}
	
	occupations = [ s.lower() for s in request.GET.getlist('occupations') ]
	
	print 'Occupations:', occupations
	
	f = Person.getFilterList(occupations)
	
	query = """SELECT DISTINCT ?u ?n WHERE {
				?u rdf:type smdb:Person .
				?u smdb:name ?n .
				"""
	
	for o in occupations:
		if o in occupationToQuery: query += occupationToQuery[o]
	
	res = graph.query(query + "}", initBindings=initBindings)
	count = len(res)
	
	return render(request, 'browsing/people.html', {'filter_list':f, 'result_list': split_array(res, settings.ITEMS_PER_PAGE), 'res_count': count})
	

# Searching

def search(request):
	
	searchString = request.GET.get('find', None)
	
	searcher = Search(graph)
	
	movies = None #searcher.movieSearch(None, searchString)
	people = searcher.personSearch(None, searchString)
	
	return render(request, 'search.html', {'movie_list': movies, 'person_list': people})
	
	query = """SELECT ?a ?b ?d WHERE{
				?a rdf:type smdb:Movie .
				?a smdb:title ?b .
				?a smdb:releaseDate ?d .
				"""
				
	if searchString: query += 'FILTER( regex(str(?b), "%s", "i") ) .' %searchString
	
	movies = graph.query(query + '}')
	
	query = """SELECT ?a ?b WHERE{
				?a rdf:type smdb:Person .
				?a smdb:name ?b .
				"""
				
	if searchString: query += 'FILTER( regex(str(?b), "%s", "i") ) .' %searchString
	
	people = graph.query(query + '}')
	
	if movies and not people:
		
		query = """SELECT DISTINCT ?a ?b WHERE{
				?a rdf:type smdb:Person .
				?a smdb:name ?b .
				?a smdb:performedIn ?m .
				"""
		if searchString: query += 'FILTER( regex(str(?m), "%s", "i") ) .' %searchString	
	
		people = graph.query(query + '}')
				
	elif people and not movies:
		print "Searching directed by"
		print people
		query = """SELECT DISTINCT ?a ?b ?d WHERE{
				?a rdf:type smdb:Movie .
				?a smdb:title ?b .
				?a smdb:releaseDate ?d .
				?p smdb:directed ?a .
				?p rdf:type smdb:Person .
				?p smdb:name ?n .
				"""
				
		if searchString: query += 'FILTER( regex(str(?n), "%s", "i") ) .' %searchString	
	
		movies = graph.query(query + '}')
	
	return render(request, 'search.html', {'movie_list': movies, 'person_list': people})