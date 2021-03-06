# -*- coding: utf-8 -*-
from PIL import Image
from albums.form import AddAlbumForm
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
from main.models import Level
from messages.form import ComposeMailForm
from messages.models import Message
from usuarios.form import RegisterUserForm, SendConfirmationForm, LoginForm, \
    EditUserForm1, UserProfileForm, EditUserForm2
from usuarios.models import Followers, UserProfile
import albums.utils as albums_utils
import json
import os
import random
import socket
import usuarios.custom_error as C_error
import usuarios.form


SESSION_EXPIRY = 86400 #Tiempo de expiracion de la sesion encargada de la verificacion.

#Nombres de los albumes
ALBUM_NAME_GARAGE = "My Garage"
ALBUM_NAME_TRUEQUES = "Trueques"
ALBUM_NAME_LIKE = "Me gusta"
ALBUM_NAME_RECOMMEND = "Recomiendo"
ALBUM_NAME_PENDIENTES = "Pendientes"
ALBUMES = [ALBUM_NAME_GARAGE, ALBUM_NAME_TRUEQUES, ALBUM_NAME_LIKE, ALBUM_NAME_RECOMMEND, ALBUM_NAME_PENDIENTES]
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
            userForm = RegisterUserForm(request.POST, prefix="user")
            profileForm = UserProfileForm(request.POST, prefix="profile")
            if userForm.is_valid() and profileForm.is_valid():
                new_register = userForm.save(commit=False)
                #Se crea una session para la verificacion via email de la activacion de cuenta
                #del usuario que se esta intentando registrar.
                session_s = SessionStore()
                session_s['user_mail'] = new_register.email
                session_s['user_name'] = new_register.first_name
                session_s.set_expiry(SESSION_EXPIRY)
                session_s.save(must_create=True)
                new_register.username = new_register.email
                new_register.is_active=False
                new_register.save()
                profile = new_register.profile
                profile.bulletins = profileForm.cleaned_data['bulletins']
                profile.save()
                
                #Se crean los primeros cuatro albums por defecto
                for name in ALBUMES:
                    user = User.objects.get(email=new_register.email)
                    albums_utils.add_album(user, name, False, True)
                
                return send_registration_confirmation(session_s)
        else:
            userForm = RegisterUserForm(prefix="user")
            profileForm = UserProfileForm(prefix="profile")
        absolute_path = os.path.dirname(os.path.realpath(__file__))
        bg_imgs_folder = os.path.join(absolute_path, 'static/img/random_register/')
        bg_imgs_count = len([name for name in os.listdir(bg_imgs_folder) if os.path.isfile(bg_imgs_folder + name)])

        data_to_render = {'form': userForm, 'profile_form':profileForm, 'terms_of_service' :  REGISTER_TERMS_OF_SERVICE,
                          'bulletins' : REGISTER_USER_BULLETINS,
                          'random_bg' : random.randint(1, bg_imgs_count)}
        data_to_render.update(csrf(request))
        
        return render_to_response('register_form.html', data_to_render)
    
    #Exceptions que se activan en caso de no poder registrar al usuario en la base de datos o
    #por alguna accion extraña durante el registro.
    except SuspiciousOperation: 
        return C_error.raise_error(C_error.PERMISSIONDENIED)
    except DatabaseError as e:
        print '%s (%s)' % (e.message, type(e)) 
        return C_error.raise_error(C_error.DATABASEERROR)
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
        send_mail(title, content, settings.EMAIL_HOST_USER, [session_s['user_mail']], fail_silently=False)
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
            user = User.objects.get(email=session_s['user_mail'])
        else: return C_error.raise_error(C_error.EXPIREDKEY)

        #Verificar que el usuario no este activo para activarlo. Una vez activado se borra
        #la sesion.
        if(user.is_active == False):
            user.is_active = True
            user.save()
            session_s.delete()
            form = LoginForm()
            c = { 'form': form, 'success':True}
            return render_to_response('user_login.html', c,context_instance = RequestContext(request) )
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
                session_s['user_mail'] = form.cleaned_data['email']
                session_s.set_expiry(SESSION_EXPIRY)
                session_s.save(must_create=True)
                
                user = User.objects.get(email=session_s['user_mail'])
                if(user.is_active == False):
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
def mLogin(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            
            if request.session.test_cookie_worked(): 
                request.session.delete_test_cookie()
            else: 
                return C_error.raise_error(C_error.NOCOOKIE)
            if form.is_valid():
                mUser = User.objects.get(email=form.cleaned_data['email'])   
                user = authenticate(username=mUser.username, password=form.cleaned_data['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect("/usuarios/profile")
                    else:
                        return HttpResponse("Usuario no activo")
                else:
                    return HttpResponse("Usuario no existe")        
        else:
            form = LoginForm()
        
        request.session.set_test_cookie()
        c = { 'form': form }
        c.update(csrf(request))
        return render_to_response('user_login.html', c)
    
    #Exceptions que se activan en caso de no poder iniciar sesion.
    except DatabaseError: 
        return C_error.raise_error(C_error.DATABASEERROR)
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        return C_error.raise_error(C_error.MAGICERROR)
    except SuspiciousOperation as e:
        print '%s (%s)' % (e.message, type(e)) 
        return C_error.raise_error(C_error.PERMISSIONDENIED)
        
    #Exceptions que se activan en caso de no poder iniciar sesion.
    except SuspiciousOperation: 
        return C_error.raise_error(C_error.PERMISSIONDENIED)
    except DatabaseError: 
        return C_error.raise_error(C_error.DATABASEERROR)
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        return C_error.raise_error(C_error.MAGICERROR)

#edit_user_profile: Funcion encargada de modificar los datos de un usuario
#PARAMS: request:  Objeto que contiene toda la informacion enviada por el navegador del usuario.
#RETURN:  Se devuelven distintos render_to_response dependiendo de como la modificacion de informacion.
def edit_user_profile(request):
    try:
        user = request.user
        if request.method == 'POST' :
            form = EditUserForm1(request.POST, instance = user, prefix="form1")
            form2 = EditUserForm2(request.POST, request.FILES , instance = user.profile, prefix="form2")
            
            authenticate(username = request.user.username, password = forms.CharField().clean(form.data['form1-password']))
            
            #Se verifica que la contraseña ingresada sea la que corresponde.
            if form.data['form1-password'] and forms.CharField().clean(form.data['form1-password']) and not authenticate(username = request.user.username, password = forms.CharField().clean(form.data['form1-password'])):
                form.errors['form1-password'] = form.error_class([usuarios.form.ERROR_WRONGPASS])

            if form.is_valid() and form2.is_valid():
                edit_register = form.save(commit=False)
                edit_register.set_password(form.cleaned_data["password"])
                if form.cleaned_data["new_password_1"]:
                    edit_register.set_password(form.cleaned_data["new_password_1"])
                edit_register.save()
                
                edit_register2 = form2.save(commit=False)
                edit_register2.img = 'profile/' + str(request.user.id)
                edit_register2.save()
                
                saveImages(request, edit_register2.img)
        else:
            form = EditUserForm1(instance=user, prefix="form1")
            form2 = EditUserForm2(instance=user.profile, prefix="form2")
         
        c = { 'form': form, 'form2': form2}
        c.update(csrf(request))
        return render_to_response('edit_user_profile.html', c, context_instance=RequestContext(request))
    
    #Exceptions que se activan en caso de no poder iniciar sesion.
    except KeyError as e: 
        print '%s (%s)' % (e.message, type(e))
        return C_error.raise_error(C_error.NEEDLOGIN)
    except SuspiciousOperation: return C_error.raise_error(C_error.PERMISSIONDENIED)
    except ObjectDoesNotExist as e: return C_error.raise_error(C_error.UNREGISTEREDUSER)
    except DatabaseError: return C_error.raise_error(C_error.DATABASEERROR)
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))
        return C_error.raise_error(C_error.MAGICERROR)

#saveImages: Busca la imagenes del request enviadas por POST y las envia a guardar.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#                  Incluye datos del usuario.
#         path: Dirección del servidor donde se guardaran los archivos. Se genera mediante HASH.
#RETURN: 
def saveImages(request, path=None):
    try:
        handle(path, request.FILES['form2-img_1'])
    except Exception as e:
        print e


#handle: Guarda el archivo en la carpeta 'cargas' (MEDIA_ROOT), dentro de la carpeta en 'path'
#PARAMS: path: Dirección del servidor donde se guardaran los archivos. Se genera mediante HASH.
#         file: Archivo que se va a guardar
#         counter: Integer que muestra cual es el orden en que se esta guardando este archivo. Se 
#                    usa para darle nombre a la imagen.
#RETURN: 
def handle(path, fileN):
    if os.path.isdir(os.path.join(settings.MEDIA_ROOT, path)) == False:
        os.makedirs(os.path.join(settings.MEDIA_ROOT, path))
    if fileN:
        filename = settings.MEDIA_ROOT + "/" +path + "/" + "img_1.png"
        destination = open(filename, 'wb+')
        for chunk in fileN.chunks():
            destination.write(chunk)
        destination.close()
        resize(filename)


def resize(filename):
    img = Image.open(filename)
    width, height = img.size
    if width>=height:
        nWidth = 60
        nHeight = 60*height/width
        mWidth = 128
        mHeight = 128*height/width
        bWidth = 210
        bHeight = 210*height/width
    else:
        nHeight = 60
        nWidth = 60*width/height
        mHeight = 128
        mWidth = 128*width/height
        bHeight = 210
        bWidth = 210*width/height
    thumb1 = img.resize((nWidth, nHeight), Image.ANTIALIAS)
    thumb2 = img.resize((mWidth, mHeight), Image.ANTIALIAS)
    thumb3 = img.resize((bWidth, bHeight), Image.ANTIALIAS)
    thumb1.save(filename.replace(".png", "_small.png"))
    thumb2.save(filename.replace(".png", "_medium.png"))
    thumb3.save(filename.replace(".png", "_big.png"))
    os.remove(filename)


class ShowProfile():
    def get_user_data(self, user):
        return [['NOMBRE', user.first_name], ['APELLIDO', user.last_name],
                ['RATING', user.profile.rating], ['LEVEL', user.profile.level],
                ['QUDS', user.profile.quds], ['TRUEQUES', user.profile.barter_qty],
                ['SIGUIENDO', user.profile.followed_qty], ['ME SIGUEN', user.profile.follower_qty]]
    
    def search(self, request):
        if request.is_ajax():
            q = request.GET.get('term', '')
            users = User.objects.filter(first_name__icontains = q)[:20]
            results = []
            for user in users:
                drug_json = {}
                drug_json['id'] = user.id
                drug_json['label'] = user.first_name + " " + user.last_name
                drug_json['value'] = user.first_name + " " + user.last_name
                results.append(drug_json)
            data = json.dumps(results)
        else:
            data = 'fail'
        mimetype = 'application/json'

        return HttpResponse(data, mimetype)
    
    def show_profile_default(self, request):
        try:
            user = request.user
            albums_list = albums_utils.get_albums(user)
            album_list =  {'object_list' : albums_list, 'user':user}
            if is_loged_edit(request,user): 
                album_list.update({'is_loged_edit':True})
                
            render_albums = render_to_response('user_albums.html', album_list, context_instance = RequestContext(request))
            
            if request.is_ajax():
                message = {"albums_data": render_albums.content}
            else:
                vars_view = {'albums' : render_albums.content}
                return self.show_profile_user(request, user, vars_view)
            
            json = simplejson.dumps(message)
            return HttpResponse(json, mimetype='application/json')
        except Exception as e: 
            return self.show_error(e)

    def show_profile_using_id(self, request, user_id):
        try:
            user = User.objects.get(id = user_id)
            albums_list = albums_utils.get_albums(user)
            
            album_list =  {'object_list' : albums_list, 'user':user}
            
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
            user = User.objects.get(email = forms.EmailField().clean(user_email))
            albums_list = albums_utils.get_albums(user)
            
            album_list =  {'object_list' : albums_list, 'user':user}
            
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
            user = request.user
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
    
    def show_album(self, request):
        try:
            if request.is_ajax():
                products = albums_utils.get_products_by_id_album(request.GET['albumID'])
                products_list =  {'album_id':request.GET['albumID'], 'object_list' : products}
                render_content = render_to_response('user_album_content.html', products_list, context_instance = RequestContext(request))
                message = {"album_content_data": render_content.content}
                json = simplejson.dumps(message)
                return HttpResponse(json, mimetype='application/json')
            
        except Exception as e: return self.show_error(e)
        
    def add_follow(self, request, user_id):
        try:
            followed = User.objects.get(id = user_id)
            if not is_loged_edit(request, followed):
                follower = request.user
                new_follower = Followers()
                new_follower.id_follower = follower
                new_follower.id_followed = followed
                new_follower.save(force_insert = True)
                follower.profile.followed_qty = follower.profile.followed_qty + 1
                followed.profile.follower_qty = followed.profile.follower_qty + 1
                follower.save()
                followed.save()
                return HttpResponseRedirect("/usuarios/profile/%s" % followed.id)
            else:
                raise SuspiciousOperation
        except Exception as e: return self.show_error(e)
        
    def cancel_follow(self, request, user_id):
        try:
            followed = User.objects.get(id = user_id)
            if not is_loged_edit(request, followed):
                follower = request.user
                following = Followers.objects.filter(id_followed = followed, id_follower = follower)
                following.delete()
                follower.profile.followed_qty = follower.profile.followed_qty - 1
                followed.profile.follower_qty = followed.profile.follower_qty - 1
                follower.save()
                followed.save()
                return HttpResponseRedirect("/usuarios/profile/%s" % followed.id)
            else:
                raise SuspiciousOperation
        except Exception as e: return self.show_error(e)
    
    def show_followers(self, request):
        try:
            user = request.user
            followers = Followers.objects.filter(id_followed = user)
            vars_view = {'following' : None, 'followers' : followers}   
            return self.show_profile_user(request, user, vars_view)
        except Exception as e: return self.show_error(e)
        
    def show_following(self, request):
        try:
            user = request.user
            following = Followers.objects.filter(id_follower = user)
            vars_view = {'following' : following, 'followers' : None}
            return self.show_profile_user(request, user, vars_view)
        except Exception as e: return self.show_error(e)
    
    def show_mail(self, request):
        try:
            if request.is_ajax():
                user = request.user
                mail_list = Message.objects.filter(id_receiver = user)
                return render_to_response('user_mail_inbox.html', 
                                            {'object_list' : mail_list,'sender':True},
                                            context_instance = RequestContext(request))
            else:
                user = request.user
                vars_view = {'mail' : True}
                return self.show_profile_user(request, user, vars_view)
        except Exception as e: return self.show_error(e)
    
    def show_mail_compose(self, request):
        try:
            if request.is_ajax():
                mail_sent_complete = False
                if request.method == 'POST':
                    form = ComposeMailForm(request.POST)
                    if form.is_valid():
                        new_mail = Message()
                        user = request.user
                        new_mail.id_sender = user
                        user2 = User.objects.get(id= form.cleaned_data['user_id'])
                        new_mail.id_receiver = user2
                        new_mail.datetime = datetime.now()
                        new_mail.id_conversation = 1
                        new_mail.text = form.cleaned_data['text']
                        new_mail.subject = form.cleaned_data['subject']
                        new_mail.save()
                        form = ComposeMailForm()
                        mail_sent_complete = MAILSENTCOMPLETE
                else: 
                    form = ComposeMailForm()
                week = {0:'Lunes',1:'Martes',2:'Miércoles',3:'Jueves',4:'Viernes',5:'Sábado',6:'Domingo'}
                month = {0: 'Enero', 1:'Febrero',2:'Marzo',3:'Abril',4:'Mayo',5:'Junio',6:'Julio',7:'Agosto',8:'Septiembre',9:'Octubre',10:'Noviembre',11:'Diciembre'}
                date_time = week[datetime.today().weekday()] + " " + str(datetime.today().day) + "/" + month[datetime.today().month - 1] + " " + str(datetime.today().year)
                c = { 'form': form , 'date_t':date_time, 'mail_sent_complete' : mail_sent_complete}
                c.update(csrf(request))
                return render_to_response('user_send_mail.html', c)
            else: return HttpResponseRedirect("/usuarios/profile/mail")
            
        except Exception as e: return self.show_error(e)
    
    def show_mail_sent(self, request):
        try:
            if request.is_ajax():
                user = request.user
                mail_list = Message.objects.filter(id_sender = user)
                return render_to_response('user_mail_inbox.html', 
                                            {'object_list' : mail_list},
                                            context_instance = RequestContext(request))
            else: 
                return HttpResponseRedirect("/usuarios/profile/mail")
        
        except Exception as e: return self.show_error(e)

        
    def show_profile_user(self, request, user, vars_view):
        try:
            level = Level().get(user.profile.quds)
            vars_view.update({'islogededit' : is_loged_edit(request, user), 'user':user, 'level':level.name})
            vars_view.update(csrf(request))
            return render_to_response('user_profile.html', vars_view)
        except Exception as e: return self.show_error(e)
        
        
    def show_another_profile(self, request, user, vars_view):
        try:
            cancel_follow = False
            active_user = None 
            if request.user.is_authenticated():
                if user != request.user:
                    following = None
                    active_user = request.user
                    try:
                        following = Followers.objects.filter(id_followed = user, id_follower = request.user)
                    except: 
                        pass
                    if following: 
                        cancel_follow = True
                    follow = user.id
                else:
                    follow = True
                    active_user = user
            else: 
                follow = False
            level = Level().get(user.profile.quds)
            vars_view.update({'view_user' : user, 'islogededit' : is_loged_edit(request, user), 'level':level.name,
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

def is_loged_edit(request, user):
    try: 
        if request.user == user: 
            return True
    except: 
        return False

def mLogout(request):
    logout(request)
    return HttpResponseRedirect("/")
