from django.db import models
from django.contrib.auth.models import User

class Invitation(models.Model):
    id_sender = models.ForeignKey(User) # Field name made lowercase.
    email = models.CharField(max_length=90) # Field name made lowercase.
    token = models.CharField(max_length=150) # Field name made lowercase.
    pending = models.BooleanField(default=True) # Field name made lowercase.
    class Meta:
        db_table = u'Invitation'
