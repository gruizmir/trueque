# -*- coding: utf-8 -*-
from django.db import models
from usuarios.models import Usuario

class Product(models.Model):
    id_owner = models.ForeignKey(Usuario) # Field name made lowercase.
    name = models.CharField(max_length=90) # Field name made lowercase.
    img = models.CharField(max_length=300) # Field name made lowercase.
    description = models.TextField(blank=True) # Field name made lowercase.
    q_amount = models.IntegerField() # Field name made lowercase.
    start_datetime = models.DateTimeField() # Field name made lowercase.
    end_datetime = models.DateTimeField() # Field name made lowercase.
    follower_qty = models.IntegerField() # Field name made lowercase.
    visit_qty = models.IntegerField() # Field name made lowercase.
    country = models.CharField(max_length=60) # Field name made lowercase.
    city = models.CharField(max_length=60) # Field name made lowercase.
    featured = models.BooleanField(default=False) # Field name made lowercase.
    featured_time = models.IntegerField() # Field name made lowercase.
    active = models.BooleanField(default=True) # Field name made lowercase.
    class Meta:
        db_table = u'Product'
        
class Category(models.Model):
    name = models.CharField(max_length=60) # Field name made lowercase.
    class Meta:
        db_table = u'Category'

class ProductCategory(models.Model):
    
    id_product = models.ForeignKey(Product) # Field name made lowercase.
    id_category = models.ForeignKey(Category) # Field name made lowercase.
    class Meta:
        db_table = u'Product_category'

class Comment(models.Model):
    id_product = models.ForeignKey(Product) # Field name made lowercase.
    id_sender = models.ForeignKey(Usuario) # Field name made lowercase.
    subject = models.CharField(max_length=300, blank=True) # Field name made lowercase.
    text = models.TextField(blank=True) # Field name made lowercase.
    datetime = models.DateTimeField() # Field name made lowercase.
    class Meta:
        db_table = u'Comment'
