/**
 * Created by wcx on 15/5/4.
 */


$(document).ready(function () {
	user_validate();
});
function user_validate(){
	$('#apply-form').validate({
		rules: {
			password: {
				required: true,
				minlength: 6
			},
			pwd_confirm: {
				required: true,
				equalTo: "#password"
			}
		}
	});
}
function form_submit(){
	document.getElementById('apply-form').submit();
	return true;
}