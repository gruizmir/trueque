lastclick = "";

function pagPagination(){
	$('.pag').bind('click', function () {
		$.get("/usuarios/profile/"+ lastclick + this.id, function(data) {
			result = data.mail_inbox;
			$('#result')[0].innerHTML = result;
			pagPagination();
		});
	});
}

function sendMailForm() {
	$('.mail').bind('click', function () {
		lastclick = this.id;
		$.get("/usuarios/profile/"+this.id, function(data) {
			result = data.mail_inbox;
			$('#result')[0].innerHTML = result;
			sendMailForm();
		});
	});

	pagPagination();

	$("#sendMailForm").submit(function(event){
		event.preventDefault();
		$.ajax({
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			success: function(data) {
				result = data.mail_inbox;
				$('#result')[0].innerHTML = result;
				sendMailForm();
			}
		});
	});
}

$(document).ready(function() {
	$('.mail').bind('click', function () {
		lastclick = this.id;
		$.get("/usuarios/profile/"+this.id, function(data) {
			result = data.mail_inbox;
			$('#result')[0].innerHTML = result;
			sendMailForm();
		});
	});
});