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

var wrapper = $('<div/>').css({height:0,width:0,'overflow':'hidden'});
var fileInput = $(':file').wrap(wrapper);

fileInput.change(function(){
    $this = $(this);
    $('#file').text($this.val());
})

$('#file').click(function(){
    fileInput.click();
}).show();