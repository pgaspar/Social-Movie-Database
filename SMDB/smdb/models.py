from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	
	user = models.ForeignKey(User, unique=True)
	uri = models.CharField("URI", max_length=200)
	
	def __unicode__(self):
		return u"%s's Profile" % self.user.get_full_name()
		
	def get_absolute_url(self):
		return self.uri
		