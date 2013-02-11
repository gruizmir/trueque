from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.utils.datetime_safe import datetime
from usuarios.form import RegisterUserForm

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            new_register = form.save(commit=False)
            new_register.usuario_register_date = datetime.now()
            new_register.save()
    else:
        form =  RegisterUserForm()
    
    c = {'form': form }
    c.update(csrf(request))
    return render_to_response('register_form.html', c)
