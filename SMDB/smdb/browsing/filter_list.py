class Filter(object):
	
	def __init__(self, header, label, obj_list, target_o, mult=False):
		super(Filter, self).__init__()
		
		self.header = header
		self.label = label
		self.obj_list = obj_list
		self.target_o = target_o
		self.mult = mult
		
		# Create the list
		self.obj_list = [ FilterData(o, self.target_o, self.label, self.mult) for o in self.obj_list]	# Add the "selected" field and some info
		self.obj_list = [ FilterData('All', self.target_o, self.label, False) ] + self.obj_list			# Add the "All" option
		
		
	def __iter__(self, *args, **kwargs):
		return self.obj_list.__iter__(*args, **kwargs)
		
	def __len__(self):
		return self.obj_list.__len__()

class FilterData(object):
	def __init__(self, object_list, target_o, label, mult):
		super(FilterData, self).__init__()
		
		if isinstance(object_list, tuple):
			self.data = object_list[0]
			
			if len(object_list) == 2: self.id = object_list[1]
			else: self.id = self.data
		
		else:
			self.id = self.data = object_list
		
		if self.data == 'All': self.selected = (not target_o)
		else: self.selected = (str(self.id) in str(target_o))
		
		self.label = label
		self.mult = mult
	
	def __str__(self):
		return str(self.data)