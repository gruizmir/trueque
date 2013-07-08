function showHiddeSearchForm() {
	if($(".cat_list_container").css("display") == "block") {
		$(".cat_list_container").css("display", "none");
		$(".up_down_button_img").attr("src", "/static/img/icons/drop-down-icon20.png");
	}
	else{
		$(".cat_list_container").css("display", "block");
		$(".up_down_button_img").attr("src", "/static/img/icons/drop-up-icon20.png");
	}
}

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
				rotatePolaroids();
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
			rotatePolaroids();
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
            		console.log(result)
        			$('#result')[0].innerHTML = result;
        			rotatePolaroids();
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
			console.log(result)
			$('#result')[0].innerHTML = result;
			rotatePolaroids();
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
			rotatePolaroids();
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
			rotatePolaroids();
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
			rotatePolaroids();
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
			rotatePolaroids();
		},
	});
}

//===== Precios ===============

function selectLow(){
    if(document.getElementById('filter_low').checked){
        document.getElementById('filter_low').checked = false;
        document.getElementById('filter_low').style.color="#a8a9ab";
    }
    else{
        document.getElementById('filter_low').checked = true;
        document.getElementById('filter_low').style.color="#000000";
    }
    $.ajax({
		data: $("#productSearchForm").serialize(),
		type: $("#productSearchForm").attr('method'),
		url: $("#productSearchForm").attr('action'),
		success: function(data) {
			result = data.products;
			$('#result')[0].innerHTML = result;
			rotatePolaroids();
		},
	});
}

function selectMedium(){
    if(document.getElementById('filter_medium').checked){
        document.getElementById('filter_medium').checked = false;
        document.getElementById('filter_medium').style.color="#a8a9ab";
    }
    else{
        document.getElementById('filter_medium').checked = true;
        document.getElementById('filter_medium').style.color="#000000";
    }
    $.ajax({
		data: $("#productSearchForm").serialize(),
		type: $("#productSearchForm").attr('method'),
		url: $("#productSearchForm").attr('action'),
		success: function(data) {
			result = data.products;
			$('#result')[0].innerHTML = result;
			rotatePolaroids();
		},
	});
}

function selectHigh(){
    if(document.getElementById('filter_high').checked){
        document.getElementById('filter_high').checked = false;
        document.getElementById('filter_high').style.color="#a8a9ab";
    }
    else{
        document.getElementById('filter_high').checked = true;
        document.getElementById('filter_high').style.color="#000000";
    }
    
    $.ajax({
		data: $("#productSearchForm").serialize(),
		type: $("#productSearchForm").attr('method'),
		url: $("#productSearchForm").attr('action'),
		success: function(data) {
			result = data.products;
			$('#result')[0].innerHTML = result;
			rotatePolaroids();
		},
	});
}

function getRandomInt (min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function rotatePolaroids() {
	$("[id^='album_polaroid_']").filter(function() {
		var rand_deg = getRandomInt (-3, 3);
		$('#'+this.id).css({ WebkitTransform: 'rotate(' + rand_deg + 'deg)',
			'-moz-transform': 'rotate(' + rand_deg + 'deg)',
			'-o-transform': 'rotate(' + rand_deg + 'deg)',
			'-ms-transform': 'rotate(' + rand_deg + 'deg)',
			'transform': 'rotate(' + rand_deg + 'deg)'
		});
	});
}

//===== Post cargado ==========
$(document).ready(function() {
	rotatePolaroids();
	
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
	$('#filter_low').bind('click', function () {
	    selectLow();
	});
	$('#filter_medium').bind('click', function () {
	    selectMedium();
	});
	$('#filter_high').bind('click', function () {
	    selectHigh();
	});

});
