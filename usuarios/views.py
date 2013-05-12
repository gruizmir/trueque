# -*- coding: utf-8 -*-
from albums.form import AddAlbumForm
from django import forms
from django.contrib.sessions.backends.db import SessionStore
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation, \
    ValidationError
from django.core.mail import send_mail
from django.db.utils import DatabaseError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
from messages.form import ComposeMailForm
from messages.models import Message
from usuarios.form import RegisterUserForm, SendConfirmationForm, LoginForm, \
    EditUserForm
from usuarios.models import Usuario, Followers
import albums.utils as albums_utils
import os
import socket
import usuarios.custom_error as C_error
import usuarios.form
import random
from django.conf import settings

SESSION_EXPIRY = 86400 #Tiempo de expiracion de la sesion encargada de la verificacion.

#Nombres de los albumes
ALBUM_NAME_GARAGE = "My Garage"
ALBUM_NAME_TRUEQUES = "Trueques"
ALBUM_NAME_LIKE = "Me gusta"
ALBUM_NAME_RECOMMEND = "Recomiendo"
ALBUMES = [ALBUM_NAME_GARAGE, ALBUM_NAME_TRUEQUES, ALBUM_NAME_LIKE, ALBUM_NAME_RECOMMEND]
MAILSENTCOMPLETE = "Mail enviado correctamente"

# Translators: Terms of service agreement
REGISTER_TERMS_OF_SERVICE = _("I agree with terms and conditions of service.")
# Translators: Bulletins agreement on register
REGISTER_USER_BULLETINS = _("I want get email bulletins.")

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
                
                #Se crean los primeros cuatro albums por defecto
                for name in ALBUMES:
                    user = Usuario.objects.get(usuario_email_1=new_register.usuario_email_1)
                    albums_utils.add_album(user, name, False, True)
                
                return send_registration_confirmation(session_s)
        else:
            form = RegisterUserForm()
            
        absolute_path = os.path.dirname(os.path.realpath(__file__))
        bg_imgs_folder = os.path.join(absolute_path, 'static/img/random_register/')
        bg_imgs_count = len([name for name in os.listdir(bg_imgs_folder) if os.path.isfile(bg_imgs_folder + name)])

        data_to_render = {'form': form, 'terms_of_service' :  REGISTER_TERMS_OF_SERVICE,
                          'usuario_bulletins' : REGISTER_USER_BULLETINS}
        data_to_render.update(csrf(request))
        render_form = render_to_response('register_form.html', data_to_render)
        return render_to_response('main_template.html', {'register_form':render_form.content, 
                                                         'random_bg' : random.randint(1, bg_imgs_count)})
    
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
        content = (settings.WEB_URL +"/usuarios/confirm/?=" + str(session_s.session_key) + "&email=" + session_s['user_mail'])
        print content
        send_mail(title, content, 'no-reply@trueque.in', [session_s['user_mail']], fail_silently=False)
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
                
                return HttpResponseRedirect("/usuarios/profile")
        else:
            form = LoginForm()
        
        request.session.set_test_cookie()
        c = { 'form': form }
        c.update(csrf(request))
        return render_to_response('user_login.html', c)
    
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
                if form.cleaned_data["usuario_new_password_1"]:
                    edit_register.usuario_password = form.cleaned_data["usuario_new_password_1"]
                edit_register.save()
        else:
            form = EditUserForm(instance=user)
            
        request.session.set_test_cookie()
        c = { 'form': form }
        c.update(csrf(request))
        return render_to_response('edit_user_profile.html', c)
    
    #Exceptions que se activan en caso de no poder iniciar sesion.
    except KeyError: return C_error.raise_error(C_error.NEEDLOGIN)
    except SuspiciousOperation: return C_error.raise_error(C_error.PERMISSIONDENIED)
    except ObjectDoesNotExist as e: return C_error.raise_error(C_error.UNREGISTEREDUSER)
    except DatabaseError: return C_error.raise_error(C_error.DATABASEERROR)
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        return C_error.raise_error(C_error.MAGICERROR)

