# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.forms.forms import Form
from usuarios.models import Usuario
from django.utils.translation import ugettext as _

ERROR_PASSDONTMATCH = u"Passwords don't match"
ERROR_WRONGPASS = u"Wrong password, try again"
ERROR_USERDONTEXIST = u"User doesn't exist"
ERROR_USERNOTCONFIRMED = u"Unconfirmed user"

# Translators: Name used on hints
HINT_NAME = _('Name')
# Translators: Last Name used on hints
HINT_LASTNAME = _('Last Name')
# Translators: Email used on hints
HINT_EMAIL = _('mail@trueque.com')
# Translators: Email 1 used on hints
HINT_EMAIL_1 = _('Email 1')
# Translators: Email 2 used on hints
HINT_EMAIL_2 = _('Email 2')
# Translators: Password used on hints
HINT_PASSWORD1 = _('Password')
# Translators: Verify Password used on hints
HINT_PASSWORD2 = _('Verify Password')
# Translators: New Password used on hints
HINT_NEW_PASSWORD_1 =('New Password')
# Translators: Verify New Password used on hints
HINT_NEW_PASSWORD_2 =('Verify New Password')
# Translators: Phone 1 used on hints
HINT_PHONE_1 = _('Phone 1')
# Translators: Phone 2 used on hints
HINT_PHONE_2 = _('Phone 2')
# Translators: Art used on tastes
TASTE_ART = _('Art')
# Translators: Music used on tastes
TASTE_MUSIC = _('Music')
# Translators: Tech used on tastes
TASTE_TECH = _('Tech')
# Translators: Cars used on tastes
TASTE_CARS = _('Cars') 
# Translators: Travels used on tastes
TASTE_TRAVELS = _('Travels')
# Translators: Clothes used on tastes
TASTE_CLOTHES = _('Clothes')
# Translators: Movies used on tastes
TASTE_CINE = _('Movies')
# Translators: Sports used on tastes
TASTE_SPORTS = _('Sports')
# Translators: Eco used on tastes
TASTE_ECO = _('Eco')
# Translators: Culture used on tastes
TASTE_CULTURE = _('Culture')
# Translators: Spectacles used on tastes
TASTE_SPECTACLES = _('Spectacles')
# Translators: Love used on tastes
TASTE_LOVE = _('Love')
# Translators: Food used on tastes
TASTE_FOOD = _('Food')
# Translators:Vacations used on tastes
TASTE_VACATIONS = _('Vacations')
# Translators: Services used on tastes
TASTE_SERVICES = _('Services')

#RegisterUserForm: Formulario con todos los campos basicos necesarios para el registro.
#PARAMS: ModelForm: Class ModelForm
#RETURN: Se devuelve cleaned_data con el caso de que los passwords no coincidan durante el registro.
class RegisterUserForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': HINT_NAME}), max_length=60)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': HINT_LASTNAME}), max_length=60)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': HINT_EMAIL}), max_length=90)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': HINT_PASSWORD1}), max_length=75, min_length=6)
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': HINT_PASSWORD2}), max_length=75, min_length=6)
    terms_service = forms.BooleanField(required=True,initial=False, label="")
    
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['bulletins'].label = ""
    
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email',
                  'password', 'password_2', 'bulletins',
                  'terms_service')
    def clean(self):
        cleaned_data = super(RegisterUserForm, self).clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("password_2")
        
        #Se verifica que los passwords esten ingresados y que no sean iguales para
        #notificar al usuario que los corrija.
        if password1 and password2 and password1 != password2:
            self._errors["password"] = self.error_class([ERROR_PASSDONTMATCH])
            del cleaned_data["password"]
            del cleaned_data["password_2"]
 
        return cleaned_data

#SendConfirmationForm: Formulario con un campo mail utilizado para reenviar la confirmacion
#                      de activacion de cuenta al usuario.
class SendConfirmationForm(Form):
    email = forms.EmailField(max_length=90)

