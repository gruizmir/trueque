from django.db import models
from products.models import Product
from usuarios.models import Usuario

class ProductFollower(models.Model):
    id_product = models.ForeignKey(Product, primary_key=True, db_column='ID_product') # Field name made lowercase.
    id_user = models.ForeignKey(Usuario, db_column='ID_user') # Field name made lowercase.
    class Meta:
        db_table = u'Product_follower'

class Comment(models.Model):
    id_product = models.ForeignKey(Product, primary_key=True, db_column='ID_product') # Field name made lowercase.
    id_sender = models.ForeignKey(Usuario, db_column='ID_sender') # Field name made lowercase.
    comment_subject = models.CharField(max_length=300, db_column='Comment_subject', blank=True) # Field name made lowercase.
    comment_text = models.TextField(db_column='Comment_text', blank=True) # Field name made lowercase.
    comment_datetime = models.DateTimeField(db_column='Comment_datetime') # Field name made lowercase.
    class Meta:
        db_table = u'Comment'
