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
def lowerThan(value, target):
	return value < target
	
@register.filter
def higherThan(value, target):
	return value > target
	

@register.filter
def useinURL(req, el):
	varname, value = el.label, el.id
	params = req.GET.copy()
	
	if value == 'All':
		if varname in params: del params[varname]
	else:
		params[varname] = value
	
	return '%s?%s' % (req.path, params.urlencode())
	
@register.filter
def useinURL_m(req, el):
	varname, value = el.label, el.id
	params = req.GET.copy()
	
	if value == 'All':
		if varname in params: del params[varname]
	else:
		if el.selected and value in params.getlist(varname):
			params.getlist(varname).remove(value)	# Has been selected before, deselects now.
		else:
			params.update({varname: value})
	
	return '%s?%s' % (req.path, params.urlencode())
	
	
@register.filter
def zip(label, name):
	
	return zip(label,name)

