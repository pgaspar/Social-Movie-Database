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
		
		self.smdb = Namespace(identifier + '#')
		self.person = Namespace("/person/")
		self.movie = Namespace("/movie/")
		self.character = Namespace("/character/")
		self.user = Namespace("/user/")

	def printTripleCount(self):
		print "Triples in graph: ", len(self.graph)
	
	def exportData(self, file_name='res'):
		
		# save the graph in RDF/XML and N3
		self.graph.serialize(destination=file_name + ".xml")
		self.graph.serialize(destination=file_name + ".n3", format="n3")
