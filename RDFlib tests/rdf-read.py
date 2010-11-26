from SMDB import SMDB
from rdflib.namespace import Namespace

s = SMDB()
s.printTripleCount()


initNs = dict(smdb=Namespace("http://www.smdb.com/smdb.owl#"))

for a, b, c in s.graph.query('SELECT ?a ?b ?c WHERE { ?a smdb:wrote ?c . }', initNs=initNs):
	print a, "\n WROTE \n", c, '\n'

s.exportData('res_read')

