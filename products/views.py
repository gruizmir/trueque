# -*- coding: utf-8 -*-
from PIL import Image
from albums.models import Album, AlbumProduct
from datetime import datetime
from django.conf import settings
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from products.forms import ProductForm, CategoryForm, ImagesForm, CommentForm, \
    NewCommentForm
from products.models import Product, Category, ProductCategory, Comment
from transactions.models import Bid
from usuarios.models import Country, City
from django.contrib.auth.models import User
import os
import uuid


#newProduct:Muestra el formulario para ingresar un nuevo producto, incluidas imagenes 
#            y categorias a las que pertenece.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#RETURN: render de la pagina de ingreso de nuevo producto, con los tres formularios que ocupa
#         (imagenes, producto y categorias del producto)
def newProduct(request):
    if request.user.is_authenticated():
        imageForm = ImagesForm(prefix='image')
        productForm = ProductForm(prefix='product')
        categoryForm = CategoryForm(prefix='category')
        title = "Nuevo producto"
        usuario = request.user
        return render_to_response("newproduct.html", {'image_form':imageForm, 'product_form':productForm, 'category_form':categoryForm, 'title':title, 'user':usuario}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/login")


#saveProduct:     Guarda el producto que el usuario ingreso. Comprueba sesion del usuario, validez de los datos
#                y envias las cinco imagenes a su carpeta propia ubicada en MEDIA_ROOT.
#PARAMS: request:     Objeto que contiene toda la informacion enviada por el navegador del usuario.
#                    Incluye datos del usuario.        
#RETURN: Mensaje de confirmacion de ingreso, si es exitoso. Si el ingreso falla, devuelve un mensaje
#         con la causa del error.
def saveProduct(request):
    if request.method == 'POST' and request.user.is_authenticated():
        productForm = ProductForm(request.POST, prefix='product')
        if productForm.is_valid():
            category_form = CategoryForm(data=request.POST, prefix='category')
            if category_form.is_valid():
                producto = saveProductData(request, productForm)
                saveCategoryData(producto, category_form)
                imageForm = ImagesForm(request.POST,request.FILES, prefix='image')
                saveAlbumData(producto, request.user.id)
                if imageForm.is_valid():
                    saveImages(request, producto.img)
                else:
                    return HttpResponse("NO FILES")
                return HttpResponseRedirect("/products/" + str(producto.id))
            else:            
                return HttpResponse("CATEGORY FAIL")
        else:            
            return HttpResponse("INVALID PRODUCT")
    return HttpResponse("FAIL")


#saveProductData:     Ingresa los datos de usuario, fecha y del nuevo producto en un objeto y lo guarda en la BD.
#PARAMS: request:     Objeto que contiene toda la informacion enviada por el navegador del usuario.
#                    Incluye datos del usuario.        
#         productForm:    Formulario enviado por el usuarios, con los datos del objeto a ingresar.
#RETURN: Nuevo objeto Product creado.
def saveProductData(request, productForm):
    product = Product()
    product.name = productForm.cleaned_data['name']
    product.description = productForm.cleaned_data['description']
    product.q_amount = productForm.cleaned_data['q_amount']
    user = request.user
    product.id_owner = user
    product.start_datetime = str(datetime.now())
    product.end_datetime = str(datetime.now())
    product.follower_qty = 0
    product.visit_qty = 0
    product.img = uuid.uuid1().hex
    product.featured_time = 0;
    product.active = 1
    product.save()
    return product

#saveAlbumData:     Ingresa el registro de que el nuevo producto pertenece al album Garage
#PARAMS: product:     Objecto producto recien guardado
#         idUser:    ID del usuario al que le pertenece el album y el producto
#RETURN: 
def saveAlbumData(producto, idUser):
    album = Album.objects.filter(id_owner=idUser).get(name='My Garage')
    albumProd = AlbumProduct(id_album=album, id_product=producto)
    albumProd.save()

#saveCategoryData:     Guarda el dato en la tabla Product_category, según las categorías seleccionadas
#                    ('on') en el formulario.
#PARAMS: producto: Objeto Product que se está guardando.
#         categoryForm: Formulario con las elecciones del usuario para las categorías del producto.
#RETURN: 
def saveCategoryData(producto, categoryForm):
    for i in range(1,13):
        if categoryForm.cleaned_data['field_'+str(i)]==True:
            proCat = ProductCategory()
            proCat.id_product = producto
            proCat.id_category = Category.objects.get(id=i)
            proCat.save()


#saveImages: Busca la imagenes del request enviadas por POST y las envia a guardar.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#                  Incluye datos del usuario.
#         path: Dirección del servidor donde se guardaran los archivos. Se genera mediante HASH.
#RETURN: 
def saveImages(request, path=None):
    for i in range(1,6):
        try:
            handle(path, request.FILES['image-img_'+str(i)], i)
        except:
            break


#handle: Guarda el archivo en la carpeta 'cargas' (MEDIA_ROOT), dentro de la carpeta en 'path'
#PARAMS: path: Dirección del servidor donde se guardaran los archivos. Se genera mediante HASH.
#         file: Archivo que se va a guardar
#         counter: Integer que muestra cual es el orden en que se esta guardando este archivo. Se 
#                    usa para darle nombre a la imagen.
#RETURN: 
def handle(path, file, counter):
    if os.path.isdir(os.path.join(settings.MEDIA_ROOT, path)) == False:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, path))
    if file:
        filename = settings.MEDIA_ROOT + "/" +path + "/" + "img_" + str(counter) + ".png"
        destination = open(filename, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        resize(filename, counter)


def resize(filename, counter):
    img = Image.open(filename)
    width, height = img.size
    if width>=height:
        nWidth = 60
        nHeight = 60*height/width
        mWidth = 128
        mHeight = 128*height/width
    else:
        nHeight = 60
        nWidth = 60*width/height
        mHeight = 128
        mWidth = 128*width/height
    thumb1 = img.resize((nWidth, nHeight), Image.ANTIALIAS)
    thumb2 = img.resize((mWidth, mHeight), Image.ANTIALIAS)
    thumb1.save(filename.replace(".png", "_small.png"))
    thumb2.save(filename.replace(".png", "_medium.png"))


#showDetails: Muestra los detalles del producto cuya ID es 'idProducto'. Comprueba que vista debe enviar
#              segun si el usuario esta logueado o no, y si es dueño del producto o no.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#                  Incluye datos del usuario.
#         idProduct: ID del producto a buscar. Integer.
#RETURN: 
def showDetails(request, idProduct=None):
    #Debe averiguar si el usuario es dueño o no.
    if idProduct==None:
        return HttpResponseRedirect("/")
    else:
        try:
            producto = Product.objects.get(id=idProduct)
            if request.user.is_authenticated() and producto.id_owner == request.user:
                return showOwnerView(request, producto)
            else:                
                return showVisitView(request, producto)
        except ObjectDoesNotExist:
            return HttpResponseRedirect("/")


#showOwnerView: Muestra los detalles del producto para el dueño de éste. Incluye los Bids y los 
#                  Comentarios de otros usuarios.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#                  Incluye datos del usuario.
#         product: Objeto Product que se va a mostrar.
#RETURN: render de la vista de productos para usuario.
def showOwnerView(request, product):
    owner = product.id_owner
    idProduct = product.id
    try:
        categories = ProductCategory.objects.filter(id_product = idProduct)
    except ObjectDoesNotExist:
        categories = None
    try:
        comments = Comment.objects.filter(id_product = idProduct).order_by('datetime')
    except ObjectDoesNotExist:
        comments = None
    try:
        bids = Bid.objects.filter(id_product = idProduct).order_by('datetime')
    except ObjectDoesNotExist:
        bids = None    
    title = product.name
    return render_to_response("owner_product_details.html", {'product':product, 'categories':categories, 'comments':comments, 'bids':bids, 'title':title, 'user':owner}, context_instance=RequestContext(request))


#showVisitView: Muestra los detalles del producto sin detalles de usuario. Incluye los Bids y los 
#                  Comentarios de otros usuarios, con posibilidad de hacer un nuevo Bid o Comment.
#                Aumenta el contador de visitas del producto.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#                  Incluye datos del usuario.
#         product: Objeto Product que se va a mostrar.
#RETURN: render de la vista de productos para usuarios no dueño del producto.
def showVisitView(request, product):
    idProduct = product.id
    try:
        categories = ProductCategory.objects.filter(id_product = idProduct)
    except ObjectDoesNotExist:
        categories = None
    try:
        comments = Comment.objects.filter(id_product = idProduct).order_by('datetime')
    except ObjectDoesNotExist:
        comments = None
    try:
        bids = Bid.objects.filter(id_product = idProduct).order_by('datetime')
    except ObjectDoesNotExist:
        bids = None
    title = product.name
    usuario = None
    if request.user.is_authenticated():
        usuario = request.user
    return render_to_response("product_details.html", {'product':product, 'categories':categories, 'comments':comments, 'bids':bids, 'title':title, 'user':usuario}, context_instance=RequestContext(request))

#newComment:Muestra el formulario para ingresar nuevos comentarios en un producto y procesa y guarda 
#            los comentarios nuevos.
#PARAMS: request: Objeto que contiene toda la informacion enviada por el navegador del usuario.
#                  Incluye datos del usuario.
#         idProduct: ID del producto al que se le hace el comentario.
#RETURN: Si no se ha enviado formulario con mensaje, muestra la vista de ingresar nuevo mensaje.
#         Si el mensaje se guarda exitosamente, muestra la vista del producto.
#         Si no se guarda, muestra un mensaje de error con la posible causa.
def newComment(request, idProducto=None):
    if request.user.is_authenticated():
        if idProducto!=None:
            if request.method == "POST":
                newComment = NewCommentForm(request.POST)
                if newComment.is_valid():
                    try:
                        data = {'id_product':idProducto,
                                'id_sender':request.user.id,
                                'subject':newComment.cleaned_data['subject'],
                                'text':newComment.cleaned_data['text'],
                                'datetime': datetime.now(),
                                }    
                        commentForm = CommentForm(data)
                        if commentForm.is_valid():
                            commentForm.save()
                            user = request.user
   #                         send_mail('Comentario enviado', 'Usted hizo un nuevo comentario.', settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
                            return HttpResponseRedirect("/products/" + str(idProducto))
                        else:
                            return HttpResponse("DATA_ERROR")
                    except Exception as e:
                        print e
                        return HttpResponseRedirect("/products/" + str(idProducto))                            
                else:
                    return HttpResponse("NO_VALID")        
            elif request.is_ajax():
                newComment = NewCommentForm()
                product = Product.objects.get(id=idProducto)
                title = "Nuevo comentario para " + product.name
                user = request.user
                message = {"add_comment_data": render_to_response("new_comment.html", {'form':newComment, 'title':title, 'user':user, 'idproducto':idProducto},context_instance=RequestContext(request)).content}
                json = simplejson.dumps(message)
                return HttpResponse(json, mimetype='application/json')
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponse("/login")
