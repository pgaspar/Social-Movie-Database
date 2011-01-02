from SMDB import SMDB
import datetime

s = SMDB()

s.printTripleCount()

#s.addMovie('Pulp Fiction (1994)', datetime.date(1994, 11, 25))
#s.addMovie('Something Else (1992)', datetime.date(1992, 12, 01))

#s.addPerson('John Travolta')
#s.addPerson('Uma Thurman')
#s.addPerson('Quentin Tarantino')

#s.addPerformance('John Travolta', 'Pulp Fiction (1994)')
#s.addPerformance('Uma Thurman', 'Pulp Fiction (1994)')
#s.addPerformance('Quentin Tarantino', 'Pulp Fiction (1994)')

#s.addDirector('Quentin Tarantino', 'Pulp Fiction (1994)')

#s.addWriter('Quentin Tarantino', 'Pulp Fiction (1994)')

#s.addCharacter('Pulp Fiction (1994)', 'John Travolta', 'Vincent Vega')
#s.addCharacter('Pulp Fiction (1994)', 'Uma Thurman', 'Mia Wallace')

#s.addSMDBUser('mtavares')
#s.addSMDBUser('pgaspar')

#s.addFriendship('mtavares', 'pgaspar')
#s.addMovieSeen('mtavares', 'Pulp Fiction (1994)')
#s.addMovieReview(1, 'This movie is awesome[*****]', 'Pulp Fiction (1994)', 'mtavares')

#s.printTripleCount()

s.exportData()