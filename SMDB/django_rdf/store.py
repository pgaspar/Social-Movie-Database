from django.conf import settings

from rdflib.graph import ConjunctiveGraph as Graph
from rdflib import plugin
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib import Namespace
from rdflib import Literal
from rdflib import URIRef

from django_rdf.utils import *

ref = URIRef(settings.DEFAULT_GRAPH_URI)


def get_mysql_store():
    store = plugin.get('MySQL', Store)(settings.DATABASE_NAME)
    config = "host=%s,user=%s,password=%s,db=%s" % \
        (settings.DATABASE_HOST, settings.DATABASE_USER, \
        settings.DATABASE_PASSWORD, settings.DATABASE_NAME)
    return store, config
    
def get_sqlite_store():
    dbpath = settings.DATABASE_NAME
    store = plugin.get('SQLite', Store)(dbpath)
    config = dbpath
    return store, config

def get_sleepy_store():
    dbpath = settings.RDF_DATABASE_NAME
    store = plugin.get('Sleepycat', Store)(dbpath)
    config = dbpath
    return store, config

def open_graph():
    """ Creates a graph store. """
    store, config = get_sleepy_store()
    """
    if settings.DATABASE_ENGINE == 'mysql':
        store, config = get_mysql_store()
    elif settings.DATABASE_ENGINE == 'sqlite3':
        store, config = get_sqlite_store()
    else:
        return Graph(identifier=ref)
    """

    rt = store.open(config, create = False)
    if rt == NO_STORE:
        # If store doesn't exist
        store.open(config, create=True)
    else:
        assert rt == VALID_STORE, "Graph store is corrupted"
    return PowerGraph(store, identifier=ref)
