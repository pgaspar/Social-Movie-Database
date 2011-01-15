function showReviewForm (argument) {
	var rev = document.getElementById('review-form');
	rev.style.display='block';
	document.getElementById('id_text').focus()
	
	elements = getElementsByClassName('new-review', document);
	for (el = 0; el < elements.length; el++) {
		elements[el].style.display='none';
	}
}

function getElementsByClassName(classname, node)  {
    if(!node) node = document.getElementsByTagName("body")[0];
    var a = [];
    var re = new RegExp('\\b' + classname + '\\b');
    var els = node.getElementsByTagName("*");
    for(var i=0,j=els.length; i<j; i++)
        if(re.test(els[i].className))a.push(els[i]);
    return a;
}