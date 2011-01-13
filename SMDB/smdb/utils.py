import math
from smdb.semantic_models import SMDBUser

# Usage: split_array(array, size of the blocks)
split_array = lambda v, l: [v[i*l:(i+1)*l] for i in range(int(math.ceil(len(v)/float(l))))]

def merge_results(res, filters):
	res_dict = {}
	
	# Aggregate by key (the URI, in this case)
	for user in res:
		if user[0] not in res_dict: res_dict[user[0]] = [user[1:]]
		else: res_dict[user[0]].append(user[1:])
	
	# Zip and merge usernames, common movies, etc.
	for key, value in res_dict.items():
		res_dict[key] = [ list(set(t)) for t in zip(*value) ]
		res_dict[key] = [ el[0] if len(el) == 1 else el for el in res_dict[key] ]
		
		# Make sure the last elements are lists.
		for i in [0,1]:
			el = res_dict[key][i]
			if not isinstance(el, list): res_dict[key][i] = [el] if el else list()
	
	# Make this a list again and replace the URI with an instance of SMDBUser
	res_final = [ [SMDBUser(key)] + value for key, value in res_dict.items() ]
	
	# Since we're here, we might as well sort the list (by number of common elements or username)
	res_final.sort(key=lambda o: (len(o[1]) + len(o[2])) if len(o[1]) or len(o[2]) else o[0].username, reverse=('similar' in filters or 'foaf' in filters))
	
	return res_final
	
def sort_by_count(matrix, indexes, cnt_index=None):
	"""
	The second argument are the indexes of the unique fields in each line.
	The third argument is the index where we'll compare to None to distinguish between optional fields.
	"""
	
	res_dict = {}
	
	# Count the number of times each line appears in the matrix
	for line in matrix:
		key = tuple([ line[i] for i in indexes ])
		if cnt_index != None: optional_cell = line[cnt_index]
		else: optional_cell = None
		
		if key not in res_dict: res_dict[key] = 0 if optional_cell == None else 1
		else: res_dict[key] += 1
	
	# Sorted the response so that the high count elements appear first
	sorted_res = sorted(res_dict.items(), key=lambda o: o[1], reverse=True)
	
	return sorted_res