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

function enableCountry(){
    $.ajax({
		type: "GET",
		url: "/search/get_countries",
		success: function(data) {
			result = data.countries;
			$('#countries')[0].innerHTML = result;
		},
	});
}

function enableCity(value){
    $.ajax({
		type: "GET",
		url: "/search/get_cities/" + value,
		success: function(data) {
			result = data.cities;
			$('#cities')[0].innerHTML = result;
		},
	});
}

function searchByCity(city){
	$.ajax({
		data: $("#productSearchForm").serialize(),
		type: $("#productSearchForm").attr('method'),
		url: $("#productSearchForm").attr('action') + city,
		success: function(data) {
			result = data.products;
			$('#result')[0].innerHTML = "";
			console.log(result);
			$('#result')[0].innerHTML = result;
			productSearchForm();
		},
	});
}

$(document).ready(function() {
    productSearchForm();
	$('#filter_local').bind('click', function () {
		enableCountry();
	});
	
});
