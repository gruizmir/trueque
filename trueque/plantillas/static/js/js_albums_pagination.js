function add_album_form(){
	$("#add_album_form").submit(function(event){
		event.preventDefault();
		$.ajax({
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			success: function(data) {
				if(data.album_form_result == false){
					result = data.add_album_render;
				}
				else{
					result = data.add_album_message;
					$('#dialog_add_album').dialog({
						 buttons: {
							Cerrar: function() {
								var options = {
								    buttons: {}
								};
								$(this).dialog('option', options);
								location.reload();
								$(this).dialog( "close" );
							}
						}
					});
				}
				$('#dialog_add_album_result')[0].innerHTML = result;
					add_album_form();
				}
			});
		});
	}

function albumsPagination(){
	$('.pag').bind('click', function () {
		var url = window.location + "";
		if(!url.match("/$")){
			url = url + "/"
		}
		$.get(url + this.id, function(data) {
			result = data.albums_data;
			$('#result')[0].innerHTML = result;
			$(".album_polaroids_container").mCustomScrollbar();
			
			$('#dialog_add_album').dialog({
				autoOpen: false,
				draggable: false,
			    resizable: false,
			    title: 'Nuevo álbum'
			});
			$('#add_album_button').bind('click', function () {
				$.get("/usuarios/profile/addalbum", function(data) {
					result = data;
					$('#dialog_add_album_result')[0].innerHTML = result;
					add_album_form();
				});
				$('#dialog_add_album').dialog('open');
			});
			
			albumsPagination();
		});
	});
}

$(document).ready(function() {
	$(".album_polaroids_container").mCustomScrollbar();
	$('#dialog_add_album').dialog({
		autoOpen: false,
		draggable: false,
	    resizable: false,
	    title: 'Nuevo álbum'
	});
	$('#add_album_button').bind('click', function () {
		$.get("/usuarios/profile/addalbum", function(data) {
			result = data;
			$('#dialog_add_album_result')[0].innerHTML = result;
			add_album_form();
		});
		$('#dialog_add_album').dialog('open');
	});
	albumsPagination();
});