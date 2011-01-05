import math

# Usage: split_array(array, size of the blocks)
split_array = lambda v, l: [v[i*l:(i+1)*l] for i in range(int(math.ceil(len(v)/float(l))))]