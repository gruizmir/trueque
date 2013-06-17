# -*- coding: utf-8 -*-
from albums.models import Album, AlbumProduct
from datetime import datetime
from django.conf import settings
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from products.models import Product, Category, ProductCategory
from transactions.forms import BidForm, TradeForm, TradeVerification
from transactions.models import Bid, Trade
from usuarios.models import Usuario
from usuarios.views import is_loged
import random
import string

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
			if request.is_ajax():
				prod = Product.objects.get(id=idProducto)
				if prod.active==True:
					bidderProducts = Product.objects.filter(id_owner = request.session['member_id'])
					title = "Nueva oferta"
					usuario = Usuario.objects.get(id_usuario=request.session['member_id'])
					render_bid = render_to_response('new_bid.html', {'products':bidderProducts, 'title':title, 'user':usuario}, context_instance=RequestContext(request))
					message = {"bid_data": render_bid.content}
					json = simplejson.dumps(message)
					return HttpResponse(json, mimetype='application/json')
				
				else:
					return HttpResponse("ESTE PRODUCTO YA FUE INTERCAMBIADO")
			else:
				prod = Product.objects.get(id=idProducto)
				if prod.active==True:
					if 'bid_product' in request.POST:
						bidProductID = request.POST['bid_product']
						bid_q = 0
					else:
						try:
							bid_q = int(request.POST['bid_q_amount'])
							user = Usuario.objects.get(id_usuario = request.session['member_id'])
							bidProductID = None
							if bid_q == 0 or bid_q > user.quds or bid_q < 0:
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
		return HttpResponse("/login")


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
					'idcode_dealer':id_generator(),
					'idcode_bidder':id_generator(),
					'idpending_dealer':True,
					'idpending_bidder':True,
					'iddatetime':datetime.now(),
					'idvalid':False,
					}
			tradeForm = TradeForm(data)
			if tradeForm.is_valid():
				tradeForm.save()
				product = Product.objects.get(id=idProduct)
				product.active = False
				product.save()
				bidder = Bid.objects.get(id = request.POST['group_product']).id_bidder
				owner = product.id_owner
				sendTradeMail(owner, bidder, tradeForm.cleaned_data['idcode_dealer'], tradeForm.cleaned_data['idcode_bidder'])
				return HttpResponseRedirect("/products/" + str(idProduct))
			else:
				return HttpResponse("DATA ERROR")
		else:
			return HttpResponse("/login")
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
		dealer_pendings = Trade.objects.filter(id_dealer=request.session['member_id']).filter(idpending_dealer=True)
		bidder_pendings = Trade.objects.filter(id_bid__id_bidder=request.session['member_id']).filter(idpending_bidder=True)
		title = "Trueques pendientes"
		usuario = Usuario.objects.get(id_usuario=request.session['member_id'])
		return render_to_response("pendings.html", {'dealer_pendings':dealer_pendings, 'bidder_pendings':bidder_pendings, 'title':title, 'user':usuario})
	else:
		return HttpResponse("/login")


