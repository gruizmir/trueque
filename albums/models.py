from django.db import models
from products.models import Product
from usuarios.models import Usuario

class Album(models.Model):
    id_album = models.AutoField(primary_key=True, db_column='ID_album') # Field name made lowercase.
    id_owner = models.ForeignKey(Usuario, db_column='ID_owner') # Field name made lowercase.
    album_name = models.CharField(max_length=60, db_column='Album_name') # Field name made lowercase.
    album_edit = models.BooleanField(db_column='Album_edit')
    class Meta:
        db_table = u'Album'
    
    def set_album(self, user, album_name, can_edit):
        self.id_owner = user
        self.album_name = album_name
        self.album_edit = can_edit

class AlbumProduct(models.Model):
    id_album = models.ForeignKey(Album, primary_key=True, db_column='ID_album') # Field name made lowercase.
    id_product = models.ForeignKey(Product, primary_key=True, db_column='ID_product') # Field name made lowercase.
    class Meta:
        db_table = u'Album_product'
