from django.template import Library

register = Library()


@register.filter
def getOccupations(person):
	director, writer, actor = ['<a href="#director-section">Director</a>',
							   '<a href="#writer-section">Writer</a>',
							   '<a href="#actor-section">Actor</a>']

	html = []

	if person.directed: html.append(director)
	if person.wrote: html.append(writer)
	if person.performedIn: html.append(actor)
	
	return " - ".join(html)


@register.filter
def friends_who_watched(movie, request):
	return movie.friends_who_watched(request.user.get_profile().uri)

@register.filter
def hasSeen(user, movie):
	return movie in user.get_profile().semantic_user.hasSeen
	
@register.filter
def isFriendsWith(session_user, other_user):
	return other_user in session_user.get_profile().semantic_user.isFriendsWith