from SMDB import SMDB

s = SMDB()

s.printTripleCount()

s.addMovie(s.smdb['movie:1'], 'Pulp Fiction', 154)

s.addPerson(s.smdb['person:1'], 'John Travolta', 'Test Biography')
s.addPerson(s.smdb['person:2'], 'Uma Thurman')
s.addPerson(s.smdb['person:3'], 'Quentin Tarantino', "Quentin's biography")

s.addPerformance(s.smdb['person:1'], s.smdb['movie:1'])
s.addPerformance(s.smdb['person:2'], s.smdb['movie:1'])
s.addPerformance(s.smdb['person:3'], s.smdb['movie:1'])

s.addDirection(s.smdb['person:3'], s.smdb['movie:1'])

s.addWriting(s.smdb['person:3'], s.smdb['movie:1'])

s.addCharacter(s.smdb['character:1'], 'Vincent Vega', s.smdb['person:1'], [s.smdb['movie:1']])
s.addCharacter(s.smdb['character:2'], 'Mia Wallace', s.smdb['person:2'], [s.smdb['movie:1']])

s.addSMDBUser(s.smdb['user:1'], 'mtavares')
s.addSMDBUser(s.smdb['user:2'], 'pgaspar')

s.addFriendship(s.smdb['user:1'], s.smdb['user:2'])
s.addMovieSeen(s.smdb['user:1'], s.smdb['movie:1'])
s.addMovieReview(s.smdb['review:1'], 'This movie is awesome[*****]', s.smdb['movie:1'], s.smdb['user:1'])

s.printTripleCount()

s.exportData()