#loginform: Formulario con los campos de email y password para iniciar sesion de un usuario,
#           adicionalmente contiene logica para verificar que el usuario se encuentra
#           registrado y que la contraseña es correcta.
#PARAMS: Form: Class Form
#RETURN: Se devuelve cleaned_data con el caso de usuario y contraseña incorrectos.
class LoginForm(Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': HINT_EMAIL}), max_length=90)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': HINT_PASSWORD1}), max_length=75, min_length=6)
    
    def clean(self): 
        cleaned_data = super(LoginForm, self).clean()
        mail = cleaned_data.get('email')
        password = cleaned_data.get("password")
        
        #Funcion que recibe el campo donde se debe desplegar el error y el error a desplegar.
        def clean_and_return(field, error):
            self._errors[field] = self.error_class([error])
            del cleaned_data["email"]
            del cleaned_data["password"]
            return cleaned_data
        
        try:
            #Se verifca que esten ingresados el mail y password, si es asi, se intenta
            #recuperar al usuario de la base de datos.
            if mail and password: user = Usuario.objects.get(email=mail)
            else: return cleaned_data
            
            #Se verifica que el usuario este activo antes de iniciar sesion.
            if user.active == False: clean_and_return("email", ERROR_USERNOTCONFIRMED)
            
            #En caso de no coincidir el password entregado con el guardado en la base de datos
            #se procede a informar al usuario
            if(password != user.password): clean_and_return("password", ERROR_WRONGPASS) 
            
            return cleaned_data
        #En caso de no exisitr el usuario se informa que no se encuentra registrado.
        except ObjectDoesNotExist: clean_and_return("email", ERROR_USERDONTEXIST)
        except Exception: return cleaned_data

#EditUserForm: Formulario que permite a un usuario modificar sus datos.
#PARAMS: ModelForm: Class ModelForm
class EditUserForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': HINT_NAME}), max_length=60)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': HINT_LASTNAME}), max_length=60)
    
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': HINT_EMAIL_1}), max_length=90)
    email_2 = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': HINT_EMAIL_2}), max_length=90, required=False)
   
    phone_1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': HINT_PHONE_1}), max_length=30, required=False)
    phone_2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': HINT_PHONE_2}), max_length=30, required=False)
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': HINT_PASSWORD1}), max_length=75, min_length=6)
    new_password_1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': HINT_NEW_PASSWORD_1}), max_length=75, min_length=6, required=False)
    new_password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': HINT_NEW_PASSWORD_2}), max_length=75, min_length=6, required=False)
    
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['art'].label = TASTE_ART
        self.fields['music'].label = TASTE_MUSIC
        self.fields['tech'].label = TASTE_TECH
        self.fields['cars'].label = TASTE_CARS
        self.fields['travels'].label = TASTE_TRAVELS
        self.fields['clothes'].label = TASTE_CLOTHES
        self.fields['cine'].label = TASTE_CINE
        self.fields['sports'].label = TASTE_SPORTS
        self.fields['eco'].label = TASTE_ECO
        self.fields['culture'].label = TASTE_CULTURE
        self.fields['spectacles'].label = TASTE_SPECTACLES
        self.fields['love'].label = TASTE_LOVE
        self.fields['food'].label = TASTE_FOOD
        self.fields['vacations'].label = TASTE_VACATIONS
        self.fields['services'].label = TASTE_SERVICES
        
    class Meta:
        model = Usuario
        fields = ('first_name','last_name',
                  'city',
                  'email','email_2',
                  'phone_1', 'phone_2',
                  'art', 'music',
                  'tech', 'cars', 'travels',
                  'clothes', 'cine', 'sports', 
                  'eco', 'culture', 'spectacles',
                  'love', 'food', 'vacations',
                  'services',
                  'password',
                  'new_password_1', 'new_password_2',
                  'lang')
        
    def clean(self):
        cleaned_data = super(EditUserForm, self).clean()
        password_new_1 = cleaned_data.get("new_password_1")
        password_new_2 = cleaned_data.get("new_password_2")
        
        #Se verifica que los passwords esten ingresados y que no sean iguales para
        #notificar al usuario que los corrija.
        if password_new_1 and password_new_2 and password_new_1 != password_new_2:
            self._errors["new_password_1"] = self.error_class([ERROR_PASSDONTMATCH])
            del cleaned_data["new_password_1"]
            del cleaned_data["new_password_2"]
  
        return cleaned_data
