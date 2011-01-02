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
		return map( None, *self._data )
	
	@classmethod
	def normalize(model, obj_list, target_o, label):
		obj_list = [ FilterData(o, target_o, label) for o in obj_list]	# Add the "selected" field and some info
		obj_list = [ FilterData('All', target_o) ] + obj_list			# Add the "All" option
		
		return obj_list
	
	
class FilterData(object):
	def __init__(self, object_list, target_o, label=''):
		super(FilterData, self).__init__()
		
		if isinstance(object_list, tuple):
			self.data = object_list[0]
			
			if len(object_list) == 2: self.id = object_list[1]
			else: self.id = self.data
		
		else:
			self.id = self.data = object_list
		
		if self.data == 'All': self.selected = (target_o == None)
		else: self.selected = (str(self.id) == str(target_o))
		
		self.label = label
	
	def __str__(self):
		return str(self.data)