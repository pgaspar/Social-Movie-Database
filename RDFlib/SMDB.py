import rdflib
from rdflib.store.Sleepycat import Sleepycat
from rdflib import Graph
from rdflib.namespace import Namespace, RDF
from rdflib import URIRef, Literal, BNode

from django.template.defaultfilters import slugify


class SMDB():
	
	def __init__(self, identifier="http://www.smdb.com/smdb.owl"):
		
		self.store = Sleepycat()
		#self.store.open('rdf-db')
		self.store.open('../SMDB/database/rdf', create = False)
		
		self.graph = Graph(self.store, identifier = URIRef(identifier))
		
		self.printTripleCount()
		
		if(len(self.graph) == 0):
			self.graph.parse('../Ontology/SocialMovieDatabase.owl')
		
		self.smdb = Namespace(identifier + '#')
		self.person = Namespace("/person/")
		self.movie = Namespace("/movie/")
		self.character = Namespace("/character/")
		self.user = Namespace("/user/")

	def printTripleCount(self):
		print "Triples in graph: ", len(self.graph)

	
	def addPerson(self, name):

		uri = self.person[name.replace(' ', '_').replace('(', '').replace(')', '')]

		self.graph.add((uri, RDF.type, self.smdb['Person']))
		self.graph.add((uri, self.smdb['name'], Literal(name)))
		
		self.graph.commit()
	
	def addPerformance(self, actor, movie):
		
		uriActor = self.person[actor.replace(' ', '_').replace('(', '').replace(')', '')]
		uriMovie = self.movie[movie.replace(' ', '_').replace('(', '').replace(')', '')]
		
		self.graph.add((uriActor, self.smdb['performedIn'], uriMovie))
		
		self.graph.commit()
	
	def addDirector(self, director, movie):
		
		uriDirector = self.person[director.replace(' ', '_').replace('(', '').replace(')', '')]
		uriMovie = self.movie[movie.replace(' ', '_').replace('(', '').replace(')', '')]
		
		self.graph.add((uriDirector, self.smdb['directed'], uriMovie))
		
		self.graph.commit()
		
	def addWriter(self, writer, movie):

		uriWriter = self.person[writer.replace(' ', '_').replace('(', '').replace(')', '')]
		uriMovie = self.movie[movie.replace(' ', '_').replace('(', '').replace(')', '')]

		self.graph.add((uriWriter, self.smdb['wrote'], uriMovie))

		self.graph.commit()

		
	def addCharacter(self, movie, actor, character):

		uriMovie = self.movie[movie.replace(' ', '_').replace('(', '').replace(')', '')]
		uriActor = self.person[actor.replace(' ', '_').replace('(', '').replace(')', '')]
		uriCharacter = self.person[character.replace(' ', '_').replace('(', '').replace(')', '')]

		self.graph.add((uriCharacter, RDF.type, self.smdb['Character']))
		self.graph.add((uriCharacter, self.smdb['name'], Literal(character)))
		self.graph.add((uriCharacter, self.smdb['portrayedBy'], uriActor))
		
		self.graph.add((uriCharacter, self.smdb['inMovie'], uriMovie))
			
		self.graph.commit()
	
	
	def addMovie(self, title, releaseDate):

		uri = self.movie[title.replace(' ', '_').replace('(', '').replace(')', '')]
		
		if '(' in title: clean_title = title[:title.find('(')-1]
		
		self.graph.add((uri, RDF.type, self.smdb['Movie']))
		self.graph.add((uri, self.smdb['title'], Literal(clean_title)))
		self.graph.add((uri, self.smdb['releaseDate'], Literal(releaseDate)))
		
		self.graph.commit()
		
	def addGenre(self, movie, genre):
		
		uri = self.movie[movie.replace(' ', '_').replace('(', '').replace(')', '')]
		uriGenre = self.smdb[genre.replace(' ', '_').replace('(', '').replace(')', '')]
		
		self.graph.add((uri, self.smdb['isOfGenre'], uriGenre))
		
		self.graph.commit()
	
	def addRating(self, movie, rating):
		
		uriMovie = self.movie[movie.replace(' ', '_').replace('(', '').replace(')', '')]
		uriRating = self.smdb[rating.replace(' ', '_').replace('(', '').replace(')', '')]
		
		self.graph.add((uriMovie, self.smdb['hasRating'], uriRating))
		
		self.graph.commit()
		
	
	def addLocation(self, movie, location):
		
		uriMovie = self.movie[movie.replace(' ', '_').replace('(', '').replace(')', '')]
		
		self.graph.add((uriMovie, self.smdb['shotIn'], uriLocation))
		
		self.graph.commit()
	
	def addSMDBUser(self, username):
		
		uri = self.user[username.replace(' ', '_').replace('(', '').replace(')', '')]
		
		self.graph.add((uri, RDF.type, self.smdb['SMDBUser']))
		self.graph.add((uri, self.smdb['username'], Literal(slugify(username).replace('-', '_'))))
		
		self.graph.commit()
		
	
	def addFriendship(self, user1, user2):
		
		uriUser1 = self.user[user1.replace(' ', '_').replace('(', '').replace(')', '')]
		uriUser2 = self.user[user2.replace(' ', '_').replace('(', '').replace(')', '')]
		
		self.graph.add((uriUser1, self.smdb['isFriendsWith'], uriUser2))
		self.graph.add((uriUser2, self.smdb['isFriendsWith'], uriUser1))
		
		self.graph.commit()
	
	def addMovieSeen(self, user, movie):
		
		uriUser = self.user[user.replace(' ', '_').replace('(', '').replace(')', '')]
		uriMovie = self.movie[movie.replace(' ', '_').replace('(', '').replace(')', '')]
		
		self.graph.add((uriUser, self.smdb['hasSeen'], uriMovie))
		
		self.graph.commit()
	
	
	def addMovieReview(self, review_id, text, movie, author):
		
		cleanMovie = movie.replace(' ', '_').replace('(', '').replace(')', '')
		
		uri = self.movie[cleanMovie + '#review-' + str(review_id)]
		uriMovie = self.movie[cleanMovie]
		uriUser = self.user[author.replace(' ', '_').replace('(', '').replace(')', '')]
		
		self.graph.add((uri,RDF.type, self.smdb['MovieReview']))
		self.graph.add((uri, self.smdb['id'], Literal(review_id)))
		self.graph.add((uri, self.smdb['refersTo'], uriMovie))
		self.graph.add((uri, self.smdb['writtenByUser'], uriUser))
		self.graph.add((uri, self.smdb['reviewText'], Literal(text)))
		
		self.graph.commit()
	
	def exportData(self, file_name='res'):
		
		# save the graph in RDF/XML and N3
		self.graph.serialize(destination=file_name + ".xml")
		self.graph.serialize(destination=file_name + ".n3", format="n3")
