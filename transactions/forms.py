# -*- coding: utf-8 -*-
from django.forms import Form, ModelForm, CharField, EmailField, IntegerField, TextInput, PasswordInput, Textarea, BooleanField,CheckboxInput, FileField, HiddenInput
from django.db import models
from transactions.models import Bid

class BidForm(ModelForm):	
	class Meta:
		model = Bid
		exclude = ('id_bid')

class ProductBidForm(Form):
	bid_q_amount = IntegerField(label="Ofrece Q", widget=TextInput(attrs={'size':20,'value':'0'}))
	bid_product_name = CharField(label="Producto", widget=TextInput(attrs={'size':40}), required=False)
	bid_product_id = IntegerField(label="Product_id", widget=TextInput(attrs={'size':20, 'value':'0'}), required=False)
#	bid_product_id = IntegerField(widget=HiddenInput(attrs={'value':'0'}))
