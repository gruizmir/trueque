# -*- coding: utf-8 -*-
from django.forms import Form, ModelForm, IntegerField, TextInput, HiddenInput, ModelChoiceField, CharField, ChoiceField
from django.db import models
from transactions.models import Bid, Trade
from products.models import Product
from django.forms import RadioSelect

GRADES=(('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'))

class BidForm(ModelForm):	
	class Meta:
		model = Bid
		exclude = ('id_bid')

def getBidForm(id_owner):
	class ProductBidForm(Form):
		bid_q_amount = IntegerField(label="Ofrece Q", widget=TextInput(attrs={'size':20,'value':'0'}))
		bid_product_id = ModelChoiceField(queryset=Product.objects.filter(id_owner=id_owner))
	return ProductBidForm


class TradeForm(ModelForm):
	class Meta:
		model = Trade
		exclude = ('id_trade')

class TradeVerification(Form):
	code = CharField(label="Tú Código", widget=TextInput(attrs={'size':10}))
	rate = ChoiceField(required=False, widget=RadioSelect(), choices=GRADES)
