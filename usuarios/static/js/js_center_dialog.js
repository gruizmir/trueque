/* Dialog Array*/
var dialogArray = new Array();

/* Clase/constructor encargada de crear nuevos dialogs*/
function newDialog(dialog_bg, dialog_container_bg){
	this.dialog_background = dialog_bg;
	this.dialog_container_background = dialog_container_bg;
}
/* Funcion encargada de "cerrar" el dialog */
function close_dialog(dialog_bg, dialog_container_bg) {
	document.getElementById(dialog_bg).style.display='none';
	document.getElementById(dialog_container_bg).style.display='none';
}
/* Funcion encargada de "abrir" el dialog */
function openDialog(dialog_bg, dialog_container_bg) {
	document.getElementById(dialog_bg).style.display='block';
	document.getElementById(dialog_container_bg).style.display='block';
}
/* Funcion encargada de centrar el dialog con respecto a su background */
newDialog.prototype.centerDialog = function centerDialog() {
	var dialogBack = document.getElementById(this.dialog_background);
	var dialogCont = document.getElementById(this.dialog_container_background);
	if(dialogBack.offsetWidth > dialogCont.offsetWidth){
		var dif = dialogBack.offsetWidth/2 - dialogCont.offsetWidth/2;
		dialogCont.style.left = dif + "px";
	}
	else{
		dialogCont.style.left = '0';
	}
	if(dialogBack.offsetHeight > dialogCont.offsetHeight){
		var dif = dialogBack.offsetHeight/2 - dialogCont.offsetHeight/2;
		dialogCont.style.top = dif + "px";
	}
	else{
		dialogCont.style.top = '0';
	}
};

function closeDialog(id) {
	document.getElementById("dialog_background").style.display='none';
	document.getElementById("dialog_container_background").style.display='none';
}

/* Funcion encargada de cargar dialogs a ser centrados */
function loadDialog(dialog_bg, dialog_container_bg){
	dialogArray[dialogArray.length] = new newDialog(dialog_bg, dialog_container_bg);
	dialogArray[dialogArray.length-1].centerDialog();
}

/* Funcion que mantiene todos los dialogs centrados */
window.onresize = function(event) {
	for (var i=0; i<=dialogArray.length; i++){ dialogArray[i].centerDialog(); } 
}