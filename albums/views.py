# -*- coding: utf-8 -*-
from albums.models import Album, AlbumProduct
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from products.models import Product

def showAlbums(request, idProduct=None):
	if request.user.is_authenticated() and request.is_ajax():
		albums = Album.objects.filter(id_owner = request.session['member_id']).exclude(name = "My Garage").exclude(name = "Trueques")
		product = Product.objects.get(id=idProduct)
		message = {"to_album_data": render_to_response("to_album.html", {'albums':albums, 'product':product}, context_instance=RequestContext(request)).content}
		
		json = simplejson.dumps(message)
		return HttpResponse(json, mimetype='application/json')
	else:
		return HttpResponse("USUARIO NO AUTENTICADO")

		
def saveAlbumData(request, idProduct=None):
	if request.user.is_authenticated():
		if request.method == "POST":
			try:
				albumValue = int(request.POST['albumValue'])
				album = Album.objects.filter(id_owner=request.session['member_id']).get(id=albumValue)
				producto = Product.objects.get(id = idProduct)
				albumProd = AlbumProduct()
				albumProd.id_album = album
				albumProd.id_product = producto
				albumProd.save()
				return HttpResponseRedirect("/products/" + str(idProduct))
			except:
				return HttpResponse("OPCION NO VALIDA")				
		else:
			return HttpResponse("NO ALLOWED")	
	else:
		return HttpResponse("USUARIO NO AUTENTICADO")

def savePendantProduct(request, idProduct=None, idUser=None):
	if request.user.is_authenticated() and idProduct!=None and idUser!=None:
		try:
			album = Album.objects.filter(id_owner=idUser).get(name="Pendientes")
			producto = Product.objects.get(id = idProduct)
			albumProd = AlbumProduct()
			albumProd.id_album = album
			albumProd.id_product = producto
			albumProd.save()
			return True
		except:
			return False
	else:
		return False
