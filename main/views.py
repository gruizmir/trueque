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
from usuarios.views import is_loged
from django.utils import simplejson
from main.util import searchFilter

#Search always keep featured elements first.

def searchByCountry(request, country=None):
    if country!=None:
        return searchFilter(request,country=country, isCountry=True)
    else:
        return searchByCategory(request)

def searchByCity(request, city=None):
    if city!=None:
        return searchFilter(request,city=city, isCity=True)
    else:
        return searchByCategory(request)

def searchByCategory(request):
    return searchFilter(request)

def getCountries(request):
    countries = Country.objects.all()
    response = render_to_response("countries.html", {'countries':countries})     
    message = {"countries": response.content}
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')

def getCities(request, country=None):
    if country==None:
        cities = None
    else:
        cities = City.objects.filter(id_country__country_name=country)
    response = render_to_response("cities.html", {'cities':cities})     
    message = {"cities": response.content}
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')
    
def search(request, page=None):
    data = None
    try:
        if page==None or page=="":
            data = Product.objects.filter(product_active=True).order_by('product_q_amount').order_by('product_featured')[:20]
        else:
            cant = 20*(int(page) - 1)
            data = Product.objects.filter(product_active=True).order_by('product_q_amount').order_by('product_featured')[cant:20]
    except ObjectDoesNotExist:
        data = None
    form = CategoryForm()
    user = None
    if is_loged(request):
        user = Usuario.objects.get(id_usuario=request.session['member_id'])
    return render_to_response("main.html", {'form':form, 'user':user, 'data':data,'direccion':settings.MEDIA_ROOT}, context_instance=RequestContext(request))


def about(request):
    user = None
    if is_loged(request):
        user = Usuario.objects.get(id_usuario=request.session['member_id'])
    return render_to_response('about.html', {'about':True, 'user':user})
    
    
    
#================================================================================================================


#searchByPrice:    Realiza una busqueda normal de productos ordenador por precio. Muestra primero los 
#                destacados ('featured')
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#         page:    pagina de resultados que se solicita. Se considera una pagina igual a 20 resultados.    
#RETURN: render de los resultados de la busqueda ordenados.
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
    if is_loged(request):
        user = Usuario.objects.get(id_usuario=request.session['member_id'])
        return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT, 'user':user})        
    else:
        return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT})        


#searchByPopularity:Realiza una busqueda normal de productos ordenador por fecha. Muestra primero los 
#                    destacados ('featured')
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#         page:    pagina de resultados que se solicita. Se considera una pagina igual a 20 resultados.    
#RETURN: render de los resultados de la busqueda ordenados.
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
    user = None
    if is_loged(request):
        user = Usuario.objects.get(id_usuario=request.session['member_id'])
    return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT, 'user':user})


#searchByName:    Realiza una busqueda normal de productos segun nombre. Muestra primero los 
#                destacados ('featured').
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#         page:    pagina de resultados que se solicita. Se considera una pagina igual a 20 resultados.    
#RETURN: render de los resultados de la busqueda ordenados.    
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
    user = None
    if is_loged(request):
        user = Usuario.objects.get(id_usuario=request.session['member_id'])
    return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT, 'user':user})


#searchByDate:    Realiza una busqueda normal de productos ordenador por fecha. Muestra primero los 
#                destacados ('featured')
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#         page:    pagina de resultados que se solicita. Se considera una pagina igual a 20 resultados.    
#RETURN: render de los resultados de la busqueda ordenados.
def searchByDate(request, page=None):
    data = None
    try:
        if page==None or page=="":
            data = Product.objects.filter(product_active=True).order_by('product_datetime').order_by('product_featured')[:20]
        else:
            cant = 20*(int(page) - 1)
            data = Product.objects.filter(product_active=True).order_by('product_start_datetime').order_by('product_featured')[cant:20]
    except ObjectDoesNotExist:
        data = None
    user = None
    if is_loged(request):
        user = Usuario.objects.get(id_usuario=request.session['member_id'])
    return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT, 'user':user})    
