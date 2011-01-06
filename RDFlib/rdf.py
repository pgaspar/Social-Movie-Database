from SMDB import SMDB
import datetime

s = SMDB()

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

s.addSMDBUser('mtavares')
s.addSMDBUser('pgaspar', 'Pedro Gaspar')
s.addSMDBUser('user_test')
s.addSMDBUser('user_test_all')

s.addFriendship('mtavares', 'pgaspar')
s.addFriendship('mtavares', 'user_test')
s.addFriendship('mtavares', 'user_test_all')

s.addMovieSeen('mtavares', 'Pulp Fiction (1994)')
s.addMovieSeen('pgaspar', 'Corpse Bride (2005)')
s.addMovieSeen('pgaspar', 'Pulp Fiction (1994)')
s.addMovieSeen('user_test_all', 'Corpse Bride (2005)')

s.addMovieReview(1, 'This movie is awesome[*****]', 'Pulp Fiction (1994)', 'mtavares')
s.addMovieReview(2, 'It was ok.', 'Corpse Bride (2005)', 'user_test_all')

s.printTripleCount()

#s.printTripleCount()

#s.exportData()