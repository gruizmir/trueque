function productSearchForm() {
	$("#productSearchForm").submit(function(event){
		event.preventDefault();
		$.ajax({
			data: $(this).serialize(),
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			success: function(data) {
				result = data.products;
				$('#result')[0].innerHTML = result;
				productSearchForm();
			},
		});
	});
}

$(document).ready(function() {
    productSearchForm();
//	$('.search_secondary_filter').bind('click', function () {
//		$.get("/search/category/", function(data) {
//			result = data.products;
//			$('#result')[0].innerHTML = result;
			
//		});
//	});
});
