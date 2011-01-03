from django.template import Library, Node, resolve_variable, TemplateSyntaxError

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
	if value == 'All': del params[varname]
	else: params[varname] = value
	return '%s?%s' % (req.path, params.urlencode())