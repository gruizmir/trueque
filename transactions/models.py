# -*- coding: utf-8 -*-
from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class Bid(models.Model):
    id_product = models.ForeignKey(Product) # Field name made lowercase.
    id_bidder = models.ForeignKey(User) # Field name made lowercase.
    q = models.IntegerField(null=True, blank=True) # Field name made lowercase.
    id_bid_product = models.ForeignKey(Product, null=True, blank=True, related_name="+") # Field name made lowercase.
    datetime = models.DateTimeField() # Field name made lowercase.
    class Meta:
        db_table = u'Bid'

class Trade(models.Model):
    id_dealer = models.ForeignKey(User, null=True, blank=True) # Field name made lowercase.
    id_bid = models.ForeignKey(Bid, null=True, blank=True) # Field name made lowercase.
    code_dealer = models.CharField(null=True, max_length=30, blank=True) # Field name made lowercase.
    code_bidder = models.CharField(null=True, max_length=30, blank=True) # Field name made lowercase.
    pending_dealer = models.BooleanField(default=True) # Field name made lowercase.
    pending_bidder = models.BooleanField(default=True) # Field name made lowercase.
    datetime = models.DateTimeField() # Field name made lowercase.
    valid = models.BooleanField(default=False) # Field name made lowercase.
    class Meta:
        db_table = u'Trade'
