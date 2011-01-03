function displayCells(obj) {
	elements = obj.parentNode.parentNode.getElementsByTagName('TR');
	
	for (el = 0; el < elements.length; el++) {
		elements[el].style.display='table-row';
	}
	
	obj.parentNode.style.display = "none";
}
