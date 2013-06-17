# -*- coding: utf-8 -*-
from products.models import Product, Category, ProductCategory, Comment
from products.forms import ProductForm, CategoryForm, ImagesForm, CommentForm, NewCommentForm
from usuarios.models import Usuario, Country, City
from usuarios.views import is_loged
from transactions.models import Bid
from albums.models import Album, AlbumProduct
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.conf import settings
import uuid
import os

# TIPOS DE NOTIFICACION
# message :	Mensajes (correo interno) de usuarios
# bid :		Ofertas en un nuevo producto
# like :	A una persona le gusta tu producto
# follow :	Una persona te sigue
# trade :	Intercambio completado


class ProductNotification:

	def bid_notification(self, idBidder, idProduct):
		bidder = Usuario.objects.get(id=idBidder)
		product = Product.objects.get(id=idProduct)
		nota = u"El usuario " + bidder.first_name + u" ha ingresado una oferta en tu " + product.product_name
		notif = Notification(id_user=product.id_owner, message=nota, pending=True, datetime = str(datetime.now()), link="/products/" + str(idProduct), ntype="bid")
		notif.save()
		
		
		try:
			prevNotif = Notification.objects.get(id_user=product.id_owner, ntype="bid", message__contains=u"personas quieren hacer trueque con tu " + product.product_name)
			prevNotif.delete()
			nota = str(cantBids) + u" personas quieren hacer trueque con tu " + product.product_name
		except:
			nota = str(cantBids) + u" persona quiere hacer trueque con tu " + product.product_name
			
			
		cantBids = Bid.objects.filter(id_product=idProduct).count()
		nota = str(cantBids) + u" personas quieren hacer trueque con tu " + product.product_name
		notif2 = Notification(id_user=product.id_owner, message=nota, pending=True, datetime = str(datetime.now()), link="/products/" + str(idProduct), ntype="bid")
		notif2.save()
	
	def like_notification(self, idProduct):
		product = Product.objects.get(id=idProduct)
		try:
			prevNotif = Notification.objects.get(id_user=product.id_owner, ntype="like", message__contains=u"personas les gusta tu " + product.product_name)
			prevNotif.delete()
			nota = u"A " + str(product.product_follower_qty) + u" personas les gusta tu " + product.product_name
		except:
			nota = u"A " + str(product.product_follower_qty) + u" persona le gusta tu " + product.product_name
		notif = Notification(id_user=product.id_owner, message=nota, pending=True, datetime = str(datetime.now()), link="/products/" + str(idProduct), ntype="like")
		notif.save()
	

class UserNotification:
	
	#Cuando se suma un seguidor
	def follower_notification(self, idFollowed):
		#debe buscar la ultima notificacion (si hay) que diga que "X personas te siguen ahora" del usuario y borrarla.
		user = Usuario.objects.get(id=idFollowed)
		try:
			prevNotif = Notification.objects.get(id_user=user, ntype="follow", message__contains=u"personas te siguen ahora")
			prevNotif.delete()
			nota = str(user.follower_qty) + u" personas te siguen ahora"
		except:
			nota = str(user.follower_qty) + u" persona te sigue ahora"
		nota = str(user.follower_qty) + u" personas te siguen ahora"
		notif = Notification(id_user=user, message=nota, pending=True, datetime = str(datetime.now()), link="/usuarios/" + str(idFollowed) + "/followers", ntype="follow")
		notif.save()


class TradeNotification:

	#Falta agregar el link: deberia ir a la lista de trueques realizados.
	def trade_notification(self, idBidder, idUsuario):
		bidder = Usuario.objects.get(id=idBidder)
		user = Usuario.objects.get(id=idUsuario)
		nota = u"Felicidades, lograste un trueque con " + bidder.first_name + " " + bidder.last_name
		notif = Notification(id_user=user, message=nota, pending=True, datetime = str(datetime.now()), link="", ntype="trade")
		notif.save()

class MessageNotification:
	
	#Recibe la id del usuario que le envio el mensaje
	#Falta agregar el link
	def message_notification(self, idUsuario):
		user = Usuario.objects.get(id=idUsuario)
		nota = user.first_name + u" te ha enviado un mensaje"
		notif = Notification(id_user=user, message=nota, pending=True, datetime = str(datetime.now()), link="", ntype="message")
		notif.save()
