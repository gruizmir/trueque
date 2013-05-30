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


#searchByCategory:   Muestra el formulario de busqueda por categorias (si no recibe formulario). Si recibe un formulario, 
#                    realiza la busqueda por categorias.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#        page:    pagina de resultados que se solicita. Se considera una pagina igual a 20 resultados.    
#RETURN: render de la pagina de busqueda usando SOLAMENTE filtro por categorias o el render de los resultados de la
#         busqueda.
def searchByCategory(request):
    return searchFilter(request)

def searchFilter(request, city=None, isCity=False, country=None, isCountry=False):
    try:
        if request.is_ajax():
            if request.method == 'POST':
                form = CategoryForm(request.POST)
                if form.is_valid():
                    data = None
                    prodCat = None
                    selected = False
                    try:
                        if form.cleaned_data['field_1']==True:
                            selected = True
                            prodCat = ProductCategory.objects.filter(id_category=1).values_list('id_product', flat=True)
                        if form.cleaned_data['field_2']==True:
                            selected = True
                            prodCat2 = ProductCategory.objects.filter(id_category=2).values_list('id_product', flat=True)
                            if prodCat!=None:
                                prodCat = intersect(prodCat,prodCat2)
                            else:
                                prodCat = prodCat2
                        if form.cleaned_data['field_3']==True:
                            selected = True
                            prodCat2 = ProductCategory.objects.filter(id_category=3).values_list('id_product', flat=True)
                            if prodCat!=None:
                                prodCat = intersect(prodCat,prodCat2)
                            else:
                                prodCat = prodCat2
                        if form.cleaned_data['field_4']==True:
                            selected = True
                            prodCat2 = ProductCategory.objects.filter(id_category=4).values_list('id_product', flat=True)
                            if prodCat!=None:
                                prodCat = intersect(prodCat,prodCat2)
                            else:
                                prodCat = prodCat2
                        if form.cleaned_data['field_5']==True:
                            selected = True
                            prodCat2 = ProductCategory.objects.filter(id_category=5).values_list('id_product', flat=True)
                            if prodCat!=None:
                                prodCat = intersect(prodCat,prodCat2)
                            else:
                                prodCat = prodCat2
                        if form.cleaned_data['field_6']==True:
                            selected = True
                            prodCat2 = ProductCategory.objects.filter(id_category=6).values_list('id_product', flat=True)
                            if prodCat!=None:
                                prodCat = intersect(prodCat,prodCat2)
                            else:
                                prodCat = prodCat2
                        if form.cleaned_data['field_7']==True:
                            selected = True
                            prodCat2 = ProductCategory.objects.filter(id_category=7).values_list('id_product', flat=True)
                            if prodCat!=None:
                                prodCat = intersect(prodCat,prodCat2)
                            else:
                                prodCat = prodCat2
                        if form.cleaned_data['field_8']==True:
                            selected = True
                            prodCat2 = ProductCategory.objects.filter(id_category=8).values_list('id_product', flat=True)
                            if prodCat!=None:
                                prodCat = intersect(prodCat,prodCat2)
                            else:
                                prodCat = prodCat2
                        if form.cleaned_data['field_9']==True:
                            selected = True
                            prodCat2 = ProductCategory.objects.filter(id_category=9).values_list('id_product', flat=True)
                            if prodCat!=None:
                                prodCat = intersect(prodCat,prodCat2)
                            else:
                                prodCat = prodCat2
                        if form.cleaned_data['field_10']==True:
                            selected = True
                            prodCat2 = ProductCategory.objects.filter(id_category=10).values_list('id_product', flat=True)
                            if prodCat!=None:
                                prodCat = intersect(prodCat,prodCat2)
                            else:
                                prodCat = prodCat2
                        if form.cleaned_data['field_11']==True:
                            selected = True
                            prodCat2 = ProductCategory.objects.filter(id_category=11).values_list('id_product', flat=True)
                            if prodCat!=None:
                                prodCat = intersect(prodCat,prodCat2)
                            else:
                                prodCat = prodCat2
                        if form.cleaned_data['field_12']==True:
                            selected = True
                            prodCat2 = ProductCategory.objects.filter(id_category=12).values_list('id_product', flat=True)
                            if prodCat!=None:
                                prodCat = intersect(prodCat,prodCat2)
                            else:
                                prodCat = prodCat2
                        if prodCat!=None:
                            if isCity:
                                data = Product.objects.filter(id_product__in=prodCat).filter(id_owner__usuario_city__city_name=city)
                            elif isCountry:
                                data = Product.objects.filter(id_product__in=prodCat).filter(id_owner__usuario_city__id_country__country_name=country)
                            else:
                                data = Product.objects.filter(id_product__in=prodCat)
                        else:
                            if selected==True:
                                data = None
                            else:
                                if isCity:
                                    data = Product.objects.filter(id_owner__usuario_city__city_name=city)
                                elif isCountry:
                                    data = Product.objects.filter(id_owner__usuario_city__id_country__country_name=country)
                                else:
                                    data = Product.objects.all()
                    except ObjectDoesNotExist:
                        data= None
                    user = None
                    if is_loged(request):
                        user = Usuario.objects.get(id_usuario=request.session['member_id'])
                    c = {'data':data, 'user':user}
                    c.update(csrf(request))
                    response = render_to_response("search.html", c)        
                else:
                    response = HttpResponse("NO VALID")
                message = {"products": response.content}
                json = simplejson.dumps(message)
                return HttpResponse(json, mimetype='application/json')
            else:
                return HttpResponseRedirect("/login")
        else:
            return HttpResponseRedirect("/register")
    except Exception as e:
        print e
        return HttpResponseRedirect("/products")

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
            data = Product.objects.filter(product_active=True).order_by('product_datetime').order_by('product_featured')[cant:20]
    except ObjectDoesNotExist:
        data = None
    user = None
    if is_loged(request):
        user = Usuario.objects.get(id_usuario=request.session['member_id'])
    return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT, 'user':user})


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

#intersect:    Intersecta dos listas comparando sus elementos (segun teoria de conjuntos)
#PARAMS: a,b: listas de datos que se van a comparar
#RETURN: Lista con los elementos en comun de las listas a y b.
def intersect(a, b):
    return list(set(a) & set(b))
    
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
