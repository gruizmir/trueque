# -*- coding: utf-8 -*-
from products.models import Product, Category, ProductCategory, Comment
from products.forms import ProductForm, CategoryForm, ImagesForm, CommentForm
from usuarios.models import Usuario, Country, City
from transactions.models import Bid
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.conf import settings
import uuid
import os

#Muestra el formulario para ingresar un nuevo producto, incluidas
#imagenes y categorias a las que pertenece.
def newProduct(request):
	image_form = ImagesForm(prefix='image')
	product_form = ProductForm(prefix='product')
	category_form = CategoryForm(prefix='category')
	return render_to_response("newproduct.html", {'image_form':image_form, 'product_form':product_form, 'category_form':category_form}, context_instance=RequestContext(request))

def saveProduct(request):
	if request.method == 'POST':
		product_form = ProductForm(request.POST, prefix='product')
		if product_form.is_valid():
			category_form = CategoryForm(data=request.POST, prefix='category')
			if category_form.is_valid():
				producto = saveProductData(product_form)
				saveCategoryData(producto, category_form)
				imageForm = ImagesForm(request.POST,request.FILES, prefix='image')
				print imageForm
				if imageForm.is_valid():
					saveImages(request, producto.product_img)
				else:
					return HttpResponse("no archivos")
				return HttpResponse("validado")
			else:			
				return HttpResponse("category_fail")
		else:			
			return HttpResponse("producto no valido")
	return HttpResponse("FAIL")

#Guarda los datos del producto en la base de datos.
def saveProductData(productForm):
	product = Product()
	product.product_name = productForm.cleaned_data['product_name']
	product.product_description = productForm.cleaned_data['product_description']
	product.product_q_amount = productForm.cleaned_data['product_q_amount']
	user = Usuario.objects.get(id_usuario=2)
	product.id_owner = user
	product.product_start_datetime = str(datetime.now())
	product.product_end_datetime = str(datetime.now())
	product.product_follower_qty = 0
	product.product_visit_qty = 0
	product.product_img = uuid.uuid1().hex
	product.product_active = 1
	product.save()
	return product


#Guarda el dato en la tabla Product_category, según las categorías
#seleccionadas ('on') en el formulario.
def saveCategoryData(producto, categoryForm):
	for i in range(1,13):
		if categoryForm.cleaned_data['field_'+str(i)]==True:
			proCat = ProductCategory()
			proCat.id_product = producto
			proCat.id_category = Category.objects.get(id_category=i)
			proCat.save()


#Busca la imagenes del request (formulario) correspondiente
#y las envia a guardar.
def saveImages(request, path=None):
	for i in range(1,6):
		print 'img_'+str(i)
		handle(path, request.FILES['image-img_'+str(i)], i)


#Guarda el archivo en la carpeta 'cargas' (MEDIA_ROOT)
#Falta agregar que la guarde en la carpeta propia del producto.
def handle(path, file, counter):
	if os.path.isdir(os.path.join(settings.MEDIA_ROOT, path)) == False:
		os.mkdir(os.path.join(settings.MEDIA_ROOT, path))
	if file:
		destination = open(settings.MEDIA_ROOT + "/" +path + "/" + "img_" + str(counter) + ".png", 'wb+')
		for chunk in file.chunks():
			destination.write(chunk)
		destination.close()

#Muestra los detalles del producto cuya ID es 'idProducto'.
#Debe enviar un mensaje si no lo encuentra o no se envia una ID.
def showDetails(request, idProduct=None):
	#Debe averiguar si el usuario es dueño o no.	
	if idProduct==None:
		return HttpResponseRedirect("/")
	else:
		try:
			producto = Product.objects.get(id_product=idProduct)
#			if producto.id_owner == request.session['member_id']:
#				showOwnerView(request, product)
#			else:				
#				showVisitView(request, product)
			return showVisitView(request, producto)
		except ObjectDoesNotExist:
			return HttpResponseRedirect("/")

#Debe mostrar opcion de aceptar una oferta.
def showOwnerView(request, product):
	owner = product.id_owner
	idProduct = product.id_product
	try:
		categories = ProductCategory.objects.get(id_product = idProduct)
	except ObjectDoesNotExist:
		categories = None
	try:
		coments = Comment.objects.get(id_product = idProduct).order_by('comment_datetime')
	except ObjectDoesNotExist:
		comments = None
	try:
		bids = Bid.objects.get(id_product = idProduct).order_by('bid_datetime')
	except ObjectDoesNotExist:
		bids = None
	return render_to_response("product_details.html", {'product':product, 'categories':categories, 'comments':comments, 'bids':bids, 'owner':owner}, context_instance=RequestContext(request))


#Muestra solo la opcion de hacer comentarios y hacer un Bid. Aumenta el contador de visitas.
def showVisitView(request, product):
	idProduct = product.id_product
	try:
		categories = ProductCategory.objects.filter(id_product = idProduct)
	except ObjectDoesNotExist:
		categories = None
	try:
		comments = Comment.objects.filter(id_product = idProduct).order_by('comment_datetime')
	except ObjectDoesNotExist:
		comments = None
	try:
		bids = Bid.objects.filter(id_product = idProduct).order_by('bid_datetime')
	except ObjectDoesNotExist:
		bids = None
	return render_to_response("product_details.html", {'product':product, 'categories':categories, 'comments':comments, 'bids':bids}, context_instance=RequestContext(request))


#Vista para dejar comentarios en un producto enviado por parametro
def newComment(request, idProduct=None):
#	comment = Comment(id_product=idProduct, id_sender=request.session['member_id'])
	producto = Product.objects.get(id_product=idProduct)
	sender = Usuario.objects.get(id_usuario=2)
	comment = Comment(id_product=producto, id_sender=sender)
	comment_form = CommentForm(instance=comment)
	return render_to_response("new_comment.html", {'form':comment_form},context_instance=RequestContext(request))


def saveComment(request):
	if request.method == "POST":
		comment_form = CommentForm(	request.POST)
		print comment_form
	return HttpResponseRedirect("/")
