# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

#LLAVES DISPONIBLES PARA LEVANTAR UN ERROR
MAGICERROR = 0
PERMISSIONDENIED = 1
EXPIREDKEY = 2
INVALIDKEY = 3
UNREGISTEREDUSER = 4
INVALIDEXPIREDKEY = 5
USERALREADYACTIVE = 6
EMAILSERVERDOWN = 7
USERREGISTEREDWITHMAGICERROR = 8
REGISTERMODULEERROR = 9
DATABASEERROR = 10
NOCOOKIE = 11
NEEDLOGIN = 12

#raise_error: Funcion encargada de levantar errores.
#PARAMS: error_key: LLave a utilizar para levantar un error.
#RETURN: Se devuelve render_to_response con el error a desplegar.
def raise_error(error_key):
    def magic_error(): return 'ERROR INESPERADO'
    def permission_denied(): return 'PERMISO DENEGADO'
    def expired_key(): return 'SU LLAVE DE CONFIRMACION A EXPIRADO'
    def invalid_key(): return 'LA LLAVE ES INVALIDA'
    def unregistered_user(): return 'USUARIO NO REGISTRADO'
    def invalid_expired_key(): return 'SU LLAVE DE CONFIRMACION A EXPIRADO O NO ES VALIDA'
    def user_already_active(): return 'USUARIO YA ACTIVO'
    def email_server_down(): return 'EL SERVIDOR DE EMAIL NO ESTA DISPONIBLE, INTENTE VALIDAR SU CUENTA EN OTRO MOMENTO SI ES QUE NO RECIBE CONFIRMACION DENTRO DE LAS PROXIMAS HORAS...'
    def user_registered_with_magic_error(): return 'SU USUARIO A SIDO REGISTRADO PERO A OCURRIDO UN ERROR AL ENVIAR EL CORREO DE CONFIRMACION ...'
    def register_module_error(): return 'EL SERVICIO DE REGISTRO NO SE ENCUENTRA DISPONIBLE, INTENTE EN OTRO MOMENTO'
    def data_base_error(): return 'A OCURRIDO UN ERROR AL INTENTAR CONTACTAR A LA BASE DE DATOS, SI EL PROBLEMA PERSISTE CONTACTENOS A ...'
    def no_cookie(): return 'Su navegador necesita tener habilitadas para poder iniciar sesion'
    def need_login(): return 'DEBE INICIAR SESION PARA ENTRAR EN ESTA SECCION'
    raise_e = {MAGICERROR : magic_error(),
               PERMISSIONDENIED : permission_denied(),
               EXPIREDKEY : expired_key(),
               INVALIDKEY : invalid_key(),
               UNREGISTEREDUSER : unregistered_user(),
               INVALIDEXPIREDKEY : invalid_expired_key(),
               USERALREADYACTIVE : user_already_active(),
               EMAILSERVERDOWN : email_server_down(),
               USERREGISTEREDWITHMAGICERROR : user_registered_with_magic_error(),
               REGISTERMODULEERROR : register_module_error(),
               DATABASEERROR : data_base_error(),
               NOCOOKIE : no_cookie(),
               NEEDLOGIN : need_login()
               }
    
    return render_to_response('register_error.html', {'error': raise_e[error_key]})

#raise_message_error: Funcion que puede desplegar una pantalla de error con el mensaje que se
#                     le entregue como parametro.
#PARAMS: message: Mensaje que se quiere desplegar
#RETURN: Se devuelve render_to_response con el error a desplegar.
def raise_message_error(message):
    return render_to_response('register_error.html', {'error':message})