class ShowProfile():
    def get_user_data(self, user):
        return [['NOMBRE', user.usuario_name], ['APELLIDO', user.usuario_lastname],
                ['RATING', user.usuario_rating], ['LEVEL', user.usuario_level],
                ['QUDS', user.usuario_quds], ['TRUEQUES', user.usuario_barter_qty],
                ['SIGUIENDO', user.usuario_followed_qty], ['ME SIGUEN', user.usuario_follower_qty]]
    
    def show_profile_default(self, request):
        try:
            user = Usuario.objects.get(id_usuario= request.session['member_id'])
            albums_list = albums_utils.get_albums(user)
            
            random_ints = []
            for num in range(0,11):
                random_ints.append(random.randint(-3,3))
                
            album_list =  {'object_list' : albums_list, 'random_ints': random_ints, 'user':user}
            
            if is_loged_edit(request,user): album_list.update({'is_loged_edit':True})
                
            render_albums = render_to_response('user_albums.html', album_list, context_instance = RequestContext(request))
            
            if request.is_ajax():
                message = {"albums_data": render_albums.content}
            else:
                vars_view = {'albums' : render_albums.content}
                return self.show_profile_user(request, user, vars_view)
            
            json = simplejson.dumps(message)
            return HttpResponse(json, mimetype='application/json')
        except Exception as e: return self.show_error(e)

    def show_profile_using_id(self, request, user_id):
        try:
            user = Usuario.objects.get(id_usuario = user_id)
            albums_list = albums_utils.get_albums(user)
            
            random_ints = []
            for num in range(0,11):
                random_ints.append(random.randint(-3,3))
                
            album_list =  {'object_list' : albums_list, 'random_ints': random_ints, 'user':user}
            
            if is_loged_edit(request,user): album_list.update({'is_loged_edit':True})
                
            render_albums = render_to_response('user_albums.html', album_list, context_instance = RequestContext(request))
            
            if request.is_ajax():
                    message = {"albums_data": render_albums.content}
            else:
                    vars_view = {'albums' : render_albums.content}
                    if is_loged_edit(request,user):
                        return self.show_profile_user(request, user, vars_view)
                    else:
                        return self.show_another_profile(request, user, vars_view)
            
            json = simplejson.dumps(message)
            return HttpResponse(json, mimetype='application/json')
        
        except Exception as e: return self.show_error(e)
        
    def show_profile_using_mail(self, request, user_email):
        try: 
            user = Usuario.objects.get(usuario_email_1 = forms.EmailField().clean(user_email))
            albums_list = albums_utils.get_albums(user)
            
            random_ints = []
            for num in range(0,11):
                random_ints.append(random.randint(-3,3))
            
            album_list =  {'object_list' : albums_list, 'random_ints': random_ints, 'user':user}
            
            if is_loged_edit(request,user): album_list.update({'is_loged_edit':True})
                
            render_albums = render_to_response('user_albums.html', album_list, context_instance = RequestContext(request))
            
            if request.is_ajax():
                    message = {"albums_data": render_albums.content}
            else:
                    vars_view = {'albums' : render_albums.content}
                    if is_loged_edit(request,user):
                        return self.show_profile_user(request, user, vars_view)
                    else:
                        return self.show_another_profile(request, user, vars_view)
            
            json = simplejson.dumps(message)
            return HttpResponse(json, mimetype='application/json')
        except Exception as e: return self.show_error(e)
            
    def show_add_album_red(self, request): return HttpResponseRedirect("/usuarios/profile/addalbum")
    
    def show_add_album(self, request):
        try:
            user = Usuario.objects.get(id_usuario= request.session['member_id'])
            
            if request.is_ajax():
                if request.method == 'POST':
                    form = AddAlbumForm(request.POST)
                    form.id_owner = user
                    if form.is_valid():
                        message = {"album_form_result": True, "add_album_message": "Album añadido correctamente"}
                    else:
                        c = { 'form': form }
                        c.update(csrf(request))
                        message = {"album_form_result": False, "add_album_render":render_to_response('album_add.html', c).content}
                    
                    json = simplejson.dumps(message)
                    return HttpResponse(json, mimetype='application/json')

            form = AddAlbumForm()
                    
            c = { 'form': form }
            c.update(csrf(request))
            return render_to_response('album_add.html', c)
        except Exception as e: return self.show_error(e)
    
    def add_follow(self, request, user_id):
        try:
            followed = Usuario.objects.get(id_usuario = user_id)
            if not is_loged_edit(request, followed):
                follower = Usuario.objects.get(id_usuario= request.session['member_id'])
                new_follower = Followers()
                new_follower.id_follower = follower
                new_follower.id_followed = followed
                new_follower.save(force_insert = True)
                follower.usuario_followed_qty = follower.usuario_followed_qty + 1
                followed.usuario_follower_qty = followed.usuario_follower_qty + 1
                follower.save()
                followed.save()
                return HttpResponseRedirect("/usuarios/profile/%s" % followed.id_usuario)
            else:
                raise SuspiciousOperation
        except Exception as e: return self.show_error(e)
        
    def cancel_follow(self, request, user_id):
        try:
            followed = Usuario.objects.get(id_usuario = user_id)
            if not is_loged_edit(request, followed):
                follower = Usuario.objects.get(id_usuario= request.session['member_id'])
                following = Followers.objects.filter(id_followed = followed, id_follower = follower)
                following.delete()
                follower.usuario_followed_qty = follower.usuario_followed_qty - 1
                followed.usuario_follower_qty = followed.usuario_follower_qty - 1
                follower.save()
                followed.save()
                return HttpResponseRedirect("/usuarios/profile/%s" % followed.id_usuario)
            else:
                raise SuspiciousOperation
        except Exception as e: return self.show_error(e)
    
    def show_followers(self, request):
        try:
            user = Usuario.objects.get(id_usuario= request.session['member_id'])
            followers = Followers.objects.filter(id_followed = user)
            vars_view = {'following' : None, 'followers' : followers}   
            return self.show_profile_user(request, user, vars_view)
        except Exception as e: return self.show_error(e)
        
    def show_following(self, request):
        try:
            user = Usuario.objects.get(id_usuario= request.session['member_id'])
            following = Followers.objects.filter(id_follower = user)
            vars_view = {'following' : following, 'followers' : None}
            return self.show_profile_user(request, user, vars_view)
        except Exception as e: return self.show_error(e)
    
    def show_mail(self, request):
        try:
            if request.is_ajax():
                user = Usuario.objects.get(id_usuario= request.session['member_id'])
                mail_list = Message.objects.filter(id_receiver = user)
                render = render_to_response('user_mail_inbox.html', 
                                            {'object_list' : mail_list},
                                            context_instance = RequestContext(request))
                message = {"mail_inbox": render.content}
            else:
                user = Usuario.objects.get(id_usuario= request.session['member_id'])
                vars_view = {'mail' : True}
                return self.show_profile_user(request, user, vars_view)

            json = simplejson.dumps(message)
            return HttpResponse(json, mimetype='application/json')
        
        except Exception as e: return self.show_error(e)
    
    def show_mail_compose(self, request):
        try:
            if request.is_ajax():
                mail_sent_complete = False
                if request.method == 'POST':
                    form = ComposeMailForm(request.POST)
                    if form.is_valid():
                        new_mail = form.save(commit=False)
                        user = Usuario.objects.get(id_usuario= 1)
                        new_mail.id_sender = user
                        user2 = Usuario.objects.get(id_usuario= 2)
                        new_mail.id_receiver = user2
                        new_mail.message_datetime = datetime.now()
                        new_mail.id_conversation = 1
                        new_mail.message_read = 0
                        new_mail.save()
                        form = ComposeMailForm()
                        mail_sent_complete = MAILSENTCOMPLETE
                        
                else: form = ComposeMailForm()
                c = { 'form': form , 'mail_sent_complete' : mail_sent_complete}
                c.update(csrf(request))
                render = render_to_response('user_send_mail.html', c)
                message = {"mail_inbox": render.content}
            else: return HttpResponseRedirect("/usuarios/profile/mail")
            
            json = simplejson.dumps(message)
            return HttpResponse(json, mimetype='application/json')
        except Exception as e: return self.show_error(e)
    
    def show_mail_sent(self, request):
        try:
            if request.is_ajax():
                
                user = Usuario.objects.get(id_usuario= request.session['member_id'])
                mail_list = Message.objects.filter(id_sender = user)
                render = render_to_response('user_mail_inbox.html', 
                                            {'object_list' : mail_list},
                                            context_instance = RequestContext(request))
                message = {"mail_inbox": render.content}
            else: 
                return HttpResponseRedirect("/usuarios/profile/mail")
            
            json = simplejson.dumps(message)
            return HttpResponse(json, mimetype='application/json')
        
        except Exception as e: return self.show_error(e)

        
    def show_profile_user(self, request, user, vars_view):
        try:
            user_data = self.get_user_data(user)
            vars_view.update({'user_data' : user_data, 'islogededit' : is_loged_edit(request, user), 'user':user})
            vars_view.update(csrf(request))
            return render_to_response('user_profile.html', vars_view)
        except Exception as e: return self.show_error(e)
        
        
    def show_another_profile(self, request, user, vars_view):
        try:
            cancel_follow = False
            active_user = None 
            if is_loged(request):
                if user.id_usuario != request.session['member_id']:
                    following = None
                    active_user = Usuario.objects.get(id_usuario=request.session['member_id'])
    	            try:
    	                following = Followers.objects.filter(id_followed = user, id_follower = Usuario.objects.get(id_usuario= request.session['member_id']))
    	            except: 
    	                pass
    	            if following: cancel_follow = True
    	            follow = user.id_usuario
    	        else:
    	            active_user = user
            else: 
            	follow = False
            user_data = self.get_user_data(user)
            vars_view.update({'user_data' : user_data, 'islogededit' : is_loged_edit(request, user),
                              'follow' :  follow, 'cancelfollow' : cancel_follow, 'user':active_user})
            vars_view.update(csrf(request))
            return render_to_response('guest_user_profile.html', vars_view)
        except Exception as e: return self.show_error(e)
        
    def show_error(self, e): 
        try: raise e
        except SuspiciousOperation: return C_error.raise_error(C_error.PERMISSIONDENIED)
        except KeyError as e: return C_error.raise_error(C_error.NEEDLOGIN)
        except ValidationError: return C_error.raise_error(C_error.UNREGISTEREDUSER)
        except ObjectDoesNotExist as e: return C_error.raise_error(C_error.UNREGISTEREDUSER)
        except DatabaseError: return C_error.raise_error(C_error.DATABASEERROR)
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            return C_error.raise_error(C_error.MAGICERROR)

def is_loged(request):
    try:
        if request.session['member_id']: return True
    except: return False

def is_loged_edit(request, user):
    try: 
        if request.session['member_id'] == user.id_usuario: return True
    except: return False 
