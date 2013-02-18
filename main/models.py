# -*- coding: utf-8 -*-
from django.db import models
from products.models import Product
from usuarios.models import Usuario

class ProductFollower(models.Model):
    id_product = models.ForeignKey(Product, primary_key=True, db_column='ID_product') # Field name made lowercase.
    id_user = models.ForeignKey(Usuario, db_column='ID_user') # Field name made lowercase.
    class Meta:
        db_table = u'Product_follower'
