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

class ProductNotification:

	def bid_notification(self, idBidder, idProduct):
		bidder = Usuario.objects.get(id_usuario=idBidder)
		product = Product.objects.get(id_product=idProduct)
		nota = u"El usuario " + bidder.usuario_name + u" ha ingresado una oferta en tu " + product.product_name
		notif = Notification(id_user=product.id_owner, notification_message=nota, notification_pending=True, notification_datetime = str(datetime.now()), notification_link="/products/" + str(idProduct))
		notif.save()
		
		cantBids = Bid.objects.filter(id_product=idProduct).count()
		nota = str(cantBids) + u" personas quieren hacer trueque con tu " + product.product_name
		notif2 = Notification(id_user=product.id_owner, notification_message=nota, notification_pending=True, notification_datetime = str(datetime.now()), notification_link="/products/" + str(idProduct))
		notif2.save()
	
	def like_notification(self, idProduct):
		#debe buscar la ultima notificacion (si hay) que diga que "a tantas personas les gusta tu <nombre-producto>" y borrarla.
		product = Product.objects.get(id_product=idProduct)
		nota = u"A " + str(product.product_follower_qty) + u" personas les gusta tu " + product.product_name
		notif = Notification(id_user=product.id_owner, notification_message=nota, notification_pending=True, notification_datetime = str(datetime.now()), notification_link="/products/" + str(idProduct))
		notif.save()
	

class UserNotification:
	
	#Cuando se suma un seguidor
	def follower_notification(self, idFollowed):
		#debe buscar la ultima notificacion (si hay) que diga que "X personas te siguen ahora" del usuario y borrarla.
		user = Usuario.objects.get(id_usuario=idFollowed)
		nota = str(user.usuario_follower_qty) + u" personas te siguen ahora"
		notif = Notification(id_user=user, notification_message=nota, notification_pending=True, notification_datetime = str(datetime.now()), notification_link="/usuarios/" + str(idFollowed) + "/followers")
		notif.save()


class TradeNotification:

	#Falta agregar el link: deberia ir a la lista de trueques realizados.
	def trade_notification(self, idBidder, idUsuario):
		bidder = Usuario.objects.get(id_usuario=idBidder)
		user = Usuario.objects.get(id_usuario=idUsuario)
		nota = u"Felicidades, lograte un trueque con " + bidder.usuario_name + " " + bidder.usuario_lastname
		notif = Notification(id_user=user, notification_message=nota, notification_pending=True, notification_datetime = str(datetime.now()), notification_link="")
		notif.save()

