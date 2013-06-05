from django.db import models
from usuarios.models import Usuario

class Invitation(models.Model):
    id_invitarion = models.IntegerField(primary_key=True, db_column='ID_invitation') # Field name made lowercase.
    id_sender = models.ForeignKey(Usuario, db_column='ID_sender') # Field name made lowercase.
    invitation_email = models.CharField(max_length=90, db_column='Invitation_email') # Field name made lowercase.
    invitation_token = models.CharField(max_length=150, db_column='Invitation_token') # Field name made lowercase.
    invitation_pending = models.BooleanField(db_column='Invitation_pending') # Field name made lowercase.
    class Meta:
        db_table = u'Invitation'
