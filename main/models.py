# -*- coding: utf-8 -*-
from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class ProductFollower(models.Model):
    id_product = models.ForeignKey(Product, primary_key=True) # Field name made lowercase.
    id_user = models.ForeignKey(User) # Field name made lowercase.
    class Meta:
        db_table = u'Product_follower'
