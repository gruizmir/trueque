function productSearchForm() {
	$("#productSearchForm").submit(function(event){
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
