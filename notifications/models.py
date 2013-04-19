from django.db import models
from usuarios.models import Usuario

# TIPOS DE NOTIFICACION (notification_type)
# message :	Mensajes (correo interno) de usuarios
# bid :		Ofertas en un nuevo producto
# like :	A una persona le gusta tu producto
# follow :	Una persona te sigue
# trade :	Intercambio completado

class Notification(models.Model):
    id_user = models.ForeignKey(Usuario, primary_key=True, db_column='ID_user') # Field name made lowercase.
    notification_message = models.TextField(db_column='Notification_message') # Field name made lowercase.
    notification_pending = models.BooleanField(db_column='Notification_pending') # Field name made lowercase.
    notification_datetime = models.DateTimeField(primary_key=True, db_column='Notification_datetime') # Field name made lowercase.
    notification_link = models.CharField(max_length=150, db_column='Notification_link') # Field name made lowercase.
    notification_type = models.CharField(max_length=30, db_column='Notification_link') # Field name made lowercase.
    class Meta:
        db_table = u'Notification'
