import rdflib
from rdflib.store.SQLite import *
from rdflib import Graph
from rdflib.namespace import Namespace, RDF
from rdflib import URIRef, Literal, BNode


class SMDB():
	
	def __init__(self, identifier="http://www.smdb.com/smdb.owl"):
		
		self.sql = SQLite()
		self.sql.open('SMDB.sqlite3')
		
		self.graph = Graph(self.sql, identifier = URIRef(identifier))
		
		self.smdb = Namespace(identifier + '#')

	def printTripleCount(self):
		print "Triples in graph: ", len(self.graph)

	
	def addPerson(self, name):

		uri = self.smdb[name]

		self.graph.add((uri, RDF.type, self.smdb['Person']))
		self.graph.add((uri, self.smdb['Name'], Literal(name)))
		
		self.graph.commit()
	
	def addPerformance(self, actor, movie):
		
		uriActor = self.smdb[actor]
		uriMovie = self.smdb[movie]
		
		self.graph.add((uriActor, self.smdb['performedIn'], urlMovie))
		
		self.graph.commit()
	
	def addDirector(self, director, movie):
		
		uriDirector = self.smdb[director]
		uriMovie = self.smdb[movie]
		
		self.graph.add((uriDirector, self.smdb['directed'], uriMovie))
		
		self.graph.commit()
		
	def addWriter(self, writer, movie):

		uriWriter = self.smdb[writer]
		uriMovie = self.smdb[movie]

		self.graph.add((uriWriter, self.smdb['wrote'], uriMovie))

		self.graph.commit()

		
	def addCharacter(self, movie, actor, character):

		uriMovie = self.smdb[movie]
		uriActor = self.smdb[actor]
		uriCharacter = self.smdb[character]

		self.graph.add((uriCharacter, RDF.type, self.smdb['Character']))
		self.graph.add((uriCharacter, self.smdb['Name'], Literal(character)))
		self.graph.add((uriCharacter, self.smdb['portrayedBy'], uriActor))
		
		
		self.graph.add((uriCharacter, self.smdb['inMovie'], uriMovie))
			
		self.graph.commit()
	
	
	def addMovie(self, title, releaseDate):

		uri = self.smdb[title]

		self.graph.add((uri, RDF.type, self.smdb['Movie']))
		self.graph.add((uri, self.smdb['Title'], Literal(title)))
		self.graph.add((uri, self.smdb['ReleaseDate'], Literal(releaseDate)))
			
		self.graph.commit()
		
	def addGenre(self, movie, genre):
		
		uri = self.smdb[movie]
		uriGenre = self.smdb[genre]
		
		self.graph.add((uri, self.smdb['isOfGenre'], uriGenre))
		
		self.graph.commit()
	
	def addRating(self, movie, rating):
		
		uriMovie = self.smdb[movie]
		uriRating = self.smdb[rating]
		
		self.graph.add((uriMovie, self.smdb['hasRating'], uriRating))
		
		self.graph.commit()
		
	
	def addLocation(self, movie, location):
		
		uriMovie = self.smdb[movie]
		uriLocation = self.smdb[location]
		
		self.graph.add((uriMovie, self.smdb['shotIn'], uriLocation))
	
	def addSMDBUser(self, uri='', username=''):
		
		if not uri: uri = BNode()
		
		self.graph.add((uri, RDF.type, self.smdb['SMDBUser']))
		if username: self.graph.add((uri, self.smdb['Username'], Literal(username)))
		
		self.graph.commit()
		
	
	def addFriendship(self, user1, user2):
		
		self.graph.add((user1, self.smdb['isFriendsWith'], user2))
		self.graph.add((user2, self.smdb['isFriendsWith'], user1))
		
		self.graph.commit()
	
	def addMovieSeen(self, user, movie):
		
		self.graph.add((user, self.smdb['hasSeen'], movie))
		
		self.graph.commit()
	
	
	def addMovieReview(self, uri='', text='', movie='', author=''):
		
		if not uri: uri = BNode()
		
		self.graph.add((uri,RDF.type, self.smdb['MovieReview']))
		self.graph.add((uri, self.smdb['refersTo'], movie))
		self.graph.add((uri, self.smdb['writtenByUser'], author))
		if text: self.graph.add((uri, self.smdb['ReviewText'], Literal(text)))
		
		self.graph.commit()
	
	def exportData(self, file_name='res'):
		
		# save the graph in RDF/XML and N3
		self.graph.serialize(destination=file_name + ".xml")
		self.graph.serialize(destination=file_name + ".n3", format="n3")
