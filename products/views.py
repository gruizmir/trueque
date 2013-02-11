# -*- coding: utf-8 -*-
from products.models import Product, Category, ProductCategory
from django.shortcuts import render_to_response
from products.forms import ProductForm, CategoryForm, ImagesForm
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

def newProduct(request):
#	image_form = ImagesForm()
	product_form = ProductForm(prefix='product')
	category_form = CategoryForm(prefix='category')
	return render_to_response("newproduct.html", {'product_form':product_form, 'category_form':category_form},context_instance=RequestContext(request))
#	return render_to_response("newproduct.html", {'image_form':image_form, 'product_form':product_form, 'category_form':category_form},context_instance=RequestContext(request))

def saveProduct(request):
	if request.method == 'POST':
		product_form = ProductForm(request.POST, prefix='product')
		if product_form.is_valid():
			category_form = CategoryForm(data=request.POST, prefix='category')
			if category_form.is_valid():
				id_producto = saveProductData(product_form)
				saveCategoryData(id_producto, category_form)
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
	product.id_owner = 1
	return 1

def saveCategoryData(idProduct, categoryForm):
	for i in range(1,12):
		if categoryForm.cleaned_data['field'+str(i)]=='on'
			proCat = ProductCategory()
			proCat.id_product = idProduct;
			proCat.id_category = i
			proCat.save()
