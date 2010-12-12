from django_rdf import graph
from rdflib.namespace import Namespace

ontologies = {

	'rdf': Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
	'smdb': Namespace("http://www.smdb.com/smdb.owl#"),

}

graph.register_ontology(ontologies)
