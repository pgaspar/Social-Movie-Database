class SemanticModelManager(object):
	
	def __init__(self):
		self._data = {}
		
	def get(self, uri, modelClass):
		instance = self._data.get(uri, None)
		
		if not instance:
			instance = modelClass(uri)
			self._data[uri] = instance
			
		return instance
	
	def getOrUse(self, uri, new_instance):
		instance = self._data.get(uri, None)
		
		if not instance:
			instance = new_instance
			self._data[uri] = instance
		
		return instance
	
	def __setitem__(self, uri, modelClass):
		return self.get(uri, modelClass)
		
	def clean(self):
		self._data.clear()
	