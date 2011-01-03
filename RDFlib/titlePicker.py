import re

PATH = '../../Data/'
DIRECTOR_FILE = 'directors.list'
PICKS_FILE = 'pickedTitles.dat'

directors = ['Tarantino, Quentin','Kubrick, Stanley (I)','Jackson, Peter (I)', 'Burton, Tim (I)', 'Bay, Michael', 'Coppola, Francis Ford']
								
if __name__ == "__main__":
	
	titleRegex = '([^"].*?\(\d{4}\))?'
	weirdShitRegex = '(\s\(T?VG?\))?(\s\{.*\})?'
	nameRegex = '(.*?)'
	characterRegex = '([[].*?[]])'
	splitRegex = '\s*\t'
	
	
	directorsFile = open( PATH + DIRECTOR_FILE )
	
	regex = re.compile(nameRegex + 
						splitRegex +
						titleRegex +
						weirdShitRegex)
	
	nMovies = 0
	
	picksFile = open(PATH+PICKS_FILE, 'w')
	
	nameCleaner= re.compile('(.*?),\s(.*)(\s\(.*\))')
	name = re.compile('(.*?),\s(.*)')
	
	for line in directorsFile:
		matches = regex.match(line)
		if(matches and matches.group(2) and not matches.group(3) and not matches.group(4)):
			try:
				if(len(matches.group(1)) != 0):
					directorName = matches.group(1)
					cleanName = ""
					names = nameCleaner.match(directorName)
					if(names):
						cleanName = names.group(2) + " " + names.group(1) + names.group(3)
					else:
						names = name.match(directorName)
						cleanName = names.group(2) + " " + names.group(1)
			except:
				continue
			#for lemma in parsed:
			#	if(lemma in directors):
			#		print directorName + " ::: " + matches.group(2)
			#		nMovies += 1
			#		break
			if(directorName in directors):
				print directorName + ":::" + cleanName + ":::" + matches.group(2)
				picksFile.write(matches.group(2) + '\n')
				nMovies += 1
	
	print "FOUND " + str(nMovies) + " MOVIES"
	
	picksFile.close()
	
	picksFile = open(PATH + PICKS_FILE)
	
	titles = []
	
	for line in picksFile:
		titles.append(line.replace("\n",""))
	
	print titles
	
	picksFile.close