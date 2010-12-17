import re
from SMDB import SMDB

PATH = '../../Data/'
MOVIE_FILE = 'movies.list'
ACTOR_FILE = 'actors.list'
ACTRESS_FILE = 'actresses.list'
WRITER_FILE = 'writers.list'
DIRECTOR_FILE = 'directors.list'
PLOT_FILE = 'plot.list'
GENRE_FILE = 'genres.list'
LOCATION_FILE = 'locations.list'
RATING_FILE = 'mpaa-ratings-reasons.list'
PICKS_FILE = 'pickedTitles.dat'


def cleanName(name):
	
	nameCleaner= re.compile('(.*?),\s(.*)(\s\(.*\))')
	nameNormal = re.compile('(.*?),\s(.*)')
	cleanName = ""
	
	names = nameCleaner.match(name)
	if(names):
		cleanName = names.group(2) + " " + names.group(1) + names.group(3)
	else:
		names = nameNormal.match(name)
		cleanName = names.group(2) + " " + names.group(1)
	
	return cleanName
	

if __name__ == "__main__":
	

	
	titleRegex = '([^"].*?\(\d{4}\))?'
	weirdShitRegex = '(\s\(T?VG?\))?(\s\{.*\})?'
	nameRegex = '(.*?)'
	characterRegex = '([[].*?[]])'
	splitRegex = '\s*\t'
	
	s = SMDB()
	
	pickedFile = open(PATH + PICKS_FILE)
	
	titles = []
	i = 0
	
	for line in pickedFile:
		titles.append(line.replace("\n",""))
	
	
	#--------------------------------------------------------------------------------------
	#MOVIES
	
	movieFile = open( PATH + MOVIE_FILE ) 

	regex = re.compile( titleRegex +
						weirdShitRegex +
						splitRegex +
						'(\d{4})$', re.VERBOSE)
	nMovies = 0
	
	for line in movieFile:
		matches = regex.match(line)
		if(matches and matches.group(1) and not matches.group(2) and not matches.group(3)):
			#print matches.group(1) + " ::: " + matches.group(4)
			if(matches.group(1) in titles):
				try:
					s.addMovie(matches.group(1),matches.group(4))
					print matches.group(1)
				except:
					print matches.group(1) + " FAILED"
					continue
				nMovies += 1
	
	print "FINISHED PARSING MOVIES : " + str(nMovies)

	#-------------------------------------------------------------------------------------
	#ACTORS
	
	actorFile = open( PATH + ACTOR_FILE )
	
	regex = re.compile(nameRegex +
						splitRegex +
						titleRegex +
						weirdShitRegex +
						'.*?' +
						characterRegex)

	nParticipations = 0

	for line in actorFile:
		matches = regex.match(line)
		if(matches and len(matches.group(1)) != 0):
			actorName = matches.group(1)
			addedPerson = False
		
		if(matches and matches.group(2) and not matches.group(3) and not matches.group(4)):
			try:
				if(matches.group(2) in titles):
					if(not addedPerson):
						clean = cleanName(actorName)
						s.addPerson(clean)
						addedPerson = True
					s.addPerformance(clean, matches.group(2))
					s.addCharacter(matches.group(2), clean, matches.group(5).replace("[","").replace("]",""))
					print clean + " AS " + matches.group(5)
			except:
				continue
	#		print actorName + " ::: " + matches.group(2) + " ::: " + matches.group(5)
			nParticipations += 1
			
	print "FINISHED PARSING ACTORS : " + str(nParticipations)
	
	
	#--------------------------------------------------------------------------------------
	#ACTRESSES
	
	actressFile = open( PATH + ACTRESS_FILE )
	
	nParticipations = 0

	for line in actressFile:
		matches = regex.match(line)
		if(matches and len(matches.group(1)) != 0):
			actorName = matches.group(1)
			addedPerson = False
		
		if(matches and matches.group(2) and not matches.group(3) and not matches.group(4)):
			try:
				if(matches.group(2) in titles):
					if(not addedPerson):
						clean = cleanName(actorName)	
						s.addPerson(clean)
						addedPerson = True
					s.addPerformance(clean, matches.group(2))
					s.addCharacter(matches.group(2), clean, matches.group(5))
					print clean + " AS " + matches.group(5)
			except:
				continue
	#		print actorName + " ::: " + matches.group(2) + " ::: " + matches.group(5)
			nParticipations += 1
			
	print "FINISHED PARSING ACTRESSES : " + str(nParticipations)
	
	#--------------------------------------------------------------------------------------
	#WRITERS
	
	writersFile = open( PATH + WRITER_FILE )
	
	regex = re.compile(nameRegex + 
						splitRegex +
						titleRegex +
						weirdShitRegex)
	
	nWrites = 0
	
	for line in writersFile:
		matches = regex.match(line)
		if(matches and len(matches.group(1)) != 0):
			actorName = matches.group(1)
			addedPerson = False
		if(matches and matches.group(2) and not matches.group(3) and not matches.group(4)):
			try:
				if(matches.group(2) in titles):
					if(not addedPerson):
						clean = cleanName(actorName)	
						s.addPerson(clean)
						addedPerson = True
					s.addWriter(clean, matches.group(2))
			except:
				continue
	#		print writerName + " ::: " + matches.group(2)
			nWrites += 1
	
	print "FINISHED PARSING WRITERS : " + str(nWrites)
	
	#--------------------------------------------------------------------------------------
	#DIRECTORS
	
	directorsFile = open( PATH + DIRECTOR_FILE )
	
	nDirects = 0
	
	for line in directorsFile:
		matches = regex.match(line)
		if(matches and len(matches.group(1)) != 0):
			actorName = matches.group(1)
			addedPerson = False
		if(matches and matches.group(2) and not matches.group(3) and not matches.group(4)):
			try:
				if(matches.group(2) in titles):
					if(not addedPerson):
						clean = cleanName(actorName)	
						s.addPerson(clean)
						addedPerson = True
					s.addDirector(clean, matches.group(2))
					nDirects += 1
			except:
				continue
	#		print directorName + " ::: " + matches.group(2)
			
	print "FINISHED PARSING DIRECTORS : " + str(nDirects)
	
	
	#--------------------------------------------------------------------------------------
	#GENRES
	
	genresFile = open( PATH + GENRE_FILE )
	
	regex = re.compile(titleRegex +
						weirdShitRegex +
						splitRegex +
						'(.*)')
	
	for line in genresFile:
		matches = regex.match(line)
		if(matches and matches.group(1) and not matches.group(2) and not matches.group(3)):
			try:
				if(matches.group(1) in titles):
					s.addGenre(matches.group(1), matches.group(4))
					print matches.group(4) + " IS GENRE OF " + matches.group(1)
			except:
				continue
	#		print matches.group(1) + " ::: " + matches.group(4)
		
	
	
	#--------------------------------------------------------------------------------------
	#LOCATIONS
	
	locationsFile = open( PATH + LOCATION_FILE )
	
	regex = re.compile(titleRegex + 
						weirdShitRegex +
						splitRegex +
						'((.*, )*)(.*?)\s')
	
	for line in locationsFile:
		matches = regex.match(line)
		if(matches and matches.group(1) and not matches.group(2) and not matches.group(3)):
			try:
				if(matches.group(1) in titles):
					s.addLocation(matches.group(1), matches.group(6))
					print matches.group(1) + " SHOT IN " + matches.group(6)
			except:
				continue
	#		print matches.group(1) + " ::: " + matches.group(6)
			
	#--------------------------------------------------------------------------------------
	#RATINGS
	
	ratingsFile = open( PATH + RATING_FILE)
	
	re1 = re.compile('MV: ' + titleRegex + weirdShitRegex)
	re2 = re.compile('RE: Rated (.*?) ' )
	
	for line in ratingsFile:
		movieMatch = re1.match(line)
		if(movieMatch and movieMatch.group(1) and not movieMatch.group(2) and not movieMatch.group(3)):
			movie = movieMatch.group(1)
			movieFound = True
			continue
		ratingMatch = re2.match(line)
		if(ratingMatch and movieFound):
			rating = ratingMatch.group(1)
			try:
				if(movie in titles):
					s.addRating(movie, rating)
					print movie + " ::: " + rating
			except:
				continue
			movieFound = False
		
	s.exportData()