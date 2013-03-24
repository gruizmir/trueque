# -*- coding: utf-8 -*-
from transactions.models import Bid, Trade
from transactions.forms import BidForm, TradeForm, TradeVerification
from products.models import Product, Category, ProductCategory
from usuarios.views import is_loged
from usuarios.models import Usuario
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
from django.forms.formsets import formset_factory
import string
import random

#newBid: Muestra el formulario para ingresar una nueva oferta. También procesa la oferta ingresada por el usuario
#		 Comprueba factibilidad de realizar una nueva oferta.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#		 idProduct:	ID del producto al que se le va a hacer una nueva oferta
#RETURN: Si no se ha enviado formulario, retorna un render con el formulario para el nuevo Bid.
#		 Si se guarda la nueva Bid, retorna a la página del producto.
#		 Si no se puede establecer la oferta, retorna un mensaje de error con la posible causa.
def newBid(request, idProducto=None):	
	if is_loged(request):
		if idProducto==None:
			return HttpResponseRedirect("/")
		else:
			if request.method != "POST":
				prod = Product.objects.get(id_product=idProducto)
				if prod.product_active==True:
					bidderProducts = Product.objects.filter(id_owner = request.session['member_id'])
					return render_to_response("new_bid.html", {'products':bidderProducts}, context_instance=RequestContext(request))
				else:
					return HttpResponse("ESTE PRODUCTO YA FUE INTERCAMBIADO")
			else:
				prod = Product.objects.get(id_product=idProducto)
				if prod.product_active==True:
					if 'bid_product' in request.POST:
						bidProductID = request.POST['bid_product']
						bid_q = 0
					else:
						try:
							bid_q = int(request.POST['bid_q_amount'])
							user = Usuario.objects.get(id_usuario = request.session['member_id'])
							bidProductID = None
							if bid_q == 0 or bid_q > user.usuario_quds :
								return HttpResponse("MONTO NO VALIDO")
						except ValueError: 
							return HttpResponse("MONTO NO VALIDO")
					if bidProductID != idProducto:
						data = {'id_product':idProducto,
							'id_bidder':request.session['member_id'],
							'bid_q': bid_q,
							'bid_id_product': bidProductID,
							'bid_datetime':datetime.now(),
							}
						bidForm = BidForm(data)
						if bidForm.is_valid():
							bidForm.save()
							return HttpResponseRedirect("/products/" + str(idProducto))
						else:
							return HttpResponse("DATA ERROR")
					else:
						return HttpResponse("SAME OBJECT")
				else:
					return HttpResponse("ESTE PRODUCTO ACABA DE SER INTERCAMBIADO")
	else:
		return HttpResponse("NO AUTORIZADO")


#makeTrade: Maneja el intercambio de un producto con la oferta ingresada por otro usuario.
#			Debe recibir por POST el dato del id_bid elegido para hacer la oferta.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#		 idProduct:	ID del producto que se está intercambiando.
#RETURN: Si el intercambio es factible y se realiza, retorna a la página del producto.
#		 Si no se puede hacer el intercambio, retorna un mensaje de error con la posible causa.
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
				bidder = Bid.objects.get(id_bid = request.POST['group_product']).id_bidder
				owner = product.id_owner
				sendTradeMail(owner, bidder, trade.trade_code_dealer, trade.trade_code_bidder)
				return HttpResponseRedirect("/products/" + str(idProduct))
			else:
				return HttpResponse("DATA ERROR")
		else:
			return HttpResponse("NO AUTORIZADO")
	else:
		return HttpResponse("FAIL")


#id_generator: Genera un codigo de 6 caracteres que se usa para confirmar el intercambio.
#PARAMS: size: tamaño del string deseado. Por default, su valor es 6.
#		 chars: coleccion de caracteres desde los que se quiere extraer el codigo. Por default,
#				se usa el conjunto de letras ascii mayusculas y los digitos.	
#RETURN: Codigo de 'size' caracteres con valores aleatorios.
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))	


#showPending: Muestra las transacciones que el usuario aun no ha confirmado, ya sea como 'vendedor' o 'comprador'.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario. Contiene datos
#				  del usuario logueado.
#RETURN: render de la pagina con los datos de transacciones pendientes.
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


#Funcion encargada de enviar los correos con las claves de bidder y owner.
#Al owner se le envia la clave del bidder y viceversa.
def sendTradeMail(owner, bidder, code_dealer, code_bidder):
	#Mail para el propietario del producto
	dealer_msg = 'Usted ha realizado un nuevo trueque con el usuario ' + bidder.usuario_name + " " + bidder.usuario_lastname + ".\nSu correo de contacto es " + bidder.usuario_email_1 + ".\nAl realizar el intercambio final de tu producto, él debe entregarte un código de confirmación que debes usar para finalizar el trueque. Tú deberás entregarle el siguiente código para confirmar el trueque:\n" + code_bidder
	send_mail('Confirmación de Trueque', dealer_msg , 'trueque@trueque.in', [owner.usuario_email_1], fail_silently=False)
	
	#Mail para el bidder
	bidder_msg = 'Usted ha realizado un nuevo trueque con el usuario ' + owner.usuario_name + " " + owner.usuario_lastname + ".\nSu correo de contacto es " + owner.usuario_email_1 + ".\nAl realizar el intercambio final de tu producto, él debe entregarte un código de confirmación que debes usar para finalizar el trueque. Tú deberás entregarle el siguiente código para confirmar el trueque:\n" + code_dealer
	send_mail('Confirmación de Trueque', bidder_msg , 'trueque@trueque.in', [bidder.usuario_email_1], fail_silently=False)
