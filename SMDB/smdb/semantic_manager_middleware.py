from smdb import manager

class SemanticMiddleware(object):
	"""This middlware class cleans the semantic model manager in every new request"""
	
	def process_response(self, request, response):
		manager.clean()
		
		return response