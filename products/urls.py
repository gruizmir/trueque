from django.conf.urls.defaults import *

urlpatterns = patterns('products.views',
    url(r'^$', 'newProduct'),
    url(r'^save$', 'saveProduct'),
    url(r'^details/(\d*)$', 'showDetails'),
)
