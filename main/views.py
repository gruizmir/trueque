# -*- coding: utf-8 -*-
from products.models import Product, Category, ProductCategory
from main.models import ProductFollower
from products.forms import CategoryForm
from usuarios.models import Usuario, Country, City
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

#Search always keep featured elements first.

def showCategories(request):
	form = CategoryForm()
	return render_to_response("main.html", {'form':form}, context_instance=RequestContext(request))

def searchByCategory(request, page=None):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			data = None
			prodCat = None
			try:
				if form.cleaned_data['field_1']==True:
					prodCat = ProductCategory.objects.filter(id_category=1).values_list('id_product', flat=True)
				if form.cleaned_data['field_2']==True:
					prodCat2 = ProductCategory.objects.filter(id_category=2).values_list('id_product', flat=True)
					if prodCat!=None:
						prodCat = intersect(prodCat,prodCat2)
					else:
						prodCat = prodCat2
				if form.cleaned_data['field_3']==True:
					prodCat2 = ProductCategory.objects.filter(id_category=3).values_list('id_product', flat=True)
					if prodCat!=None:
						prodCat = intersect(prodCat,prodCat2)
					else:
						prodCat = prodCat2
				if form.cleaned_data['field_4']==True:
					prodCat2 = ProductCategory.objects.filter(id_category=4).values_list('id_product', flat=True)
					if prodCat!=None:
						prodCat = intersect(prodCat,prodCat2)
					else:
						prodCat = prodCat2
				if form.cleaned_data['field_5']==True:
					prodCat2 = ProductCategory.objects.filter(id_category=5).values_list('id_product', flat=True)
					if prodCat!=None:
						prodCat = intersect(prodCat,prodCat2)
					else:
						prodCat = prodCat2
				if form.cleaned_data['field_6']==True:
					prodCat2 = ProductCategory.objects.filter(id_category=6).values_list('id_product', flat=True)
					if prodCat!=None:
						prodCat = intersect(prodCat,prodCat2)
					else:
						prodCat = prodCat2
				if form.cleaned_data['field_7']==True:
					prodCat2 = ProductCategory.objects.filter(id_category=7).values_list('id_product', flat=True)
					if prodCat!=None:
						prodCat = intersect(prodCat,prodCat2)
					else:
						prodCat = prodCat2
				if form.cleaned_data['field_8']==True:
					prodCat2 = ProductCategory.objects.filter(id_category=8).values_list('id_product', flat=True)
					if prodCat!=None:
						prodCat = intersect(prodCat,prodCat2)
					else:
						prodCat = prodCat2
				if form.cleaned_data['field_9']==True:
					prodCat2 = ProductCategory.objects.filter(id_category=9).values_list('id_product', flat=True)
					if prodCat!=None:
						prodCat = intersect(prodCat,prodCat2)
					else:
						prodCat = prodCat2
				if form.cleaned_data['field_10']==True:
					prodCat2 = ProductCategory.objects.filter(id_category=10).values_list('id_product', flat=True)
					if prodCat!=None:
						prodCat = intersect(prodCat,prodCat2)
					else:
						prodCat = prodCat2
				if form.cleaned_data['field_11']==True:
					prodCat2 = ProductCategory.objects.filter(id_category=11).values_list('id_product', flat=True)
					if prodCat!=None:
						prodCat = intersect(prodCat,prodCat2)
					else:
						prodCat = prodCat2
				if form.cleaned_data['field_12']==True:
					prodCat2 = ProductCategory.objects.filter(id_category=12).values_list('id_product', flat=True)
					if prodCat!=None:
						prodCat = intersect(prodCat,prodCat2)
					else:
						prodCat = prodCat2
				if prodCat!=None:
					data = Product.objects.filter(id_product__in=prodCat)
				else:
					data = None
			except ObjectDoesNotExist:
				data= None
			return render_to_response("search.html", {'data':data})		
				
		else:
			return HttpResponse("NO VALID")
	else:
		return HttpResponseRedirect("/")

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

#return the intersection of two lists
def intersect(a, b):
    return list(set(a) & set(b))
