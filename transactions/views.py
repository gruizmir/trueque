# -*- coding: utf-8 -*-
from transactions.models import Bid
from transactions.forms import BidForm, ProductBidForm
from products.models import Product, Category, ProductCategory
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.conf import settings
from datetime import datetime

#Funcion que muestra el formulario para ingresar una nueva oferta
def newBid(request, idProducto=None):	
	#Falta verificar que este logueado
	if idProducto==None:
		return HttpResponseRedirect("/")
	else:
		if request.method != "POST":
			preBidForm = ProductBidForm()
			return render_to_response("new_bid.html", {'bid_form':preBidForm}, context_instance=RequestContext(request))
		else:
			preBidForm = ProductBidForm(request.POST)
			if preBidForm.is_valid() and preBidForm.cleaned_data['bid_product_id']!=idProducto :
				if preBidForm.cleaned_data['bid_product_id']==0:
					bidProductID = None
					bidQ = preBidForm.cleaned_data['bid_q_amount']
				else:
					bidProductID = preBidForm.cleaned_data['bid_product_id']
					bidQ = 0
				data = {'id_product':idProducto,
#						'id_bidder':request.session['member_id'],
						'id_bidder':2,
						'bid_q':bidQ,
						'bid_id_product':bidProductID,
						'bid_datetime': datetime.now(),
						}	
				bidForm = BidForm(data)
				if bidForm.is_valid():
					bidForm.save()
					return HttpResponseRedirect("/products/" + str(idProducto))
				else:
					return HttpResponse("DATA_ERROR")
			else:
				return HttpResponse("FAIL")
