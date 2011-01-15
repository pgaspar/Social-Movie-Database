from rdflib import *

g = Graph()

r = g.parse('http://localhost:8000/movie/pulp-fiction-1994/', format="rdfa", publicID='.')

print "Triples in graph: ", len(r)

g.serialize(destination='rdfa-export.xml')
g.serialize(destination='rdfa-export.n3', format="n3")

