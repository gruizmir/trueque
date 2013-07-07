import albums.utils as albums_utils
from django import template
register = template.Library()

@register.filter('last_img')
def last_img(album):
    products = albums_utils.get_products_by_id_album(album.id)
    if products.count() != 0:
        products = products[::-1]
        return products[0].img
    else:
        return None
    
@register.filter('last_4_product')
def last_4_img(album):
    products = albums_utils.get_products_by_id_album(album.id)
    if products.count() != 0:
        products = products[::-1]
        return products[0:3]
    else:
        return []