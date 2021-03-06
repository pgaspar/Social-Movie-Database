from django.template import Library

register = Library()

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

