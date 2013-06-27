# -*- coding: utf-8 -*-
from albums.models import Album, AlbumProduct
from products.models import Product

#get_albums: Obtiene los albums de un usuario
#PARAMS: user : Usuario del cual se quiere obtener los albums
#RETURN: Lista de Albums (objetos) que posea el usuario.
def get_albums(user):
    try:
        return Album.objects.filter(id_owner = user)
    except Exception:
        raise Exception("albums.get_albums : Can't get albums")

#get_album: Obtiene un album del usuario en base al nombre del album.
#PARAMS: user : Usuario del cual se quiere obtener el album
#        name_album : Nombre del album que se quiere recuperar
#RETURN: Album (objeto) que se quiere recuperar.
def get_album(user, name_album):
    try:
        return Album.objects.filter(id_owner = user, name = name_album)
    except Exception:
        raise Exception("albums.get_album : Can't get album")
    
def get_products_by_id_album(id_album):
    try:
        album = AlbumProduct.objects.filter(id_album_id = id_album)
        return Product.objects.filter(id__in = [product.id_product_id for product in album])
    except Exception:
        raise Exception("albums.get_products_by_id_album : Can't get products")
    
#add_album: Se guarda un album en la db del usuario entregado por parametro, adicionalmente
#           se debe añadir el nombre del album, si es que se puede editar o no y si se quiere
#           forzar la insercion en la db.
#PARAMS : user : Usuario al cual se le quiere añadir un album
#         name_album: Nombre del album a añadir.
#         can_edit: True / False dependiendo si se le quiere dar permiso de edicion al usuario.
#         force: True / False dependiendo si se quiere forzar la insercion en la db
#RETURN: True si se logro la incersion en la db o False si no se logro.
def add_album(user, album_name, can_edit, force):
    try:
        if not get_album(user, album_name):
            new_album = Album()
            new_album.set_album(user, album_name, can_edit)
            new_album.save(force_insert=force)
            return True
        return False
    except Exception:
        raise Exception("albums.add_album : Can't add album")
