from rdflib.graph import ConjunctiveGraph as Graph
from rdflib import Namespace, Literal, URIRef
from rdflib.term import Identifier, Variable

from smdb.reverses import reverse

class PowerGraph(Graph):
	
	def __init__(self, *args, **kwargs):
		super(PowerGraph, self).__init__(*args, **kwargs)
		self.ontologies = {}
	
	def register_ontology(self, o):
		""" Registers an ontology with the graph """
		self.ontologies.update(o)
		
	def query(self, q, **kwargs):
		d = self.ontologies.copy()
		if 'initNs' in kwargs:
			d.update(kwargs.pop("initNs"))		
		return super(PowerGraph, self).query(q, initNs=d, **kwargs)
	
	def query_single(self, q, **kwargs):
		for result in self.query(q, **kwargs):
			return result
		
	def has_sth(self, url, f):
		if not isinstance(url,URIRef):
			url = URIRef(url)
		return bool(list(self.triples(f(url))))
	
	def has_subject(self, url):
		""" Returns wether a certain URI exists as a subject in a triple """
		return self.has_sth(url, lambda url: (url, None, None))

	def has_value(self, url):
		""" Returns wether a certain URI exists as an object in a triple """
		return self.has_sth(url, lambda url: (None, None, url))

	def has_verb(self, url):
		""" Returns wether a certain URI exists as a verb in a triple """
		return self.has_sth(url, lambda url: (None, url, None))
		
	def get(self, **kwargs):
		""" Returns a LazySubject instance for that URI, or a single response query """
		if 'uri' in kwargs:
			return LazySubject(self, kwargs['uri'])
		else:
			""" Single response query """
			subject = kwargs.get('subject', None)
			verb = kwargs.get('verb', None)
			value = kwargs.get('value', None)
			try:
				return list(self.triples((subject, verb, value)))[0]
			except:
				return None
			
class LazySubject(object):
	def __init__(self, graph, uri):
		self.graph = graph
		if isinstance(uri, URIRef):
			self.uri = uri
		else:
			self.uri = URIRef(uri)

	def get_multiple(self, name):
		if isinstance(name,Identifier):
			for _,_,o in self.graph.triples((self.uri, name, None)):
				if isinstance(o, URIRef): yield LazySubject(self.graph, o)
				else: yield o
		else:
			for o in self.graph.query("SELECT DISTINCT ?o WHERE { { ?s %s ?o } UNION { ?o %s ?s } }" % (name, reverse.get(name, 'smdb:none')), initBindings={'s': self.uri}):
				if isinstance(o, URIRef): yield LazySubject(self.graph, o)
				else: yield o

	def get_single(self, name):
		for i in self.get_multiple(name):
			return i

	def __getattr__(self, name):
		if name.startswith("__"):
			return super(LazySubject, self).__getattribute__(name)
		return self[name]
		
	def __getitem__(self, name):
		name = name.replace('__',':')
		
		# Anything that is not controlled by us...
		if True not in map(name.startswith, self.graph.ontologies.keys()):
			attr = super(LazySubject, self).__getattribute__(name)
			if hasattr(attr, '__call__'): raise AttributeError	# Let Django find the functions later...
			return attr
		
		# Everything else...
		try:
			if name.endswith(":m"):
				return self.get_multiple(name[:-2])
			elif name.endswith(":p"):
				return self.get_single(name[:-2]).toPython()
			else:
				return self.get_single(name)
		except:
			return None
			
	def __str__(self):
		default = str(self.uri)
		try:
			if self.rdf__label:
				return str(self.rdf__label)
		except:
			pass
		return default