from django.forms import ModelForm
from usuarios.models import Usuario
from django import forms

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
        
        if password1 and password2 and password1 != password2:
            msg = u"Passwords don't match"
            self._errors["usuario_password"] = self.error_class([msg])
            
            del cleaned_data["usuario_password"]
            del cleaned_data["usuario_password_2"]
        
        return cleaned_data
