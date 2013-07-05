from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    id_conversation = models.IntegerField() # Field name made lowercase.
    id_sender = models.ForeignKey(User) # Field name made lowercase.
    id_receiver = models.ForeignKey(User, related_name="+") # Field name made lowercase.
    subject = models.CharField(max_length=300) # Field name made lowercase.
    text = models.TextField(blank=True) # Field name made lowercase.
    datetime = models.DateTimeField() # Field name made lowercase.
    read = models.BooleanField(default=False) # Field name made lowercase.
    class Meta:
        db_table = u'Message'
