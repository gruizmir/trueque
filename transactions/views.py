# -*- coding: utf-8 -*-
from albums.models import Album, AlbumProduct
from albums.views import savePendantProduct
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
from django.contrib.auth.models import User
import random
import string

#newBid: Muestra el formulario para ingresar una nueva oferta. También procesa la oferta ingresada por el usuario
#         Comprueba factibilidad de realizar una nueva oferta.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#         idProduct:    ID del producto al que se le va a hacer una nueva oferta
#RETURN: Si no se ha enviado formulario, retorna un render con el formulario para el nuevo Bid.
#         Si se guarda la nueva Bid, retorna a la página del producto.
#         Si no se puede establecer la oferta, retorna un mensaje de error con la posible causa.
def newBid(request, idProduct=None):    
    if is_loged(request):
        if idProduct==None:
            return HttpResponseRedirect("/")
        else:
            if request.is_ajax() and not request.method=="POST":
                prod = Product.objects.get(id=idProduct)
                if prod.active==True:
                    bidderProducts = Product.objects.filter(id_owner = request.session['member_id'])
                    title = "Nueva oferta"
                    usuario = User.objects.get(id=request.session['member_id'])
                    render_bid = render_to_response('new_bid.html', {'products':bidderProducts, 'title':title, 'user':usuario, 'owner_product':idProduct}, context_instance=RequestContext(request))
                    message = {"bid_data": render_bid.content}
                    json = simplejson.dumps(message)
                    return HttpResponse(json, mimetype='application/json')
                
                else:
                    return HttpResponse("ESTE PRODUCTO YA FUE INTERCAMBIADO")
            elif request.is_ajax() and request.method=="POST":
                prod = Product.objects.get(id=idProduct)
                if prod.active==True:
                    if 'bid_product' in request.POST:
                        bidProductID = request.POST['bid_product']
                        bid_q = 0
                    else:
                        try:
                            bid_q = int(request.POST['bid_q_amount'])
                            user = User.objects.get(id = request.session['member_id'])
                            bidProductID = None
                            if bid_q == 0 or bid_q > user.profile.quds or bid_q < 0:
                                render_bid_result = render_to_response('bid_transaction_result.html', {'error_amount': True})
                                message = {"bid_result_data": render_bid_result.content}
                                json = simplejson.dumps(message)
                                return HttpResponse(json, mimetype='application/json')
                        except ValueError: 
                            render_bid_result = render_to_response('bid_transaction_result.html', {'error_amount': True})
                            message = {"bid_result_data": render_bid_result.content}
                            json = simplejson.dumps(message)
                            return HttpResponse(json, mimetype='application/json')
                    if bidProductID != idProduct:
                        data = {'id_product':idProduct,
                            'id_bidder':request.session['member_id'],
                            'q': bid_q,
                            'id_bid_product': bidProductID,
                            'datetime':datetime.now(),
                            }
                        bidForm = BidForm(data)
                        if bidForm.is_valid():
                            bidForm.save()
                            render_bid_result = render_to_response('bid_transaction_result.html', {'correct_bid': True})
                            message = {"bid_result_data": render_bid_result.content}
                            json = simplejson.dumps(message)
                            return HttpResponse(json, mimetype='application/json')
                        else:
                            return HttpResponseRedirect("/products/" + str(idProduct) + "#error")
                    else:
                        return HttpResponseRedirect("/products/" + str(idProduct) + "#same")
                else:
                    return HttpResponseRedirect("/products/" + str(idProduct) + "#unavailable")
    else:
        return HttpResponse("/login")


