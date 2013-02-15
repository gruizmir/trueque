# -*- coding: utf-8 -*-
from django import forms
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.core.mail import send_mail
from django.db.utils import DatabaseError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.datetime_safe import datetime
from usuarios.form import RegisterUserForm, SendConfirmationForm, LoginForm, \
    EditUserForm
from usuarios.models import Usuario
import socket
import usuarios.custom_error as C_error
import usuarios.form

SESSION_EXPIRY = 86400 #Tiempo de expiracion de la sesion encargada de la verificacion.

#register: funcion encargada de desplegar el formulario de registro y de ingresar los datos
#          del usuario en la base de datos.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#RETURN: Se devuelven distintos render_to_response dependiendo de como termine el registro.
def register(request):
    try:
        if request.method == 'POST':
            form = RegisterUserForm(request.POST)

            if form.is_valid():
                new_register = form.save(commit=False)
                new_register.usuario_register_date = datetime.now()
                
                #Se crea una session para la verificacion via email de la activacion de cuenta
                #del usuario que se esta intentando registrar.
                session_s = SessionStore()
                session_s['user_mail'] = new_register.usuario_email_1
                session_s['user_name'] = new_register.usuario_name
                session_s.set_expiry(SESSION_EXPIRY)
                session_s.save(must_create=True)      
                new_register.save()
                return send_registration_confirmation(session_s)
        else:
            form = RegisterUserForm()
        
        c = { 'form': form }
        c.update(csrf(request))
        return render_to_response('register_form.html', c)
    
    #Exceptions que se activan en caso de no poder registrar al usuario en la base de datos o
    #por alguna accion extraña durante el registro.
    except SuspiciousOperation: return C_error.raise_error(C_error.PERMISSIONDENIED)
    except DatabaseError: return C_error.raise_error(C_error.DATABASEERROR)
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        return C_error.raise_error(C_error.REGISTERMODULEERROR)

#send_registration_confirmation: funcion encargada de enviar el mail de confirmacion de
#                                registro al usuario.
#PARAMS: session_s: Sesion creada durante el registro del usuario, contiene nombre y mail.
#RETURN: Se devuelven distintos render_to_response dependiendo de como termine el envio del email.
def send_registration_confirmation(session_s):
    try:
        title = "WELCOME TO TRUEQUE!"
        content = ("http://localhost:8000/usuarios/confirm/?=" + str(session_s.session_key) + "&email=" + session_s['user_mail'])
        print content
        send_mail(title, content, 'no-reply@trueque.com', [session_s['user_mail']], fail_silently=False)
        return render_to_response('register_mail_confirmation.html')
    
    #Exceptions que se activan en caso de no poder enviar el mail al usuario.
    except socket.error: return C_error.raise_error(C_error.EMAILSERVERDOWN)
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        return C_error.raise_error(C_error.USERREGISTEREDWITHMAGICERROR)

#confirm: esta encargado de validar a un usuario como activo
#         a traves de la llave enviada a su email
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#RETURN: Se devuelven distintos render_to_response dependiendo de como termine la verificacion.
def confirm(request):
    try:
        session_s, user_mail, user = None, None, None
        
        #Obtener llave de sesion y mail de usuario a partir del GET
        if request.method == 'GET':
            session_s = SessionStore(session_key=request.GET[''])
            user_mail = request.GET['email']    
        else: return C_error.raise_error(C_error.PERMISSIONDENIED)

        #Verificar que coinciden el email de sesion y el email que se entrega para obtener
        #al usuario a traves del email
        if session_s['user_mail'] == user_mail:
            user = Usuario.objects.get(usuario_email_1=session_s['user_mail'])
        else: return C_error.raise_error(C_error.EXPIREDKEY)

        #Verificar que el usuario no este activo para activarlo. Una vez activado se borra
        #la sesion.
        if(user.usuario_active == False):
            user.usuario_active = True
            user.save()
            session_s.delete()
            return render_to_response('register_complete.html')
        else: return C_error.raise_error(C_error.USERALREADYACTIVE)    
    
    #Exceptions que se pueden producir por algun fallo durante la activacion de la cuenta.   
    except KeyError: return C_error.raise_error(C_error.INVALIDEXPIREDKEY)
    except ObjectDoesNotExist: return C_error.raise_error(C_error.UNREGISTEREDUSER)
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        return C_error.raise_error(C_error.MAGICERROR)