def verifyTrade(request, idTrade=None):
	if request.method == "POST":
		if is_loged(request):
			tradeVer = TradeVerification(request.POST)
			if tradeVer.is_valid():
				trade = Trade.objects.get(id_trade=idTrade)
				if request.session['member_id']==trade.id_dealer.id_usuario:
					if trade.idcode_dealer == tradeVer.cleaned_data['code']:
						trade.idpending_dealer = False
						trade.save()
						rate(trade.id_bid.id_bidder, tradeVer.cleaned_data['rate'])
						if trade.idpending_bidder==False:
							exchange(trade.id_bid.id, trade.id_bid.id_product.id_product)
							trade.idvalid=True
							trade.save()
							#Vuelve a mi nuevo producto recibido si existe, o si no a la busqueda (es el vendedor)
							if trade.id_bid.bid_q == 0:
								return HttpResponseRedirect("/products/" )
							else:
								return HttpResponseRedirect("/products/" + str(trade.id_bid.bid_id_product))
						else:
							return HttpResponse("FALTA VERIFICACION DEL COMPRADOR")
					else:
						return HttpResponse("CODIGO NO VALIDO")
				elif request.session['member_id']==trade.id_bid.id_bidder.id_usuario:
					if trade.idcode_bidder == tradeVer.cleaned_data['code']:
						trade.idpending_bidder = False
						trade.save()
						rate(trade.id_dealer, tradeVer.cleaned_data['rate'])
						if trade.idpending_dealer==False:
							exchange(trade.id_bid.id, trade.id_bid.id_product.id_product)
							trade.idvalid=True
							trade.save()
							
							#Vuelve al productp adquirido (es el comprador)
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
			return HttpResponse("/login")
	else:
		if is_loged(request):
			tradeVer = TradeVerification()
			title = "Verificar trueque"
			usuario = Usuario.objects.get(id_usuario=request.session['member_id'])
			return render_to_response("trade_idverifier.html", {'form':tradeVer,'id_trade':idTrade, 'title':title, 'user':usuario}, context_instance=RequestContext(request))
		else:
			return HttpResponse("/login")

#Funcion llamada para cambiar de Owner a un producto, y restar la cantidad de Q ofrecida
#en caso de "compra"
def exchange(idBid, idProduct):
	product = Product.objects.get(id=idProduct)
	bid = Bid.objects.get(id=idBid)
	dealer = product.id_owner
	bidder = bid.id_bidder
	product.id_owner = bidder
	saveAlbumData(product, bidder)
	if bid.bid_id_product != None:			#Significa que fue un trueque por producto
		bid.bid_id_product.id_owner = dealer
		saveAlbumData(bid.bid_id_product, dealer)
	else:									#Significa que fue un trueque por Q
		dealer.quds += bid.bid_q
		bidder.quds -= bid.bid_q

#saveAlbumData: 	Ingresa el registro de que el nuevo producto pertenece al album Trueques
#PARAMS: product: 	Objecto producto recien guardado
#		 idUsuario:	ID del usuario al que le pertenece el album y el producto
#RETURN: 
def saveAlbumData(producto, idUsuario):
	album = Album.objects.filter(id_owner=idUsuario).get(album_name='Trueques')
	albumProd = AlbumProduct()
	albumProd.id_album = album
	albumProd.id_product = producto
	albumProd.save()

#Funcion encargada de agregar la calificacion a un usuario
def rate(usuario, nota):
	cant = usuario.ranking_qty
	prevNota = usuario.rating
	usuario.rating = (prevNota*cant + int(nota))/(cant + 1)
	usuario.ranking_qty += 1
	usuario.save()


#Funcion encargada de enviar los correos con las claves de bidder y owner.
#Al owner se le envia la clave del bidder y viceversa.
def sendTradeMail(owner, bidder, code_dealer, code_bidder):
	#Mail para el propietario del producto
	dealer_msg = u"Usted ha realizado un nuevo trueque con el usuario " + bidder.first_name + " " + bidder.last_name + u".\nSu correo de contacto es " + bidder.email + u".\nAl realizar el intercambio final de tu producto, él debe entregarte un código de confirmación que debes usar para finalizar el trueque. Tú deberás entregarle el siguiente código para confirmar el trueque:\n" + code_bidder
	send_mail('Confirmación de Trueque', dealer_msg , 'trueque@trueque.in', [owner.email], fail_silently=False)
	
	#Mail para el bidder
	bidder_msg = u"Usted ha realizado un nuevo trueque con el usuario " + owner.first_name + " " + owner.last_name + u".\nSu correo de contacto es " + owner.email + u".\nAl realizar el intercambio final de tu producto, él debe entregarte un código de confirmación que debes usar para finalizar el trueque. Tú deberás entregarle el siguiente código para confirmar el trueque:\n" + code_dealer
	send_mail('Confirmación de Trueque', bidder_msg , 'trueque@trueque.in', [bidder.email], fail_silently=False)