#makeTrade: Maneja el intercambio de un producto con la oferta ingresada por otro usuario.
#            Debe recibir por POST el dato del id_bid elegido para hacer la oferta.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#         idProduct:    ID del producto que se está intercambiando.
#RETURN: Si el intercambio es factible y se realiza, retorna a la página del producto.
#         Si no se puede hacer el intercambio, retorna un mensaje de error con la posible causa.
def makeTrade(request, idProduct):
    if request.is_ajax() and request.method=="POST":
        if is_loged(request):
            data = {'id_dealer':request.session['member_id'],
                    'id_bid':request.POST['group_product'],
                    'code_dealer':id_generator(),
                    'code_bidder':id_generator(),
                    'pending_dealer':True,
                    'pending_bidder':True,
                    'datetime':datetime.now(),
                    'valid':False,
                    }
            tradeForm = TradeForm(data)
            if tradeForm.is_valid():
                tradeForm.save()
                product = Product.objects.get(id=idProduct)
                product.active = False
                product.save()
                bid = Bid.objects.get(id = request.POST['group_product'])
                bid.id_bid_product.active = False
                bidder = bid.id_bidder
                owner = product.id_owner
                savePendantProduct(request, idProduct, owner.id)
                savePendantProduct(request, idProduct, bidder.id)
                sendTradeMail(owner, bidder, tradeForm.cleaned_data['code_dealer'], tradeForm.cleaned_data['code_bidder'])
                user_dealer = User.objects.get(id = request.session['member_id'])
                bid = Bid.objects.get(id = request.POST['group_product'])
                user_bidder = bid.id_bidder
                message = {"middle_data": render_to_response('transaction_successful.html', 
                                                             {'middle':True,
                                                              'dealer': user_dealer,
                                                              'bidder': user_bidder}).content,
                           "right_data": render_to_response('transaction_successful.html', 
                                                            {'right':True,
                                                             'bid': bid
                                                             }).content
                           }
                json = simplejson.dumps(message)
                return HttpResponse(json, mimetype='application/json')
            else:
                return HttpResponseRedirect("/products/" + str(idProduct) + "#error")
        else:
            return HttpResponse("/login")
    else:
        return HttpResponseRedirect("/products/" + str(idProduct) + "#error")


#id_generator: Genera un codigo de 6 caracteres que se usa para confirmar el intercambio.
#PARAMS: size: tamaño del string deseado. Por default, su valor es 6.
#         chars: coleccion de caracteres desde los que se quiere extraer el codigo. Por default,
#                se usa el conjunto de letras ascii mayusculas y los digitos.    
#RETURN: Codigo de 'size' caracteres con valores aleatorios.
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))    


#showPending: Muestra las transacciones que el usuario aun no ha confirmado, ya sea como 'vendedor' o 'comprador'.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario. Contiene datos
#                  del usuario logueado.
#RETURN: render de la pagina con los datos de transacciones pendientes.
def showPending(request):
    if is_loged(request):
        dealer_pendings = Trade.objects.filter(id_dealer=request.session['member_id']).filter(pending_dealer=True)
        bidder_pendings = Trade.objects.filter(id_bid__id_bidder=request.session['member_id']).filter(pending_bidder=True)
        title = "Trueques pendientes"
        usuario = User.objects.get(id=request.session['member_id'])
        return render_to_response("pending.html", {'dealer_pendings':dealer_pendings, 'bidder_pendings':bidder_pendings, 'title':title, 'user':usuario})
    else:
        return HttpResponse("/login")


