from django.db import models
from django.contrib.auth.models import User
from smdb.semantic_models import SMDBUser
from rdflib import Literal, URIRef

class UserProfile(models.Model):
	
	user = models.ForeignKey(User, unique=True)
	_uri = models.CharField("URI", max_length=200)
	
	def __unicode__(self):
		return u"%s's Profile" % self.user.get_full_name()
	
	@property
	def uri(self):
		return URIRef(self._uri)
	
	@property
	def semantic_user(self):
		return SMDBUser(self._uri)
	
	def get_absolute_url(self):
		return self._uri
		