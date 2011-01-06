function goToPage (pageID) {
		
	hideEveryPage();
	var page = document.getElementById('page-'+pageID);
	page.style.display = 'block';
	currentPage = pageID;
	
	// Update page counter
	var marker = document.getElementById('nav-current-page');
	marker.innerHTML = currentPage;
	
	// Hide nav if not needed
	var nav_lower = document.getElementById('nav-lower-page');
	var nav_higher = document.getElementById('nav-higher-page');
	
	if (currentPage == 1) {
		nav_lower.style.display = 'none';
		nav_higher.style.display = 'inline';
	}
	else if (currentPage == finalPage) {
		nav_higher.style.display = 'none';
		nav_lower.style.display = 'inline';
	}
	else {
		nav_lower.style.display = 'inline';
		nav_higher.style.display = 'inline';
	}
	
}

function hideEveryPage () {
	for (var i = 1; i <= finalPage; i++) {
		var page = document.getElementById('page-'+i);
		page.style.display = 'none';
	}
}

function goToFirstPage () {
	goToPage(1);
}

function goToLastPage () {
	goToPage(finalPage);
}

//Movies

function goToMovie (pageID) {
		
	hideEveryMovie();
	var page = document.getElementById('movie-'+pageID);
	page.style.display = 'block';
	currentMovie = pageID;
	
	// Update page counter
	var marker = document.getElementById('nav-current-Movie');
	marker.innerHTML = currentMovie;
	
	// Hide nav if not needed
	var nav_lower = document.getElementById('nav-lower-Movie');
	var nav_higher = document.getElementById('nav-higher-Movie');
	
	if (currentMovie == 1) {
		nav_lower.style.display = 'none';
		nav_higher.style.display = 'inline';
	}
	else if (currentMovie == finalMovie) {
		nav_higher.style.display = 'none';
		nav_lower.style.display = 'inline';
	}
	else {
		nav_lower.style.display = 'inline';
		nav_higher.style.display = 'inline';
	}
	
}

function hideEveryMovie () {
	for (var i = 1; i <= finalMovie; i++) {
		var page = document.getElementById('movie-'+i);
		page.style.display = 'none';
	}
}

function goToFirstMovie () {
	goToMovie(1);
}

function goToLastMovie () {
	goToMovie(finalMovie);
}

//People
function goToPerson (pageID) {
		
	hideEveryPerson();
	var page = document.getElementById('person-'+pageID);
	page.style.display = 'block';
	currentPerson = pageID;
	
	// Update page counter
	var marker = document.getElementById('nav-current-Person');
	marker.innerHTML = currentPerson;
	
	// Hide nav if not needed
	var nav_lower = document.getElementById('nav-lower-Person');
	var nav_higher = document.getElementById('nav-higher-Person');
	
	if (currentPerson == 1) {
		nav_lower.style.display = 'none';
		nav_higher.style.display = 'inline';
	}
	else if (currentPerson == finalPerson) {
		nav_higher.style.display = 'none';
		nav_lower.style.display = 'inline';
	}
	else {
		nav_lower.style.display = 'inline';
		nav_higher.style.display = 'inline';
	}
	
}

function hideEveryPerson () {
	for (var i = 1; i <= finalPerson; i++) {
		var page = document.getElementById('person-'+i);
		page.style.display = 'none';
	}
}

function goToFirstPerson () {
	goToPerson(1);
}

function goToLastPerson () {
	goToPerson(finalPerson);
}


//Characters

function goToChar (pageID) {
		
	hideEveryChar();
	var page = document.getElementById('char-'+pageID);
	page.style.display = 'block';
	currentChar = pageID;
	
	// Update page counter
	var marker = document.getElementById('nav-current-Char');
	marker.innerHTML = currentChar;
	
	// Hide nav if not needed
	var nav_lower = document.getElementById('nav-lower-Char');
	var nav_higher = document.getElementById('nav-higher-Char');
	
	if (currentChar == 1) {
		nav_lower.style.display = 'none';
		nav_higher.style.display = 'inline';
	}
	else if (currentChar == finalChar) {
		nav_higher.style.display = 'none';
		nav_lower.style.display = 'inline';
	}
	else {
		nav_lower.style.display = 'inline';
		nav_higher.style.display = 'inline';
	}
	
}

function hideEveryChar () {
	for (var i = 1; i <= finalChar; i++) {
		var page = document.getElementById('char-'+i);
		page.style.display = 'none';
	}
}

function goToFirstChar () {
	goToChar(1);
}

function goToLastChar () {
	goToChar(finalChar);
}