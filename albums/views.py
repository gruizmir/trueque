# -*- coding: utf-8 -*-
from products.models import Product
from albums.models import Album, AlbumProduct
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from usuarios.views import is_loged

def showAlbums(request, idProduct=None):
	if is_loged(request):
		albums = Album.objects.filter(id_owner = request.session['member_id']).exclude(album_name = "My Garage").exclude(album_name = "Trueques")
		product = Product.objects.get(id_product=idProduct)
		return render_to_response("to_album.html", {'albums':albums, 'product':product}, context_instance=RequestContext(request))
	else:
		return HttpResponse("USUARIO NO AUTENTICADO")

		
def saveAlbumData(request, idProduct=None):
	if is_loged(request):
		if request.method == "POST":
			try:
				album_value = int(request.POST['album_value'])
				album = Album.objects.filter(id_owner=request.session['member_id']).get(id_album=album_value)
				producto = Product.objects.get(id_product = idProduct)
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
