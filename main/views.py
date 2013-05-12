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

#searchByCategory:   Muestra el formulario de busqueda por categorias (si no recibe formulario). Si recibe un formulario, 
#                    realiza la busqueda por categorias.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#        page:    pagina de resultados que se solicita. Se considera una pagina igual a 20 resultados.    
#RETURN: render de la pagina de busqueda usando SOLAMENTE filtro por categorias o el render de los resultados de la
#         busqueda.
def searchByCategory(request, page=None):
    try:
        if request.is_ajax():
            print "es ajax"
            if request.method == 'POST':
                print "es post"
                form = CategoryForm(request.POST)
                if form.is_valid():
                    print "es valido"
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
                    if is_loged(request):
                        user = Usuario.objects.get(id_usuario=request.session['member_id'])
                        c = {'data':data, 'user':user}
                        c.update(csrf(request))
                    else:
                        c = {'data':data}
                        c.update(csrf(request))
                    response = render_to_response("search.html", c)        
                else:
                    print "no es valido"
                    response = HttpResponse("NO VALID")
                message = {"products": response.content}
                json = simplejson.dumps(message)
                return HttpResponse(json, mimetype='application/json')
            else:
                print "No es post"
                return HttpResponseRedirect("/login")
        else:
            return HttpResponseRedirect("/register")
    except Exception as e:
        return HttpResponseRedirect("/login")

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
    if is_loged(request):
        user = Usuario.objects.get(id_usuario=request.session['member_id'])
        return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT, 'user':user})
    else:
        return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT})


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
    if is_loged(request):
        user = Usuario.objects.get(id_usuario=request.session['member_id'])
        return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT, 'user':user})
    else:
        return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT})


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
    if is_loged(request):
        user = Usuario.objects.get(id_usuario=request.session['member_id'])
        return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT, 'user':user})
    else:
        return render_to_response("search.html", {'data':data, 'direccion':settings.MEDIA_ROOT})

#intersect:    Intersecta dos listas comparando sus elementos (segun teoria de conjuntos)
#PARAMS: a,b: listas de datos que se van a comparar
#RETURN: Lista con los elementos en comun de las listas a y b.
def intersect(a, b):
    return list(set(a) & set(b))

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
    if is_loged(request):
        user = Usuario.objects.get(id_usuario=request.session['member_id'])
        return render_to_response("main.html", {'form':form, 'user':user, 'data':data,'direccion':settings.MEDIA_ROOT}, context_instance=RequestContext(request))
    else:
        return render_to_response("main.html", {'form':form, 'data':data, 'direccion':settings.MEDIA_ROOT}, context_instance=RequestContext(request))
