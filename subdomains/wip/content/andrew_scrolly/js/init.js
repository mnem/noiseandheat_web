// This function handles the razor link being clicked
// It's attached to the link in the document ready
// function at the end of the source file
function go_razor() {
	// Scrolls to the element with the ID "razor"
	// over 1 second (1000 milliseconds)
	$.scrollTo("#razor", 1000);
}

// This code runs after the web page has loaded
$(document).ready(function() {
	// Find the go-razor link and add a click event handler
	$("#go-razor").click(go_razor);
});
