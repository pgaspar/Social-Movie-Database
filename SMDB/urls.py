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
	
	# Login/Logout
	
	(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
	(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	
	# SMDB
	
	(r'^$', 'smdb.views.index'),

	(r'^movie/(?P<slug>[-\w]+)/$', 'smdb.views.movie_detail'),
	(r'^user/(?P<username>[-_\w]+)/$', 'smdb.views.user_detail'),
	(r'^person/(?P<slug>[-\w]+)/$', 'smdb.views.person_detail'),
	(r'^character/(?P<slug>[-\w]+)/$', 'smdb.views.character_detail'),

	url(r'^browse/movies/$', 'smdb.views.browse_movies', name='browse-movies'),
	url(r'^browse/people/$', 'smdb.views.browse_people', name='browse-people'),
	url(r'^browse/users/$', 'smdb.views.browse_users', name='browse-users'),
	
	(r'^search/.*$', 'smdb.views.search'),
	
	(r'^profile/$', 'smdb.views.redirect_to_profile'),
	
	url(r'^(?P<movieURI>movie/[-/\w]+)mark-seen/$', 'smdb.views.mark_seen', name='mark-seen'),
	
)
