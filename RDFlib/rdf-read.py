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
			person=Namespace("/person/"),
			movie=Namespace("/movie/"),
			character=Namespace("/character/"),
			user=Namespace("/user/"),
		)

for a, b, c in s.graph.query('SELECT ?a ?b ?c WHERE { ?a smdb:wrote ?c . }', initNs=initNs):
	print a, "\n WROTE \n", c, '\n'

print 'Movie List:'
for uri, title in s.graph.query("""SELECT ?a ?b WHERE {
 			?a rdf:type smdb:Movie .
			?a smdb:title ?b .
			}""", initNs=initNs):
	print 'URI:', uri, 'Title:', title


print 'Director: ',
for director in s.graph.query("""SELECT ?o WHERE {
 			?o smdb:directed ?a .
			}""", initNs=initNs, initBindings={'a': URIRef(s.movie['pulp-fiction-1994/'])}):
	print director


print 'Pulp Fiction reviews:',
for review in s.graph.query("""SELECT ?u WHERE {
 			?u rdf:type smdb:MovieReview .
			?u smdb:refersTo ?m .
			}""", initNs=initNs, initBindings={'m': URIRef('/movie/pulp-fiction-1994/')}):
	print review

for directed, wrote, performedIn in s.graph.query("""SELECT ?d ?w ?p WHERE {
 			?a rdf:type smdb:Person .
			?a smdb:directed ?d .
			?a smdb:wrote ?w .
			?a smdb:performedIn ?p .
			}""", initNs=initNs, initBindings={'a': URIRef(s.person['quentin-tarantino/'])}):
	print 'Directed:', directed
	print 'Wrote:', wrote
	print 'Performed In', performedIn

print 'Users:',
for user in s.graph.query("""SELECT ?un WHERE {
 			?u rdf:type smdb:SMDBUser .
			?u smdb:username ?un .
			}""", initNs=initNs, initBindings={'u': s.user['pgaspar/']}):
	print user

s.exportData('res_read')

