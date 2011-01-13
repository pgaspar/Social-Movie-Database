from django_rdf.utils import LazySubject
from django_rdf import graph
from smdb import manager
from smdb.browsing.filter_list import Filter
from rdflib import Literal, URIRef

from django.core.urlresolvers import reverse
import urllib

class BaseModel(LazySubject):
	
	def __new__(self, uri):
		obj = object.__new__(self)
		
		return manager.getOrUse(uri, obj)
	
	def __init__(self, uri):
		
		# Avoid running __init__() in an already created instance
		try:
			self.__getattribute__('uri')
			return True
		except AttributeError: pass
		
		# Proceed with the initialization
		super(BaseModel, self).__init__(graph, uri)
		
		self.dynamic = {}
	
	def __getattr__(self, name):
		
		if name in self.dynamic.keys():
			
			if self.dynamic[name] == None:
				self.dynamic[name] = getattr(self, 'get_' + name)()
			
			return self.dynamic[name]
		else:
			return super(BaseModel, self).__getattr__(name)
	
	def __str__(self):
		return u"%s(%s)" %(self.__class__.__name__, self.uri)


class Movie(BaseModel):
	
	def __init__(self, uri):
		if super(Movie, self).__init__(uri): return		# Call super and exit if this is a created instance
		
		self.title, self.releaseDate, self.duration, self.synopsis = graph.query_single(
			"""SELECT ?t ?y ?d ?s WHERE {
						?u rdf:type smdb:Movie .
						?u smdb:title ?t .
						?u smdb:releaseDate ?y .
						?u smdb:duration ?d .
						?u smdb:synopsis ?s .
					}""", initBindings={'u': self.uri})
		
		self.dynamic = {
			'directedBy': None,
			'writtenBy': None,
			'featured': None,
			'isOfGenre': None,
			'hasReview': None,
			'shotIn': None,
			'hasRating': None,
		}
		
			
	def get_directedBy(self):
		print '>> fetching [Movie-directedBy]'
		return [ Person(obj.uri) for obj in self.smdb__directedBy__m ]
	
	def get_writtenBy(self):
		print '>> fetching [Movie-writtenBy]'
		return [ Person(obj.uri) for obj in self.smdb__writtenBy__m ]
		
	def get_featured(self):
		print '>> fetching [Movie-featured]'
		return [ Person(obj.uri) for obj in self.smdb__featured__m ]
	
	def get_isOfGenre(self):
		print '>> fetching [Movie-isOfGenre]'
		return [ Genre(obj.uri) for obj in self.smdb__isOfGenre__m ]
	
	def get_hasReview(self):
		print '>> fetching [Movie-hasReview]'
		return [ MovieReview(obj.uri) for obj in self.smdb__hasReview__m ]
		
	def get_shotIn(self):
		print '>> fetching [Movie-shotIn]'
		return [ Location(obj) for obj in self.smdb__shotIn__m ]
		
	def get_hasRating(self):
		print '>> fetching [Movie-hasRating]'
		# Return a single result.
		for rating in [ MPAA_Rating(obj.uri) for obj in self.smdb__hasRating__m ]:
			return rating
		
	def get_actor_character(self):
		for uriActor, uriCharacter in graph.query("""SELECT ?a ?c WHERE {
										?a smdb:performedIn ?u.
										?c smdb:inMovie ?u .
										?c smdb:portrayedBy ?a .
										}""", initBindings={'u': self.uri}):
			yield Person(uriActor), Character(uriCharacter)
	
	def friends_who_watched(self, user):
		for uri in graph.query("""SELECT ?u WHERE {
										?u smdb:hasSeen ?m .
										?u smdb:isFriendsWith ?me .
										}""", initBindings={'m': self.uri, 'me': URIRef(user)}):
			yield SMDBUser(uri) 
	
	@classmethod
	def getFilterList(model, year=None, director=None, genre=None, location=None, rating=None):
		
		# Define the filtering rules so that we can filter the options themselves
		f_rules = [
					"?m smdb:releaseDate \"%s\" . " % Literal(year) if year else "",
					"<%s> smdb:directed ?m . " % URIRef(director) if director else "",
					"?m smdb:isOfGenre smdb:%s . " % URIRef(genre) if genre else "",
					"?m smdb:shotIn \"%s\" . " % Literal(location) if location else "",
					"?m smdb:hasRating <%s> . " % URIRef(rating) if rating else "",
				]
		
		# Years
		years = graph.query("SELECT DISTINCT ?y WHERE { ?m smdb:releaseDate ?y . %s} ORDER BY ?y" \
				% ( ''.join(f_rules) ), initBindings={'y':Literal(year)} if year else {})
		
		# Directors
		directors = graph.query("SELECT DISTINCT ?n ?d WHERE { ?d smdb:name ?n . ?d smdb:directed ?m . %s}" \
				% ( ''.join(f_rules) ), initBindings={'d':URIRef(director)} if director else {})
		
		# Genre
		genres = graph.query("""SELECT DISTINCT ?g WHERE {
				?u rdfs:subClassOf smdb:Genre . ?m smdb:isOfGenre ?u . ?u rdfs:label ?g .%s }""" \
				% ( ''.join(f_rules) ), initBindings={'g':Literal(genre, datatype=graph.ontologies['xsd'].string)} if genre else {})
				
		
		# Location
		locations = graph.query("SELECT DISTINCT ?l WHERE { ?m smdb:shotIn ?l . %s}" \
				% ( ''.join(f_rules) ), initBindings={'l':Literal(location)} if location else {})
		
		# Rating
		ratings = graph.query("""SELECT DISTINCT ?r ?u WHERE {
				?u rdfs:subClassOf smdb:MPAA_Rating . ?u rdfs:label ?r . ?m smdb:hasRating ?u . %s} ORDER BY ?r
				"""% ( ''.join(f_rules) ), initBindings={'u':URIRef(rating)} if rating else {})
		
		ratings = [ (label.split(' ')[0], uri) for (label, uri) in ratings ]	# Make the label shorter
		
		return [
			Filter(header='Genre', label='genre', obj_list=genres, target_o=genre),
			Filter(header='Director', label='director', obj_list=directors, target_o=director),
			Filter(header='Year', label='year', obj_list=years, target_o=year),
			Filter(header='Shot In', label='location', obj_list=locations, target_o=location),
			Filter(header='Rating', label='rating', obj_list=ratings, target_o=rating),
		]
		
		
	
	def get_absolute_url(self):
		return self.uri
		

