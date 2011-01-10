function go_razor() {
	$.scrollTo("#razor", 1000);
}

$(document).ready(function() {
	$('div.pane').scrollTo( 0 );
	$.scrollTo( 0 );
	$("#go-razor").click(go_razor);
});
