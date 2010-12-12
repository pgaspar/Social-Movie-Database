import imp
import store

from django.conf import settings
from django.utils import importlib

graph = store.open_graph()


for app in settings.INSTALLED_APPS:
        try:
            app_path = importlib.import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('semantic', app_path)
        except ImportError:
            continue
        
        importlib.import_module("%s.semantic" % app)