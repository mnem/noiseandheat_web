function maybe_clear_prompt(event) {
	if(this.value == this.defaultValue) {
		$("#emailaddress").val("");
	}
}

function maybe_show_prompt(event) {
	if(this.value == "") {
		$("#emailaddress").val(this.defaultValue);
		email_style_prompt();
	} else {
		validate_mail();
	}
}

function check_mail_entry(event) {
	validate_mail();
}

function validate_mail() {
	if(email_address_valid($("#emailaddress").val())) {
		email_style_valid();
	} else {
		email_style_invalid();
	}
}

function submit_mail_and_fetch_track() {
	var mail_address = $("#emailaddress").val();
	if(email_address_valid(mail_address)) {
		alert("This is where you'd get a download");
	}
}

function email_style_prompt() {
	$("#emailaddress").removeClass("emailaddress-prompt emailaddress-valid emailaddress-invalid");
	$("#emailaddress").addClass("emailaddress-prompt");

	$("#button").removeClass("make-see-through");
	$("#button").addClass("make-see-through");
}

function email_style_valid() {
	$("#emailaddress").removeClass("emailaddress-prompt emailaddress-valid emailaddress-invalid");
	$("#emailaddress").addClass("emailaddress-valid");

	$("#button").removeClass("make-see-through");
}

function email_style_invalid() {
	$("#emailaddress").removeClass("emailaddress-prompt emailaddress-valid emailaddress-invalid");
	$("#emailaddress").addClass("emailaddress-invalid");

	$("#button").removeClass("make-see-through");
	$("#button").addClass("make-see-through");
}

function email_address_valid(email)
{
	var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
	return email.match(re)
}
$(document).ready(function() {
	email_style_prompt();

	$("#emailaddress").focus(maybe_clear_prompt);
	$("#emailaddress").blur(maybe_show_prompt);
	$("#emailaddress").keypress(check_mail_entry);

	$("#submit-email").click(submit_mail_and_fetch_track);
});
