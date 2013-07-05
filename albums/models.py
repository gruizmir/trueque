from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class Album(models.Model):
    id_owner = models.ForeignKey(User) # Field name made lowercase.
    name = models.CharField(max_length=60) # Field name made lowercase.
    edit = models.BooleanField()
    class Meta:
        db_table = u'Album'
    
    def set_album(self, user, album_name, can_edit):
        self.id_owner = user
        self.name = album_name
        self.edit = can_edit
    
    def __unicode__(self):
        return self.name + " of " + self.id_owner.get_full_name()
    
class AlbumProduct(models.Model):
    id_album = models.ForeignKey(Album) # Field name made lowercase.
    id_product = models.ForeignKey(Product) # Field name made lowercase.
    class Meta:
        db_table = u'Album_product'
    
    def __unicode__(self):
        return self.id_product.name + " in " + self.id_album.name
