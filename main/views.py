# -*- coding: utf-8 -*-
from products.models import Product, Category, ProductCategory
from main.models import ProductFollower, Comment
from usuarios.models import Usuario, Country, City
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

#Search always keep featured elements first.

def searchByCategory(request, page=None):
	return HttpResponseRender("/")
	#usar aggregate(Count('id_product'))
#	data = None
#	try:
#		if page==None:
#			data = Product.objects.filter('product_active'=True).order_by('product_datetime').order_by('featured')[:20]
#		else:
#			data = Product.objects.filter('product_active'=True).order_by('product_datetime').order_by('featured')[20*(page-1):20]
#	except ObjectDoesNotExists:
#		data = None
#	return render_to_response("search.html", {'data':data})

def searchByDate(request, page=None):
	data = None
	try:
		if page==None or page=="":
			data = Product.objects.filter(product_active=True).order_by('product_datetime').order_by('product_featured')[:20]
		else:
			cant = 20*(int(page) - 1)
			data = Product.objects.filter(product_active=True).order_by('product_datetime').order_by('product_featured')[cant:20]
	except ObjectDoesNotExist:
		data = None
	return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT})

def searchByPrice(request, page=None):
	data = None
	try:
		if page==None or page=="":
			data = Product.objects.filter(product_active=True).order_by('product_q_amount').order_by('product_featured')[:20]
		else:
			cant = 20*(int(page) - 1)
			data = Product.objects.filter(product_active=True).order_by('product_q_amount').order_by('product_featured')[cant:20]
	except ObjectDoesNotExist:
		data = None
	return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT})

def searchByPopularity(request, page=None):
	data = None
	try:
		if page==None or page=="":
			data = Product.objects.filter(product_active=True).order_by('product_follower_qty').order_by('product_featured')[:20]
		else:
			cant = 20*(int(page) - 1)
			data = Product.objects.filter(product_active=True).order_by('product_follower_qty').order_by('product_featured')[cant:20]
	except ObjectDoesNotExist:
		data = None
	return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT})
	
def searchByName(request,page=None):
	data = None
	if request.method == 'POST':
		try:
			if page==None or page=="":
				data = Product.objects.filter(product_name__icontains=request.POST['search_data']).order_by('product_featured')[:20]
			else:
				cant = 20*(int(page) - 1)
				data = Product.objects.filter(product_name__icontains=request.POST['search_data']).order_by('product_featured')[cant:20]
		except ObjectDoesNotExist:
			data = None
	else:
		return HttpResponseRedirect("/")
	return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT})
