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
	
	