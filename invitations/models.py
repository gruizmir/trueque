from django.db import models
from usuarios.models import Usuario

class Invitation(models.Model):
    id_sender = models.ForeignKey(Usuario, primary_key=True, db_column='ID_sender') # Field name made lowercase.
    invitation_email = models.CharField(max_length=90, primary_key=True, db_column='Invitation_email') # Field name made lowercase.
    invitation_token = models.CharField(max_length=150, db_column='Invitation_token') # Field name made lowercase.
    invitation_pending = models.IntegerField(db_column='Invitation_pending') # Field name made lowercase.
    class Meta:
        db_table = u'Invitation'
