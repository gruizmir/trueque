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
			},
		});
	});
}

function enableCountry(){
    document.getElementById('filter_global').style.color="#a8a9ab";
    document.getElementById('filter_local').style.color="#000000";
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
    var lista = document.getElementsByClassName('search_country_filter');
    for (i = 0; i < lista.length; i++){
        lista[i].style.color="#a8a9ab";
    }
    document.getElementById(value).style.color="#000000";
    $.ajax({
		type: "GET",
		url: "/search/get_cities/" + value,
		success: function(data) {
			result = data.cities;
			$('#cities')[0].innerHTML = result;
			$.ajax({
		        data: $("#productSearchForm").serialize(),
        		type: $("#productSearchForm").attr('method'),
        		url: $("#productSearchForm").attr('action') + "country/" + value,
        		success: function(data) {
            		result = data.products;
        			$('#result')[0].innerHTML = result;
        		},
        	});
		},
	});
}

function searchByCity(city){
    var lista = document.getElementsByClassName('search_city_filter');
    for (i = 0; i < lista.length; i++){
        lista[i].style.color="#a8a9ab";
    }
    document.getElementById(city).style.color="#000000";
	$.ajax({
		data: $("#productSearchForm").serialize(),
		type: $("#productSearchForm").attr('method'),
		url: $("#productSearchForm").attr('action') + "city/" + city,
		success: function(data) {
			result = data.products;
			$('#result')[0].innerHTML = result;
		},
	});
}

function cleanSearch(){
	$.ajax({
		data: $("#productSearchForm").serialize(),
		type: $("#productSearchForm").attr('method'),
		url: $("#productSearchForm").attr('action'),
		success: function(data) {
			result = data.products;
			$('#result')[0].innerHTML = result;
		},
	});
}

function selectPop(){
    document.getElementById('pop_text').style.color="#000000";
    document.getElementById('price_text').style.color="#a8a9ab";
    document.getElementById('recent_text').style.color="#a8a9ab";
    document.getElementById('filter_popularity').checked=true;
    $.ajax({
		data: $("#productSearchForm").serialize(),
		type: $("#productSearchForm").attr('method'),
		url: $("#productSearchForm").attr('action'),
		success: function(data) {
			result = data.products;
			$('#result')[0].innerHTML = result;
		},
	});
}

function selectPrice(){
    document.getElementById('pop_text').style.color="#a8a9ab";
    document.getElementById('price_text').style.color="#000000";
    document.getElementById('recent_text').style.color="#a8a9ab";
    document.getElementById('filter_price').checked=true;
    $.ajax({
		data: $("#productSearchForm").serialize(),
		type: $("#productSearchForm").attr('method'),
		url: $("#productSearchForm").attr('action'),
		success: function(data) {
			result = data.products;
			$('#result')[0].innerHTML = result;
		},
	});
}

function selectRecent(){
    document.getElementById('pop_text').style.color="#a8a9ab";
    document.getElementById('price_text').style.color="#a8a9ab";
    document.getElementById('recent_text').style.color="#000000";
    document.getElementById('filter_recent').checked = true;
    $.ajax({
		data: $("#productSearchForm").serialize(),
		type: $("#productSearchForm").attr('method'),
		url: $("#productSearchForm").attr('action'),
		success: function(data) {
			result = data.products;
			$('#result')[0].innerHTML = result;
		},
	});
}

$(document).ready(function() {
    productSearchForm();
	$('#filter_local').bind('click', function () {
		enableCountry();
	});
	$('#filter_global').bind('click', function () {
	    document.getElementById('filter_local').style.color="#a8a9ab";
        document.getElementById('filter_global').style.color="#000000";
        $('#countries')[0].innerHTML = "";
        $('#cities')[0].innerHTML = "";
	    cleanSearch();
	});
	$('#pop_text').bind('click', function () {
	    selectPop();
	});
	$('#price_text').bind('click', function () {
	    selectPrice();
	});
	$('#recent_text').bind('click', function () {
	    selectRecent();
	});
});
