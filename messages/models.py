from django.db import models
from usuarios.models import Usuario

class Message(models.Model):
    id_message = models.AutoField(primary_key=True, db_column='ID_message') # Field name made lowercase.
    id_conversation = models.IntegerField(primary_key=True, db_column='ID_conversation') # Field name made lowercase.
    id_sender = models.ForeignKey(Usuario, db_column='ID_sender') # Field name made lowercase.
    id_receiver = models.ForeignKey(Usuario, db_column='ID_receiver', related_name="+") # Field name made lowercase.
    message_subject = models.CharField(max_length=300, db_column='Message_subject') # Field name made lowercase.
    message_text = models.TextField(db_column='Message_text', blank=True) # Field name made lowercase.
    message_datetime = models.DateTimeField(db_column='Message_datetime') # Field name made lowercase.
    message_read = models.IntegerField(db_column='Message_read') # Field name made lowercase.
    class Meta:
        db_table = u'Message'
