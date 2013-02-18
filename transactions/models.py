# -*- coding: utf-8 -*-
from django.db import models
from products.models import Product
from usuarios.models import Usuario

class Bid(models.Model):
    id_bid = models.AutoField(primary_key=True, db_column='ID_bid') # Field name made lowercase.
    id_product = models.ForeignKey(Product, db_column='ID_product') # Field name made lowercase.
    id_bidder = models.ForeignKey(Usuario, db_column='ID_bidder') # Field name made lowercase.
    bid_q = models.IntegerField(null=True, db_column='BID_Q', blank=True) # Field name made lowercase.
    bid_id_product = models.ForeignKey(Product, null=True, db_column='BID_ID_product', blank=True, related_name="+") # Field name made lowercase.
    bid_datetime = models.DateTimeField(db_column='BID_datetime') # Field name made lowercase.
    class Meta:
        db_table = u'Bid'

class Trade(models.Model):
    id_trade = models.AutoField(primary_key=True, db_column='ID_trade') # Field name made lowercase.
    id_dealer = models.ForeignKey(Usuario, null=True, db_column='ID_dealer', blank=True) # Field name made lowercase.
    id_bid = models.ForeignKey(Bid, null=True, db_column='ID_bid', blank=True) # Field name made lowercase.
    trade_code_dealer = models.CharField(max_length=30, db_column='Trade_code_dealer', blank=True) # Field name made lowercase.
    trade_code_bidder = models.IntegerField(null=True, db_column='Trade_code_bidder', blank=True) # Field name made lowercase.
    trade_pending_dealer = models.IntegerField(db_column='Trade_pending_dealer') # Field name made lowercase.
    trade_pending_bidder = models.IntegerField(db_column='Trade_pending_bidder') # Field name made lowercase.
    trade_datetime = models.DateTimeField(db_column='Trade_datetime') # Field name made lowercase.
    trade_valid = models.IntegerField(db_column='Trade_valid') # Field name made lowercase.
    class Meta:
        db_table = u'Trade'
