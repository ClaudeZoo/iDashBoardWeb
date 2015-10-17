$(document).ready(function () {
	$('#user-name-label').hide();
	$('#navbar-collapse-body').hide();

	$('#user-info-form').validate({
		rules: {
			username: "required",
			email: {
				required: true,
				email: true
			},
			password: {
				required: true,
				minlength: 6
			},
			confirmpassword: {
				required: true,
				equalTo: "#password"
			}
		}
	});


	$('#user-name').bind('blur', function(){
		name = $("#user-name").val();
		$.get("/validateUserName/", {'userName':name}, function(ret){
			$('#user-name-label').text('Someone already has that username. Try another?');
			if (ret == "no"){
				$('#user-name-label').show();
			}
			else{
				$('#user-name-label').hide();
			}
		})
	});
});