#resend_confirmation : Funcion encargada de desplegar un formulario con el campo de email
#                      para que el usuario reenvie su codigo de confirmacion.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#RETURN: Se devuelven distintos render_to_response dependiendo de como termine el reenvio.
def resend_confirmation(request):
    try:
        if request.method == 'POST':
            form = SendConfirmationForm(request.POST)
            if form.is_valid():
                session_s = SessionStore()
                session_s['user_mail'] = form.cleaned_data['usuario_email_1']
                session_s.set_expiry(SESSION_EXPIRY)
                session_s.save(must_create=True)
                
                user = Usuario.objects.get(usuario_email_1=session_s['user_mail'])
                if(user.usuario_active == False):
                    return send_registration_confirmation(session_s)
                else: return C_error.raise_error(C_error.USERALREADYACTIVE)    
        else:
            form = SendConfirmationForm()
        
        c = { 'form': form }
        c.update(csrf(request))
        return render_to_response('register_form.html', c)
    
    #Exceptions que se pueden producir por algun fallo durante el reenvio de la llave de confirmacion.    
    except ObjectDoesNotExist as e: return C_error.raise_error(C_error.UNREGISTEREDUSER)
    except Exception:
        print '%s (%s)' % (e.message, type(e))
        return C_error.raise_error(C_error.MAGICERROR)

#login: Funcion encargada de iniciar la sesion del usuario.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#RETURN: Se devuelven distintos render_to_response dependiendo de como termine el reenvio y se
#        agrega el id del usuario al request.
def login(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            
            if request.session.test_cookie_worked(): request.session.delete_test_cookie()
            else: return C_error.raise_error(C_error.NOCOOKIE)
            
            if form.is_valid():
                form.cleaned_data['usuario_email_1']
                user = Usuario.objects.get(usuario_email_1=form.cleaned_data['usuario_email_1'])   
                request.session['member_id'] = user.id_usuario
                request.session.set_expiry(0)
                request.session.save()
                
                session_s = Session.objects.get(pk=request.session.session_key)
  
                return HttpResponse("Logged :" + str(session_s.session_key)
                                    + "<br>" + str(session_s.expire_date)
                                    + "<br>" + str(session_s.get_decoded()))
        else:
            form = LoginForm()
        
        request.session.set_test_cookie()
        c = { 'form': form }
        c.update(csrf(request))
        return render_to_response('register_form.html', c)
    
    #Exceptions que se activan en caso de no poder iniciar sesion.
    except SuspiciousOperation: return C_error.raise_error(C_error.PERMISSIONDENIED)
    except DatabaseError: return C_error.raise_error(C_error.DATABASEERROR)
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        return C_error.raise_error(C_error.MAGICERROR)

#edit_user_profile: Funcion encargada de modificar los datos de un usuario
#PARAMS: request:  Objeto que contiene toda la informacion enviada por el navegador del usuario.
#RETURN:  Se devuelven distintos render_to_response dependiendo de como la modificacion de informacion.
def edit_user_profile(request):
    try:
        user = Usuario.objects.get(id_usuario= request.session['member_id'])
        if request.method == 'POST' :
            form = EditUserForm(request.POST, instance=user)
            
            #Se verifica que la contraseña ingresada sea la que corresponde.
            if form.data['usuario_password'] and forms.CharField().clean(form.data['usuario_password']) and user.usuario_password != forms.CharField().clean(form.data['usuario_password']):
                form.errors['usuario_password'] = form.error_class([usuarios.form.ERROR_WRONGPASS])
                
            if form.is_valid():
                edit_register = form.save(commit=False)
                if form.cleaned_data["new_password"]:
                    edit_register.usuario_password = form.cleaned_data["new_password"]
                edit_register.save()
        else:
            form = EditUserForm(instance=user)
            
        request.session.set_test_cookie()
        c = { 'form': form }
        c.update(csrf(request))
        return render_to_response('register_form.html', c)
    
    #Exceptions que se activan en caso de no poder iniciar sesion.
    except KeyError: return C_error.raise_error(C_error.NEEDLOGIN)
    except SuspiciousOperation: return C_error.raise_error(C_error.PERMISSIONDENIED)
    except ObjectDoesNotExist as e: return C_error.raise_error(C_error.UNREGISTEREDUSER)
    except DatabaseError: return C_error.raise_error(C_error.DATABASEERROR)
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        return C_error.raise_error(C_error.MAGICERROR)