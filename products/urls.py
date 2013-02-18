from django.conf.urls.defaults import *

urlpatterns = patterns('products.views',
    url(r'^$', 'newProduct'),
    url(r'^(\d+)$', 'showDetails'),
    url(r'^save$', 'saveProduct'),
    url(r'^comment/(\d+)$', 'newComment'),
    url(r'^savecomment$', 'saveComment'),
)
