from SMDB import SMDB
from rdflib.namespace import Namespace
from rdflib import URIRef
from rdflib.term import Variable

s = SMDB()
s.printTripleCount()

initNs = dict(
			rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"), 
			smdb=Namespace("http://www.smdb.com/smdb.owl#"),
			xsd=Namespace("http://www.w3.org/2001/XMLSchema#"),
		)

for a, b, c in s.graph.query('SELECT ?a ?b ?c WHERE { ?a smdb:wrote ?c . }', initNs=initNs):
	print a, "\n WROTE \n", c, '\n'

print 'Movie List:'
for uri, title, slug in s.graph.query("""SELECT ?a ?b ?c WHERE {
 			?a rdf:type smdb:Movie .
			?a smdb:title ?b .
			?a smdb:slug ?c .
			}""", initNs=initNs):
	print 'URI:', uri, 'Title:', title, 'Slug:', slug 


print 'Director: ',
for director in s.graph.query("""SELECT ?o WHERE {
 			?o smdb:directed smdb:Pulp_Fiction_1994 .
			}""", initNs=initNs):
	print director


print 'Pulp Fiction reviews:',
for review in s.graph.query("""SELECT ?u WHERE {
 			?u rdf:type smdb:MovieReview .
			?u smdb:refersTo ?m .
			}""", initNs=initNs, initBindings={'m': uri}):
	print review

for directed, wrote, performedIn in s.graph.query("""SELECT ?d ?w ?p WHERE {
 			?a rdf:type smdb:Person .
			?a smdb:directed ?d .
			?a smdb:wrote ?w .
			?a smdb:performedIn ?p .
			}""", initNs=initNs, initBindings={'a': URIRef(s.smdb['Quentin_Tarantino'])}):
	print 'Directed:', directed
	print 'Wrote:', wrote
	print 'Performed In', performedIn

s.exportData('res_read')