def verifyTrade(request, idTrade=None):
    if request.method == "POST":
        if is_loged(request):
            tradeVer = TradeVerification(request.POST)
            if tradeVer.is_valid():
                trade = Trade.objects.get(id=idTrade)
                if request.session['member_id']==trade.id_dealer.id:
                    if trade.code_dealer == tradeVer.cleaned_data['code']:
                        trade.pending_dealer = False
                        trade.save()
                        rate(trade.id_bid.id_bidder, tradeVer.cleaned_data['rate'])
                        if trade.pending_bidder==False:     #Los dos ya verificaron
                            exchange(trade.id_bid, trade.id_bid.id_product)
                            trade.valid=True
                            trade.save()
                            #Vuelve a mi nuevo producto recibido si existe, o si no a la busqueda (es el vendedor)
                            if trade.id_bid.bid_q == 0:
                                return HttpResponseRedirect("/" )
                            else:
                                return HttpResponseRedirect("/products/" + str(trade.id_bid.id_bid_product.id))
                        else:
                            return HttpResponse("FALTA VERIFICACION DEL COMPRADOR")
                    else:
                        return HttpResponse("CODIGO NO VALIDO")
                        
                elif request.session['member_id']==trade.id_bid.id_bidder.id:
                    if trade.code_bidder == tradeVer.cleaned_data['code']:
                        trade.pending_bidder = False
                        trade.save()
                        rate(trade.id_dealer, tradeVer.cleaned_data['rate'])
                        if trade.pending_dealer==False:      #Los dos ya verificaron
                            exchange(trade.id_bid, trade.id_bid.id_product)
                            trade.valid=True
                            trade.save()
                            
                            #Vuelve al producto adquirido (es el comprador)
                            return HttpResponseRedirect("/products/" + str(trade.id_bid.id_product.id))
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
            trade = Trade.objects.get(id = idTrade)
            bid = trade.id_bid
            
            if trade.id_dealer_id == request.session['member_id']:
                usuario = User.objects.get(id = bid.id_bidder_id)
                if bid.q != 0:
                    q = bid.q
                    product = None
                else:
                    q = 0
                    product = Product.objects.get(id = bid.id_bid_product_id)
                code = trade.code_dealer
            else:
                usuario = User.objects.get(id = trade.id_dealer_id)
                product = Product.objects.get(id = bid.id_product_id)
                q = 0
                code = trade.code_bidder
                
            message = {"verify_window": render_to_response("trade_verification.html", {'form':tradeVer,'id_trade':idTrade, 'user':usuario,'q':q,'product':product,'code':code}, context_instance=RequestContext(request)).content}
            json = simplejson.dumps(message)
            return HttpResponse(json, mimetype='application/json')
        else:
            return HttpResponse("/login")

#Funcion llamada para cambiar de Owner a un producto, y restar la cantidad de Q ofrecida
#en caso de "compra"
def exchange(bid, product):
    dealer = bid.id_dealer
    bidder = bid.id_bidder
    product.id_owner = bidder
    saveAlbumData(product, bidder)
    if bid.id_bid_product != None:            #Significa que fue un trueque por producto
        bid.id_bid_product.id_owner = dealer
        saveAlbumData(bid.id_bid_product, dealer)
    else:                                    #Significa que fue un trueque por Q
        dealer.profile.quds += bid.q
        bidder.profile.quds -= bid.q

#saveAlbumData:     Ingresa el registro de que el nuevo producto pertenece al album Trueques
#PARAMS: product:     Objecto producto recien guardado
#         idUser:    ID del usuario al que le pertenece el album y el producto
#RETURN: 
def saveAlbumData(producto, user):
    album = Album.objects.filter(id_owner=user).get(name='Trueques')
    albumProd = AlbumProduct()
    albumProd.id_album = album
    albumProd.id_product = producto
    albumProd.save()

#Funcion encargada de agregar la calificacion a un usuario
def rate(usuario, nota):
    cant = usuario.profile.ranking_qty
    prevNota = usuario.profile.rating
    usuario.profile.rating = (prevNota*cant + int(nota))/(cant + 1)
    usuario.profile.ranking_qty += 1
    usuario.save()


#Funcion encargada de enviar los correos con las claves de bidder y owner.
#Al owner se le envia la clave del bidder y viceversa.
def sendTradeMail(owner, bidder, code_dealer, code_bidder):
    #Mail para el propietario del producto
    dealer_msg = u"Usted ha realizado un nuevo trueque con el usuario " + bidder.first_name + " " + bidder.last_name + u".\nSu correo de contacto es " + bidder.email + u".\nAl realizar el intercambio final de tu producto, él debe entregarte un código de confirmación que debes usar para finalizar el trueque. Tú deberás entregarle el siguiente código para confirmar el trueque:\n" + code_bidder
#    send_mail('Confirmación de Trueque', dealer_msg , 'trueque@trueque.in', [owner.email], fail_silently=False)
    
    #Mail para el bidder
    bidder_msg = u"Usted ha realizado un nuevo trueque con el usuario " + owner.first_name + " " + owner.last_name + u".\nSu correo de contacto es " + owner.email + u".\nAl realizar el intercambio final de tu producto, él debe entregarte un código de confirmación que debes usar para finalizar el trueque. Tú deberás entregarle el siguiente código para confirmar el trueque:\n" + code_dealer
#    send_mail('Confirmación de Trueque', bidder_msg , 'trueque@trueque.in', [bidder.email], fail_silently=False)
