from django.shortcuts import render_to_response
from usuarios.forms import UsuarioForm
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

def reg(request):
	regForm = UsuarioForm()
	return render_to_response("index.html", {'reg_form':regForm},context_instance=RequestContext(request))

def save(request):
	if request.method == "POST":
		form = UsuarioForm(request.POST)
		form.save()
#		if form.is_valid():
#			form.save()
#			return HttpResponse('OK')
#		else:
#			print form
#			return HttpResponse('NO valido')
	return HttpResponse('FAIL')
