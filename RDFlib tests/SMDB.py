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

	
	def addPerson(self, uri='', name='', biography=''):

		if not uri: uri = BNode()

		self.graph.add((uri, RDF.type, self.smdb['Person']))
		if name: self.graph.add((uri, self.smdb['Name'], Literal(name)))
		if biography: self.graph.add((uri, self.smdb['Biography'], Literal(biography)))
		
		self.graph.commit()
	
	def addPerformance(self, actor, movie):
		
		self.graph.add((actor, self.smdb['performedIn'], movie))
		
		self.graph.commit()
	
	def addDirection(self, director, movie):
		
		self.graph.add((director, self.smdb['directed'], movie))
		
		self.graph.commit()
		
	def addWriting(self, writer, movie):

		self.graph.add((writer, self.smdb['wrote'], movie))

		self.graph.commit()

		
	def addCharacter(self, uri='', name='', portrayed_by_uri='', in_movie_uris=[]):

		if not uri: uri = BNode()

		self.graph.add((uri, RDF.type, self.smdb['Character']))
		if name: self.graph.add((uri, self.smdb['Name'], Literal(name)))
		if portrayed_by_uri: self.graph.add((uri, self.smdb['portrayedBy'], Literal(portrayed_by_uri)))
		
		for m_uri in in_movie_uris:
			self.graph.add((uri, self.smdb['inMovie'], m_uri))
			
		self.graph.commit()
	
	def addMovie(self, uri='', title='', duration=0, synopsis='', genres_uris=[]):

		if not uri: uri = BNode()

		self.graph.add((uri, RDF.type, self.smdb['Movie']))
		if title: self.graph.add((uri, self.smdb['Title'], Literal(title)))
		if duration: self.graph.add((uri, self.smdb['Duration'], Literal(duration)))
		if synopsis: self.graph.add((uri, self.smdb['Synopsis'], Literal(synopsis)))
		
		
		for g_uri in genres_uris:
			self.graph.add((uri, self.smdb['isOfGenre'], g_uri))
		
			
		self.graph.commit()
	
	
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
