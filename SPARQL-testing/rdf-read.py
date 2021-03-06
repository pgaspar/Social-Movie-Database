from SMDB import SMDB
from rdflib.namespace import Namespace
from rdflib import URIRef
from rdflib.term import Variable, Literal
import time

s = SMDB()

initNs = dict(
			rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"), 
			smdb=Namespace("http://www.smdb.com/smdb.owl#"),
			xsd=Namespace("http://www.w3.org/2001/XMLSchema#"),
			rdfs=Namespace("http://www.w3.org/2000/01/rdf-schema#"),
			owls=Namespace("http://www.w3.org/2002/07/owl#"),
			person=Namespace("/person/"),
			movie=Namespace("/movie/"),
			character=Namespace("/character/"),
			user=Namespace("/user/"),
		)

rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
xsd=Namespace("http://www.w3.org/2001/XMLSchema#")
rdfs=Namespace("http://www.w3.org/2000/01/rdf-schema#")
owls=Namespace("http://www.w3.org/2002/07/owl#")

term_1 = "person"

query = """SELECT DISTINCT ?u WHERE{
		?u rdf:type ?p .
		?u rdfs:label ?l .
		FILTER ( regex(str(?p), "class", "i") ).
		FILTER ( regex(str(?l), "%s", "i") ).
		}"""%term_1

results = s.graph.query(query, initNs = initNs)

for res in results:
	print res

# for a, b, c in s.graph.query('SELECT ?a ?b ?c WHERE { ?a smdb:wrote ?c . }', initNs=initNs):
# 	print a, "\n WROTE \n", c, '\n'
# 
# print 'Movie List:'
# for uri, title in s.graph.query("""SELECT ?a ?b WHERE {
#  			?a rdf:type smdb:Movie .
# 			?a smdb:title ?b .
# 			}""", initNs=initNs):
# 	print 'URI:', uri, 'Title:', title
# 
# 
# print 'Director: ',
# for director in s.graph.query("""SELECT ?o WHERE {
#  			?o smdb:directed ?a .
# 			}""", initNs=initNs, initBindings={'a': URIRef(s.movie['pulp-fiction-1994/'])}):
# 	print director
# 
# 
# print 'Pulp Fiction reviews:',
# for review in s.graph.query("""SELECT ?u WHERE {
#  			?u rdf:type smdb:MovieReview .
# 			?u smdb:refersTo ?m .
# 			}""", initNs=initNs, initBindings={'m': URIRef('/movie/pulp-fiction-1994/')}):
# 	print review
# 
# for directed, wrote, performedIn in s.graph.query("""SELECT ?d ?w ?p WHERE {
#  			?a rdf:type smdb:Person .
# 			?a smdb:directed ?d .
# 			?a smdb:wrote ?w .
# 			?a smdb:performedIn ?p .
# 			}""", initNs=initNs, initBindings={'a': URIRef(s.person['quentin-tarantino/'])}):
# 	print 'Directed:', directed
# 	print 'Wrote:', wrote
# 	print 'Performed In', performedIn

# print 'Users:',
# for user in s.graph.query("""SELECT ?un WHERE {
#  			?u rdf:type smdb:SMDBUser .
# 			?u smdb:username ?un .
# 			}""", initNs=initNs, initBindings={'u': s.user['pgaspar/']}):
# 	print user
# 
# print ''
# 
# print 'Filtering:'
# 
# q = """SELECT ?a ?b WHERE {
# 			?a rdf:type smdb:Movie .
# 			?a smdb:title ?b .
# 			?d smdb:directed ?a . 
# 			FILTER( ?d = <%s> || ?d = <%s> ) .
# 		}""" % (URIRef('/person/frank-miller-ii/'), URIRef('/person/aleksandr-kozyr/'))
# 
# print q
# 
# for a, b in s.graph.query(q, initNs=initNs):
# 	print a, b
# 
# for a in s.graph.query("""SELECT ?g WHERE { ?g rdfs:subClassOf smdb:Genre . }""", initNs=initNs):
# 	print a

# movies = "SELECT ?r ?l ?c WHERE { ?r rdfs:subPropertyOf smdb:participatedInMovie . ?r rdfs:label ?l}"
# 
# res = s.graph.query(movies, initNs = initNs)
# 
# for i in res:
# 	print i

