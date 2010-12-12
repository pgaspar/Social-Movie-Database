reverse = {
	'smdb:directedBy': 'smdb:directed',
	'smdb:featured': 'smdb:performedIn',
	'smdb:hasReview': 'smdb:refersTo',
	'smdb:hasWritten': 'smdb:writtenByUser',
	'smdb:playsCharacter': 'smdb:portrayedBy',
	'smdb:writtenBy': 'smdb:wrote',
	'smdb:isFriendsWith': 'smdb:isFriendsWith',
}

reverse.update( dict( [(b, a) for a, b in reverse.items()] ) )	# Add reverses