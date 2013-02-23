# -*- coding: utf-8 -*-
from transactions.models import Bid, Trade
from transactions.forms import BidForm, getBidForm, TradeForm, TradeVerification
from products.models import Product, Category, ProductCategory
from usuarios.views import is_loged
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.conf import settings
from datetime import datetime
from django.forms.formsets import formset_factory
import string
import random

#Funcion que muestra el formulario para ingresar una nueva oferta
def newBid(request, idProducto=None):	
	if is_loged(request):
		if idProducto==None:
			return HttpResponseRedirect("/")
		else:
			if request.method != "POST":
				prod = Product.objects.get(id_product=idProducto)
				if prod.product_active==True:
					ProductBidForm = formset_factory(getBidForm(request.session['member_id']))
					preBidForm = ProductBidForm()
					return render_to_response("new_bid.html", {'bid_form':preBidForm}, context_instance=RequestContext(request))
				else:
					return HttpResponse("ESTE PRODUCTO YA FUE INTERCAMBIADO")
			else:
				prod = Product.objects.get(id_product=idProducto)
				if prod.product_active==True:
					ProductBidForm = formset_factory(getBidForm())
					preBidForm = ProductBidForm(request.POST)
					if preBidForm.is_valid() and preBidForm.cleaned_data['bid_product_id']!=idProducto :
						if preBidForm.cleaned_data['bid_product_id']==0:
							bidProductID = None
							bidQ = preBidForm.cleaned_data['bid_q_amount']
						else:
							bidProductID = preBidForm.cleaned_data['bid_product_id']
							bidQ = 0
						data = {'id_product':idProducto,
								'id_bidder':request.session['member_id'],
								'bid_q':bidQ,
								'bid_id_product':bidProductID,
								'bid_datetime': datetime.now(),
								}	
						bidForm = BidForm(data)
						if bidForm.is_valid():
							bidForm.save()
							return HttpResponseRedirect("/products/" + str(idProducto))
						else:
							return HttpResponse("DATA ERROR")
					else:
						return HttpResponse("FAIL")
				else:
					return HttpResponse("ESTE PRODUCTO ACABA DE SER INTERCAMBIADO")
	else:
		return HttpResponse("NO AUTORIZADO")



def makeTrade(request, idProduct):
	if request.method=="POST":
		if is_loged(request):
			data = {'id_dealer':request.session['member_id'],
					'id_bid':request.POST['group_product'],
					'trade_code_dealer':id_generator(),
					'trade_code_bidder':id_generator(),
					'trade_pending_dealer':True,
					'trade_pending_bidder':True,
					'trade_datetime':datetime.now(),
					'trade_valid':False,
					}
			tradeForm = TradeForm(data)
			if tradeForm.is_valid():
				tradeForm.save()
				product = Product.objects.get(id_product=idProduct)
				product.product_active = False
				product.save()
				return HttpResponseRedirect("/products/" + str(idProduct))
			else:
				return HttpResponse("DATA ERROR")
		else:
			return HttpResponse("NO AUTORIZADO")
	else:
		return HttpResponse("FAIL")

#Genera el codigo de 6 caracteres que se usa para confirmar el intercambio
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))	


def showPending(request):
	if is_loged(request):
		dealer_pendings = Trade.objects.filter(id_dealer=request.session['member_id']).filter(trade_pending_dealer=True)
		bidder_pendings = Trade.objects.filter(id_bid__id_bidder=request.session['member_id']).filter(trade_pending_bidder=True)
		return render_to_response("pendings.html", {'dealer_pendings':dealer_pendings, 'bidder_pendings':bidder_pendings})
	else:
		return HttpResponse("NO AUTORIZADO")


def verifyTrade(request, idTrade=None):
	if request.method == "POST":
		if is_loged(request):
			tradeVer = TradeVerification(request.POST)
			if tradeVer.is_valid():
				trade = Trade.objects.get(id_trade=idTrade)
				if request.session['member_id']==trade.id_dealer.id_usuario:
					if trade.trade_code_dealer == tradeVer.cleaned_data['code']:
						trade.trade_pending_dealer = False
						trade.save()
						rate(trade.id_bid.id_bidder, tradeVer.cleaned_data['rate'])
						if trade.trade_pending_bidder==False:
							exchange(trade.id_bid.id_bid, trade.id_bid.id_product.id_product)
							trade.trade_valid=True
							trade.save()
							return HttpResponseRedirect("/products/" + str(idProduct))
						else:
							return HttpResponse("FALTA VERIFICACION DEL COMPRADOR")
					else:
						return HttpResponse("CODIGO NO VALIDO")
				elif request.session['member_id']==trade.id_bid.id_bidder.id_usuario:
					if trade.trade_code_bidder == tradeVer.cleaned_data['code']:
						trade.trade_pending_bidder = False
						trade.save()
						rate(trade.id_dealer, tradeVer.cleaned_data['rate'])
						if trade.trade_pending_dealer==False:
							exchange(trade.id_bid.id_bid, trade.id_bid.id_product.id_product)
							trade.trade_valid=True
							trade.save()
							return HttpResponseRedirect("/products/" + str(trade.id_bid.id_product.id_product))
						else:
							return HttpResponse("FALTA VERIFICACION DEL VENDEDOR")
					else:
						return HttpResponse("CODIGO NO VALIDO")
				else:
					return HttpResponse("NO INVOLUCRADO")
			else:
				return HttpResponse("DATA ERROR")
		else:
			return HttpResponse("NO AUTORIZADO")
	else:
		if is_loged(request):
			tradeVer = TradeVerification()
			return render_to_response("trade_verifier.html", {'form':tradeVer,'id_trade':idTrade}, context_instance=RequestContext(request))
		else:
			return HttpResponse("NO AUTORIZADO")

#Funcion llamada para cambiar de Owner a un producto, y restar la cantidad de Q ofrecida
#en caso de "compra"
def exchange(idBid, idProduct):
	product = Product.objects.get(id_product=idProduct)
	bid = Bid.objects.get(id_bid=idBid)
	dealer = product.id_owner
	bidder = bid.id_bidder
	product.id_owner = bidder
	if bid.bid_id_product != None:			#Significa que fue un trueque por producto
		bid.bid_id_product.id_owner = dealer
	else:									#Significa que fue un trueque por Q
		dealer.usuario_quds += bid.bid_q
		bidder.usuario_quds -= bid.bid_q

#Funcion encargada de agregar la calificacion a un usuario
def rate(usuario, nota):
	cant = usuario.usuario_ranking_qty
	prevNota = usuario.usuario_rating
	usuario.usuario_rating = (prevNota*cant + int(nota))/(cant + 1)
	usuario.usuario_ranking_qty += 1
	usuario.save()
