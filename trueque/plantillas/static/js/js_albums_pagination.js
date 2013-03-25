function albumsPagination(){
	$('.pag').bind('click', function () {
		var url = window.location + "";
		if(!url.match("/$")){
			url = url + "/"
		}
		$.get(url + this.id, function(data) {
			result = data.albums_data;
			$('#result')[0].innerHTML = result;
			albumsPagination();
		});
	});
}

$(document).ready(function() {
	albumsPagination();
});