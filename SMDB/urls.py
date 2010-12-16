from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^SMDB/', include('SMDB.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
	(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	
	# SMDB
	
	(r'^$', direct_to_template, {'template': 'index.html'}),
	(r'^movie/$', direct_to_template, {'template': 'movie.html'}),
	(r'^person/$', direct_to_template, {'template': 'person.html'}),
	(r'^character/$', direct_to_template, {'template': 'character.html'}),
	(r'^profile/$', direct_to_template, {'template': 'user.html'}),
	
	(r'^search/$', direct_to_template, {'template': 'search.html'}),
	(r'^suggestion/$', direct_to_template, {'template': 'suggestion.html'}),
	
	(r'^browse/$', direct_to_template, {'template': 'browse.html'}),
	(r'^browse/movies/$', 'smdb.views.test'),
	(r'^browse/.*/$', direct_to_template, {'template': 'browse.html'}),
	
	(r'^movie/(?P<slug>[-\w]+)/$', 'smdb.views.movie_detail'),
	(r'^user/(?P<username>[\w]+)/$', 'smdb.views.user_detail'),
	(r'^person/(?P<slug>[-\w]+)/$', 'smdb.views.person_detail'),
	(r'^character/(?P<slug>[-\w]+)/$', 'smdb.views.character_detail'),
	
	(r'^test/$', 'smdb.views.test'),
)