class Person(BaseModel):
	
	def __init__(self, uri):
		if super(Person, self).__init__(uri): return		# Call super and exit if this is a created instance
		
		self.name = graph.query_single(
			"""SELECT ?n WHERE {
						?u rdf:type smdb:Person .
						?u smdb:name ?n .
					}""", initBindings={'u': self.uri})
		
		self.dynamic = {
			'directed': None,
			'wrote': None,
			'performedIn': None,
			'playsCharacter': None,
		}
		
		
	def get_directed(self):
		print '>> fetching [Person-directed]'
		return [ Movie(obj.uri) for obj in self.smdb__directed__m ]
	
	def get_wrote(self):
		print '>> fetching [Person-wrote]'
		return [ Movie(obj.uri) for obj in self.smdb__wrote__m ]
		
	def get_performedIn(self):
		print '>> fetching [Person-performedIn]'
		return [ Movie(obj.uri) for obj in self.smdb__performedIn__m ]
	
	def get_playsCharacter(self):
		print '>> fetching [Person-playsCharacter]'
		return [ Character(obj.uri) for obj in self.smdb__playsCharacter__m ]

	@classmethod
	def getFilterList(model, occupations=[]):
		
		occupation_list = [ (o, o.lower()) for o in ['Director', 'Writer', 'Actor'] ]
		
		return [ Filter(header='Occupations', label='occupations', obj_list=occupation_list, target_o=occupations, mult=True) ]
		
	def get_absolute_url(self):
		return self.uri
		
		
class Character(BaseModel):
	
	def __init__(self, uri):
		if super(Character, self).__init__(uri): return		# Call super and exit if this is a created instance
		
		self.name = graph.query_single(
			"""SELECT ?n WHERE {
						?u rdf:type smdb:Character .
						?u smdb:name ?n .
					}""", initBindings={'u': self.uri})
					
		
		self.dynamic = {
			'portrayedBy': None,
			'inMovie': None,
		}
		
	
	def get_portrayedBy(self):
		print '>> fetching [Character-portrayedBy]'
		return [ Person(obj.uri) for obj in self.smdb__portrayedBy__m ]
		
	def get_inMovie(self):
		print '>> fetching [Character-inMovie]'
		return [ Movie(obj.uri) for obj in self.smdb__inMovie__m ]
	
	def get_movie_actors(self):
		for uriMovie, uriActor in graph.query("""SELECT ?m ?a WHERE {
										?a smdb:performedIn ?m.
										?c smdb:inMovie ?m .
										?c smdb:portrayedBy ?a .
										}""", initBindings={'c': self.uri}):
			yield Movie(uriMovie), Person(uriActor)
	
	
	def get_absolute_url(self):
		return self.uri
	
	
