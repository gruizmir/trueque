# -*- coding: utf-8 -*-
from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class ProductFollower(models.Model):
    id_product = models.ForeignKey(Product, primary_key=True) # Field name made lowercase.
    id_user = models.ForeignKey(User) # Field name made lowercase.
    class Meta:
        db_table = u'Product_follower'


class Level(models.Model):
    inf = models.IntegerField()
    sup = models.IntegerField()
    name = models.CharField(max_length=90)
    
    class Meta:
        db_table = u'Level'
    
    def __unicode__(self):
        return self.name
    
    def get(self, value):
        temp = Level.objects.filter(inf__lte = int(value)).filter(sup__gte = int(value))
        if temp.count()==1:
            self = list(temp)[0]
            return self
        else:
            return None


class Point(models.Model):
    action = models.CharField(max_length=90)
    qty = models.IntegerField()
    
    class Meta:
        db_table = u'Points'
    
    def __unicode__(self):
        return self.action
