from django_rdf.utils import LazySubject
from django_rdf import graph
from smdb import manager
from smdb.browsing.filter_list import Filter
from rdflib import Literal, URIRef

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
		
		self.title, self.releaseDate = graph.query_single(
			"""SELECT ?t ?d WHERE {
						?u rdf:type smdb:Movie .
						?u smdb:title ?t .
						?u smdb:releaseDate ?d .
					}""", initBindings={'u': self.uri})
		
		self.dynamic = {
			'directedBy': None,
			'writtenBy': None,
			'featured': None,
			'isOfGenre': None,
			'hasReview': None,
		}
		
			
	def get_directedBy(self):
		print '>> fetching [Movie-directedBy]'
		# Return a single result.
		for person in [ Person(obj.uri) for obj in self.smdb__directedBy__m ]:
			return person
	
	def get_writtenBy(self):
		print '>> fetching [Movie-writtenBy]'
		return [ Person(obj.uri) for obj in self.smdb__writtenBy__m ]
		
	def get_featured(self):
		print '>> fetching [Movie-featured]'
		return [ Person(obj.uri) for obj in self.smdb__featured__m ]
	
	def get_isOfGenre(self):
		print '>> fetching [Movie-isOfGenre]'
		return [] #[ Genre(obj.uri) for obj in self.smdb__isOfGenre__m ]
	
	def get_hasReview(self):
		print '>> fetching [Movie-hasReview]'
		return [ MovieReview(obj.uri) for obj in self.smdb__hasReview__m ]
		
	def get_actor_character(self):
		for uriActor, uriCharacter in graph.query("""SELECT ?a ?c WHERE {
										?a smdb:performedIn ?u.
										?c smdb:inMovie ?u .
										?c smdb:portrayedBy ?a .
										}""", initBindings={'u': self.uri}):
			yield Person(uriActor), Character(uriCharacter)
	
	@classmethod
	def getFilterList(model, year=None, director=None):
		
		# Years
		years = graph.query("SELECT DISTINCT ?y WHERE { ?u rdf:type smdb:Movie . ?u smdb:releaseDate ?y . %s } ORDER BY ?y" \
				% ( ("<%s> smdb:directed ?u . " % URIRef(director)) if director else "" ), initBindings={'y':Literal(year)} if year else {} )
		
		# Directors
		directors = graph.query("SELECT DISTINCT ?n ?d WHERE { ?d smdb:name ?n . ?d smdb:directed ?m . %s }" \
				% ( ("?m smdb:releaseDate \"%s\" . " % Literal(year)) if year else "" ), initBindings={'d':URIRef(director)} if director else {})
		
		
		years = Filter(header='Year', label='year', obj_list=years, target_o=year)
		directors = Filter(header='Director', label='director', obj_list=directors, target_o=director)
		
		return [directors, years]
	
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
										?a smdb:performedIn ?u.
										?c smdb:inMovie ?m .
										?c smdb:portrayedBy ?a .
										}""", initBindings={'c': self.uri}):
			yield Movie(uriMovie), Person(uriActor)
	
	
	def get_absolute_url(self):
		return self.uri
	
	
class SMDBUser(BaseModel):
	
	def __init__(self, uri):
		if super(SMDBUser, self).__init__(uri): return		# Call super and exit if this is a created instance
		
		self.username = graph.query_single(
			"""SELECT ?un WHERE {
						?u rdf:type smdb:SMDBUser .
						?u smdb:username ?un .
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