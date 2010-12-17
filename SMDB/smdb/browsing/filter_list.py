class FilterList(object):
	
	def __init__(self, data):
		super(FilterList, self).__init__()
		
		self._data = []
		self._keys = []
		
		for key, value in data.items():
			self._data.append( value )
			self._keys.append( key )
		
	def getHeaders(self):
		return self._keys
	
	def getData(self):
		return zip(*self._data)
		
