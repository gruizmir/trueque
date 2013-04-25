placeholder = "";
$('input[type=text]').blur(function(){
	$(this).attr("placeholder", placeholder);
	});
$('input:password').blur(function(){
	$(this).attr("placeholder", placeholder);
	});
$('input[type=text]').focus(function(){
	placeholder = $(this).attr("placeholder");
	$(this).attr("placeholder", "");
	});
$('input:password').focus(function(){
	placeholder = $(this).attr("placeholder");
	$(this).attr("placeholder", "");
	});