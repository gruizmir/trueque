from django.db import models
from usuarios.models import Usuario

# TIPOS DE NOTIFICACION (type)
# message :	Mensajes (correo interno) de usuarios
# bid :		Ofertas en un nuevo producto
# like :	A una persona le gusta tu producto
# follow :	Una persona te sigue
# trade :	Intercambio completado

class Notification(models.Model):
    id_user = models.ForeignKey(Usuario) # Field name made lowercase.
    message = models.TextField() # Field name made lowercase.
    pending = models.BooleanField() # Field name made lowercase.
    datetime = models.DateTimeField(primary_key=True) # Field name made lowercase.
    link = models.CharField(max_length=150) # Field name made lowercase.
    ntype = models.CharField(max_length=30) # Field name made lowercase.
    class Meta:
        db_table = u'Notification'
