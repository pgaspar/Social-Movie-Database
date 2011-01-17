from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404 as django_get_object_or_404
from django.contrib.auth.models import User

from django.conf import settings
from django.contrib.auth.decorators import login_required

from django_rdf import graph
from rdflib import Literal, URIRef

from smdb.semantic_models import *
from smdb import manager

from smdb.browsing import browsing
from smdb.searching.search import Search
from smdb.suggestion import suggestion

from smdb.utils import split_array

# Util Functions

def render(request,template,context={}):
	return render_to_response(template,context,context_instance=RequestContext(request))

def get_object_or_404(Model, uri):
	try: return Model(uri)
	except TypeError: raise Http404
	
# User related

@login_required
def redirect_to_profile(request):
	return HttpResponseRedirect('/user/' + request.user.username)

@login_required
def mark_seen(request, movieURI):
	movieURI = '/' + movieURI
	
	movie = get_object_or_404(Movie, movieURI)
	movie.markSeen(request.user)
	
	return HttpResponseRedirect(movieURI)

@login_required
def add_friend(request, userURI):
	userURI = '/' + userURI
	
	user = get_object_or_404(SMDBUser, userURI)
	user.addFriend(request.user)
	
	return HttpResponseRedirect(userURI)

@login_required
def remove_friend(request, userURI):
	userURI = '/' + userURI
	
	user = get_object_or_404(SMDBUser, userURI)
	user.removeFriend(request.user)
	
	return HttpResponseRedirect(userURI)

@login_required
def add_review(request, movieURI):
	movieURI = '/' + movieURI
	
	if request.method != 'POST': raise Http404
	
	text = request.POST.get('text')
	revID = int(request.POST.get('rev_ID'))
	
	if not text or not revID: raise Http404
	
	movie = get_object_or_404(Movie, movieURI)
	movie.addReview(request.user, revID, text)
	
	return HttpResponseRedirect(movieURI + '#review-' + str(revID))


# Index Page

def index(request):
	context = {}
	
	# Fetch the Movies of the Year section
	context['movies_of_the_year'] = suggestion.movies_of_the_year()
	
	# Fetch the Popular Movies section
	context['popular_movies'] = suggestion.popular_movies()
	
	if request.user.is_authenticated():
		
		# Fetch the Seen by Friends section
		context['seen_by_friends'] = suggestion.seen_by_friends(request)
		
		# Fetch the Recommended Movies section
		context['recommended_movies'] = suggestion.recommended_movies(request)
		
		# Fetch the Recommended Users section
		context['recommended_users'] = suggestion.recommended_users(request)
		
	return render(request, 'index.html', context)

# Detail Pages

def movie_detail(request, slug):
	
	uri = request.path
	
	movie = get_object_or_404(Movie, uri)
	
	suggested = suggestion.movie_suggestions(uri)
	
	return render(request, 'movie.html', {'movie': movie, 'suggestions': suggested})
	
def user_detail(request, username):
	
	uri = request.path
	user = get_object_or_404(SMDBUser, uri)
	django_user = django_get_object_or_404(User, username=username)
	
	return render(request, 'user.html', {'user': user, 'd_user': django_user})
	
def person_detail(request, slug):
	
	uri = request.path
	person = get_object_or_404(Person, uri)
	
	suggested = suggestion.person_suggestions(uri)
	
	return render(request, 'person.html', {'person': person, 'suggestions': suggested})
	
def character_detail(request, slug):
	
	uri = request.path
	character = get_object_or_404(Character, uri)
	
	return render(request, 'character.html', {'character': character})
	

# Browsing

def browse_movies(request):
	
	year = request.GET.get('year', None)
	director = request.GET.get('director', None)
	genre = request.GET.get('genre', None)
	location = request.GET.get('location', None)
	rating = request.GET.get('rating', None)
	
	print 'Year:', year; print 'Director:', director; print 'Genre:', genre; print 'Location:', location; print 'Rating:', rating
	
	f, res = browsing.browse_movies(year, director, genre, location, rating)
	count = len(res)
	
	return render(request, 'browsing/movies.html', {'filter_list':f, 'result_list': split_array(res, settings.ITEMS_PER_PAGE), 'res_count': count})
	
def browse_people(request):
	
	occupations = [ s.lower() for s in request.GET.getlist('occupations') ]
	
	print 'Occupations:', occupations
	
	f, res = browsing.browse_people(occupations)
	count = len(res)
	
	return render(request, 'browsing/people.html', {'filter_list':f, 'result_list': split_array(res, settings.ITEMS_PER_PAGE), 'res_count': count})
	
def browse_users(request):
	
	filters = [ s.lower() for s in request.GET.getlist('filters') ]
	
	print 'Filters:', filters
	
	f, res = browsing.browse_users(filters, request.user)
	count = len(res)
	
	return render(request, 'browsing/users.html', {'filter_list':f, 'result_list': split_array(res, settings.ITEMS_PER_PAGE), 'res_count': count})



# Searching

def search(request):
	
	searchString = request.GET.get('find', None)
	
	searcher = Search(graph)
	
	semanticResults = searcher.semanticSearch(searchString)
	(movies, people, chars)  = searcher.keywordSearch(searchString)
	
	return render(request, 'search.html', {'semantic_list': split_array(semanticResults, settings.ITEMS_PER_PAGE),'movie_list': split_array(movies, settings.ITEMS_PER_PAGE), 'person_list': split_array(people, settings.ITEMS_PER_PAGE), 'char_list': split_array(chars, settings.ITEMS_PER_PAGE)})
