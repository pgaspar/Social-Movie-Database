import re
from SMDB import SMDB
import sys
import django

PATH = '../../Data/'
DURATION_FILE = 'running-times.list'

titleRegex = '([^"].*?\(\d{4}\))?'
weirdShitRegex = '(\s\(T?VG?\))?(\s\{.*\})?'
nameRegex = '(.*?)'
characterRegex = '([[].*?[]])'
splitRegex = '\s*\t'

durationsFile = open( PATH + DURATION_FILE )

regex = re.compile(titleRegex + 
					weirdShitRegex +
					splitRegex +
					'(.*?:)?(\d*)')

previous = ""

for line in durationsFile:
	matches = regex.match(line)
	
	if(matches and matches.group(1) and not matches.group(2) and not matches.group(3)):
		try:
			if(matches.group(1) in titles):
				if(matches.group(1) == previous): 
					continue			
				previous = matches.group(1)
				s.addDuration(matches.group(1), matches.group(5))
				print matches.group(1) + ":::" + str(matches.group(4)) + ":::" + matches.group(5)
		except:
			continue
	
	#if(matches and matches.group(1) and not matches.group(2) and not matches.group(3)):
	#	try:
	#		if(matches.group(1) in titles):
	#			s.addLocation(matches.group(1), matches.group(6))
	#			#print matches.group(1) + " SHOT IN " + matches.group(6)
	#	except:
	#		continue
#		print matches.group(1) + " ::: " + matches.group(6)