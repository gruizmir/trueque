lastclick = "";

function pagPagination(){
	$('.pag').bind('click', function () {
		$.get("/usuarios/profile/"+ lastclick + this.id, function(data) {
			result = data.mail_inbox;
			$('#result')[0].innerHTML = result;
			pagPagination();
		});
	});
	
	$('.mail_container').bind('click', function () {
		if ( this.className.match(/(?:^|\s)mail_container(?!\S)/) ){
			this.classList.remove('mail_container');
			this.classList.add('mail_container_show');
		}
		else{
			this.classList.remove('mail_container_show');
			this.classList.add('mail_container');
		}
	});
}

function sendMailForm() {
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
			pagPagination();
		});
	});
});