# year, director, genre = None, None, 'Action'
# 
# genres = "SELECT DISTINCT ?g ?u WHERE { ?u rdfs:subClassOf smdb:Genre . ?m smdb:isOfGenre ?u . ?u rdfs:label ?g . %s %s }" \
# 				% ( 
# 					"<%s> smdb:directed ?m . " % URIRef(director) if director else "",
# 					"?m smdb:releaseDate \"%s\" . " % Literal(year) if year else ""
# 				)
# 
# print genres
# 
# for a, u in s.graph.query(genres, initNs=initNs, initBindings={'g':Literal(genre, datatype=xsd.string)} if genre else {}).result:
# 	print a, u


# movies = "SELECT ?b WHERE {?b owls:inverseOf smdb:directedBy .}"
# 
# res = s.graph.query(movies, initNs = initNs)
# 
# 
# for i in res:
# 	print i
	
# notSeen = """SELECT DISTINCT ?m ?f ?u WHERE {
# 					?m rdf:type smdb:Movie .
# 					OPTIONAL{ ?f smdb:hasSeen ?m .
# 							  ?f smdb:isFriendsWith <%s> .
# 							  } .
# 					OPTIONAL{ ?u smdb:hasSeen ?m .
# 							  FILTER( ?u = <%s>) . 
# 							  } .
# 					}""" % (URIRef("/user/mtavares/"), URIRef("/user/mtavares/"))
# 					
# res = s.graph.query(notSeen, initNs = initNs)
# 
# 
# for i in res:
# 	print i[0] + ":::" + str(i[1]) + ":::" + str(i[2])

# n_iter = 1000
# time_sum = 0
# for i in range(n_iter):
# 	a = time.time()
# 
# 	res = s.graph.query("""SELECT ?un ?f WHERE {
# 					?u rdf:type smdb:SMDBUser .
# 					?u smdb:username ?un .
# 					?u smdb:hasSeen ?m .
# 					?me smdb:hasSeen ?m .
# 					OPTIONAL{ ?me smdb:isFriendsWith ?f . ?u smdb:isFriendsWith ?f } .
# 					OPTIONAL{ ?u smdb:isFriendsWith ?me . ?u2 rdf:type smdb:SMDBUser . }
# 					FILTER( !bound(?u2) && ?u != ?me) .
# 					}""", initBindings={'me': URIRef("/user/pgaspar/")}, initNs=initNs).result
# 
# 	res = [ (u, f) for (u, f) in res if u]
# 
# 	#for u, f in res: print u, f
# 
# 	b = time.time()
# 	time_sum += (b - a)
# 
# print "--- Big Query Method: %f ---" % (time_sum/n_iter)


# n_iter = 1000
# time_sum = 0
# for i in range(n_iter):
# 	a = time.time()
# 
# 	friends = s.graph.query("""SELECT ?un WHERE {
# 					?u rdf:type smdb:SMDBUser .
# 					?u smdb:username ?un .
# 					?u smdb:isFriendsWith ?me .
# 					}""", initBindings={'me': URIRef("/user/pgaspar/")}, initNs=initNs).result
# 
# 	res = s.graph.query("""SELECT ?un ?f WHERE {
# 					?u rdf:type smdb:SMDBUser .
# 					?u smdb:username ?un .
# 					?u smdb:hasSeen ?m .
# 					?me smdb:hasSeen ?m .
# 					OPTIONAL{ ?me smdb:isFriendsWith ?f . ?u smdb:isFriendsWith ?f } .
# 					FILTER( ?u != ?me) .
# 					}""", initBindings={'me': URIRef("/user/pgaspar/")}, initNs=initNs).result
# 
# 
# 	res = [ (u, f) for (u, f) in res if u and u not in friends]
# 
# 	#for u, f in res: print u, f
# 
# 	b = time.time()
# 	time_sum += (b - a)
# 
# print "--- 2-query Method: %f ---" % (time_sum/n_iter)


# movies = """SELECT DISTINCT ?u ?un ?fn WHERE {
# 				?u rdf:type smdb:SMDBUser .
# 				?u smdb:username ?un .
# 				OPTIONAL { ?u smdb:fullName ?fn . }
# 			}"""

#res = s.graph.query(movies, initNs = initNs)

#for i in res:
#	print i

# c = 0
# print 'Directors:'
# for n, d in s.graph.query("""SELECT DISTINCT ?n ?d WHERE { ?d rdf:type smdb:Person . ?d smdb:name ?n . ?d smdb:directed ?m . }""", initNs=initNs, DEBUG=False).result[0:10]:
# 	print 'n:', n, '\nd:', d
# 	c += 1
# 	
# print '--- Processed', c, 'Directors ---'

#s.exportData()

