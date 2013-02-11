from django.db import models
from usuarios.models import Usuario

class Notification(models.Model):
    id_user = models.ForeignKey(Usuario, primary_key=True, db_column='ID_user') # Field name made lowercase.
    notification_message = models.TextField(db_column='Notification_message') # Field name made lowercase.
    notification_pending = models.IntegerField(db_column='Notification_pending') # Field name made lowercase.
    notification_datetime = models.DateTimeField(primary_key=True, db_column='Notification_datetime') # Field name made lowercase.
    notification_link = models.CharField(max_length=150, db_column='Notification_link') # Field name made lowercase.
    class Meta:
        db_table = u'Notification'
