function goToPage (pageID) {
	hideEveryPage();
	var page = document.getElementById('page-'+pageID);
	page.style.display = 'block';
	currentPage = pageID;
	
	// Update page counter
	var marker = document.getElementById('nav-current-page');
	marker.innerHTML = currentPage;
	
	// Hide nav if not needed
	var nav_lower = document.getElementById('nav-lower');
	var nav_higher = document.getElementById('nav-higher');
	
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

function goToFirst () {
	goToPage(1);
}

function goToLast () {
	goToPage(finalPage);
}