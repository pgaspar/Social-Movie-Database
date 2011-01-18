from rdflib import *
from urllib2 import HTTPError

def main():
	g = Graph()

	baseURL = 'http://localhost:8000'
	
	objURI = '/movie/pulp-fiction-1994/'
	#objURI = '/person/quentin-tarantino/'
	#objURI = '/character/vincent-vega/'
	#objURI = '/user/pgaspar/'

	# Parse URL
	r = g.parse(baseURL + objURI, format="rdfa", publicID='.')

	print "Triples in graph: ", len(r)

	# Save to disk
	g.serialize(destination='rdfa-export.xml')
	g.serialize(destination='rdfa-export.n3', format="n3")


	# Display some page info

	initNs = dict(
				rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"), 
				smdb=Namespace("http://www.smdb.com/smdb.owl#"),
			)

	query = """SELECT DISTINCT ?e ?t ?y ?d ?n ?un ?fn WHERE{
			?u rdf:type ?e .
		
			OPTIONAL{ ?u smdb:title ?t } .
			OPTIONAL{ ?u smdb:releaseDate ?y } .
			OPTIONAL { ?u smdb:duration ?d . } .
		
			OPTIONAL{ ?u smdb:name ?n } .
		
			OPTIONAL { ?u smdb:username ?un . } .
			OPTIONAL { ?u smdb:fullName ?fn . } .
			}"""

	res = g.query(query, initNs = initNs, initBindings={'u':URIRef(objURI)})

	for e, t, y, d, n, un, fn in res:
		print '\nURL:', (baseURL + objURI)
		print 'Class:', e
	
		if t: print 'Title:', t
		if y: print 'Year:', y
		if d: print 'Duration:', d
	
		if n: print 'Name:', n
	
		if un: print 'Username:', un
		if fn: print 'Full Name:', fn

if __name__ == '__main__':
	main()