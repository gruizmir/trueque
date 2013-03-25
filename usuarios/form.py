# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.forms.forms import Form
from usuarios.models import Usuario

ERROR_PASSDONTMATCH = u"Passwords don't match"
ERROR_WRONGPASS = u"Wrong password, try again"
ERROR_USERDONTEXIST = u"User doesn't exist"
ERROR_USERNOTCONFIRMED = u"Unconfirmed user"

#RegisterUserForm: Formulario con todos los campos basicos necesarios para el registro.
#PARAMS: ModelForm: Class ModelForm
#RETURN: Se devuelve cleaned_data con el caso de que los passwords no coincidan durante el registro.
class RegisterUserForm(ModelForm):
    usuario_password = forms.CharField(widget=forms.PasswordInput(), max_length=75, min_length=6)
    usuario_password_2 = forms.CharField(widget=forms.PasswordInput(), max_length=75, min_length=6)
    class Meta:
        model = Usuario
        fields = ('usuario_name', 'usuario_lastname', 'usuario_email_1',
                  'usuario_password', 'usuario_password_2', 'usuario_bulletins',
                  'usuario_art', 'usuario_music',
                  'usuario_tech', 'usuario_cars', 'usuario_travels',
                  'usuario_clothes', 'usuario_cine', 'usuario_sports', 
                  'usuario_eco', 'usuario_culture', 'usuario_spectacles',
                  'usuario_love', 'usuario_food', 'usuario_vacations',
                  'usuario_services')
    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        password1 = cleaned_data.get("usuario_password")
        password2 = cleaned_data.get("usuario_password_2")
        #Se verifica que los passwords esten ingresados y que no sean iguales para
        #notificar al usuario que los corrija.
        if password1 and password2 and password1 != password2:
            self._errors["usuario_password"] = self.error_class([ERROR_PASSDONTMATCH])
            del cleaned_data["usuario_password"]
            del cleaned_data["usuario_password_2"]
        
        return cleaned_data

#SendConfirmationForm: Formulario con un campo mail utilizado para reenviar la confirmacion
#                      de activacion de cuenta al usuario.
class SendConfirmationForm(Form):
    usuario_email_1 = forms.EmailField(max_length=90)

#loginform: Formulario con los campos de email y password para iniciar sesion de un usuario,
#           adicionalmente contiene logica para verificar que el usuario se encuentra
#           registrado y que la contraseña es correcta.
#PARAMS: Form: Class Form
#RETURN: Se devuelve cleaned_data con el caso de usuario y contraseña incorrectos.
class LoginForm(Form):
    usuario_email_1 = forms.EmailField(max_length=90)
    usuario_password = forms.CharField(widget=forms.PasswordInput(), max_length=75, min_length=6)
    
    def clean(self): 
        cleaned_data = super(LoginForm, self).clean()
        mail = cleaned_data.get('usuario_email_1')
        password = cleaned_data.get("usuario_password")
        
        #Funcion que recibe el campo donde se debe desplegar el error y el error a desplegar.
        def clean_and_return(field, error):
            self._errors[field] = self.error_class([error])
            del cleaned_data["usuario_email_1"]
            del cleaned_data["usuario_password"]
            return cleaned_data
        
        try:
            #Se verifca que esten ingresados el mail y password, si es asi, se intenta
            #recuperar al usuario de la base de datos.
            if mail and password: user = Usuario.objects.get(usuario_email_1=mail)
            else: return cleaned_data
            
            #Se verifica que el usuario este activo antes de iniciar sesion.
            if user.usuario_active == False: clean_and_return("usuario_email_1", ERROR_USERNOTCONFIRMED)
            
            #En caso de no coincidir el password entregado con el guardado en la base de datos
            #se procede a informar al usuario
            if(password != user.usuario_password): clean_and_return("usuario_password", ERROR_WRONGPASS) 
            
            return cleaned_data
        #En caso de no exisitr el usuario se informa que no se encuentra registrado.
        except ObjectDoesNotExist: clean_and_return("usuario_email_1", ERROR_USERDONTEXIST)
        except Exception: return cleaned_data

#EditUserForm: Formulario que permite a un usuario modificar sus datos.
#PARAMS: ModelForm: Class ModelForm
class EditUserForm(ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(), max_length=75, min_length=6, required=False)
    usuario_password = forms.CharField(widget=forms.PasswordInput(), max_length=75, min_length=6)
    class Meta:
        model = Usuario
        fields = ('usuario_email_1','usuario_email_2',
                  'usuario_phone_1', 'usuario_phone_2',
                  'usuario_city','usuario_lang',
                  'usuario_bulletins',      
                  'usuario_art', 'usuario_music',
                  'usuario_tech', 'usuario_cars', 'usuario_travels',
                  'usuario_clothes', 'usuario_cine', 'usuario_sports', 
                  'usuario_eco', 'usuario_culture', 'usuario_spectacles',
                  'usuario_love', 'usuario_food', 'usuario_vacations',
                  'usuario_services', 'new_password', 'usuario_password')