class SMDBUser(BaseModel):
	
	def __init__(self, uri):
		if super(SMDBUser, self).__init__(uri): return		# Call super and exit if this is a created instance
		
		self.username, self.fullName = graph.query_single(
			"""SELECT ?un ?fn WHERE {
						?u rdf:type smdb:SMDBUser .
						?u smdb:username ?un .
						OPTIONAL { ?u smdb:fullName ?fn . }
					}""", initBindings={'u': self.uri})
		
		self.dynamic = {
			'isFriendsWith': None,
			'hasWritten': None,
			'hasSeen': None,
		}
		
	
	def get_isFriendsWith(self):
		print '>> fetching [SMDBUser-isFriendsWith]'
		return [ SMDBUser(obj.uri) for obj in self.smdb__isFriendsWith__m ]
		
	def get_hasWritten(self):
		print '>> fetching [SMDBUser-hasWritten]'
		return [ MovieReview(obj.uri) for obj in self.smdb__hasWritten__m ]
		
	def get_hasSeen(self):
		print '>> fetching [SMDBUser-hasSeen]'
		return [ Movie(obj.uri) for obj in self.smdb__hasSeen__m ]
	
	@classmethod
	def getFilterList(model, is_auth, filters=[]):
		
		filter_list = [ ('Similar Tastes', 'similar'), ('Friend of a Friend', 'foaf'), ('Reviewers', 'reviewer') ]
		
		if not is_auth: filter_list = filter_list[2:]
		
		return [ Filter(header='Filter By', label='filters', obj_list=filter_list, target_o=filters, mult=True) ]
	
	def get_absolute_url(self):
		return self.uri
	
	
class MovieReview(BaseModel):
	
	def __init__(self, uri):
		if super(MovieReview, self).__init__(uri): return		# Call super and exit if this is a created instance
		
		self.id, self.reviewText = graph.query_single(
			"""SELECT ?id ?t WHERE {
						?u rdf:type smdb:MovieReview .
						?u smdb:id ?id .
						?u smdb:reviewText ?t .
					}""", initBindings={'u': self.uri})
					
		
		self.dynamic = {
			'refersTo': None,
			'writtenByUser': None,
		}
		
	
	def get_refersTo(self):
		print '>> fetching [MovieReview-refersTo]'
		# Return a single result.
		for movie in [ Movie(obj.uri) for obj in self.smdb__refersTo__m ]:
			return movie
	
	def get_writtenByUser(self):
		print '>> fetching [MovieReview-writtenByUser]'
		# Return a single result.
		for user in [ SMDBUser(obj.uri) for obj in self.smdb__writtenByUser__m ]:
			return user
	
	def get_absolute_url(self):
		return u'%s#review-%s' %(self.refersTo.get_absolute_url(), self.id)
		
		


# Helper Models - These are not semantic models per se. They're used by semantic models, though...

class Location():
	
	def __init__(self, name):
		self.name = name
		
	def __unicode__(self):
		return u'%s' % self.name
	
	def get_absolute_url(self):
		return u'%s?location=%s' % (reverse('browse-movies'), self.name)
	
class MPAA_Rating():
	
	def __init__(self, uri):
		self.uri = URIRef(uri)
		
		self.label = graph.query_single (
			"""SELECT ?l WHERE {
						?u rdfs:subClassOf smdb:MPAA_Rating .
						?u rdfs:label ?l .
					}""", initBindings={'u': self.uri})
	
	def __unicode__(self):
		return u'%s' % self.label
	
	def get_absolute_url(self):
		return u'%s?rating=%s' % (reverse('browse-movies'), urllib.quote(self.uri))		# Quote encodes the URL
	
	
class Genre():
	
	def __init__(self, uri):
		self.uri = URIRef(uri)
		
		self.label = graph.query_single (
			"""SELECT ?l WHERE {
						?u rdfs:subClassOf smdb:Genre .
						?u rdfs:label ?l .
					}""", initBindings={'u': self.uri})
	
	def __unicode__(self):
		return u'%s' % self.label
	
	def get_absolute_url(self):
		return u'%s?genre=%s' % (reverse('browse-movies'), self.label)
	