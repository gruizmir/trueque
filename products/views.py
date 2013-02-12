# -*- coding: utf-8 -*-
from products.models import Product, Category, ProductCategory
from django.shortcuts import render_to_response
from products.forms import ProductForm, CategoryForm, ImagesForm
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from usuarios.models import Usuario, Country, City
from datetime import datetime
from django.conf import settings

def newProduct(request):
	image_form = ImagesForm(prefix='image')
	product_form = ProductForm(prefix='product')
	category_form = CategoryForm(prefix='category')
#	return render_to_response("newproduct.html", {'product_form':product_form, 'category_form':category_form},context_instance=RequestContext(request))
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
					saveImages(request)
				else:
					return HttpResponse("no archivos")
				return HttpResponse("validado")
			else:			
				return HttpResponse("category_fail")
		else:			
			return HttpResponse("producto no valido")
	return HttpResponse("FAIL")

def saveProductData(productForm):
	product = Product()
	product.product_name = productForm.cleaned_data['product_name']
	product.product_description = productForm.cleaned_data['product_description']
	product.product_q_amount = productForm.cleaned_data['product_q_amount']
	user = Usuario.objects.get(id_usuario=2)
	product.id_owner = user
	product.product_datetime = str(datetime.now())
	product.product_follower_qty = 0
	product.product_visit_qty = 0
	product.save()
	return product

def saveCategoryData(producto, categoryForm):
	for i in range(1,13):
		if categoryForm.cleaned_data['field_'+str(i)]==True:
			proCat = ProductCategory()
			proCat.id_product = producto
			proCat.id_category = Category.objects.get(id_category=i)
			proCat.save()

def saveImages(request):
	for i in range(1,6):
		print 'img_'+str(i)
		handle(request.FILES['image-img_'+str(i)])


def handle(file):
	if file:
		destination = open(settings.MEDIA_ROOT + "/" +file.name, 'wb+')
		for chunk in file.chunks():
			destination.write(chunk)
		destination.close()
