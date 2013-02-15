from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
    url(r'^category/(\d*)$', 'searchByCategory'),
    url(r'^date/(\d*)$', 'searchByDate'),
    url(r'^price/(\d*)$', 'searchByPrice'),
    url(r'^popular/(\d*)$', 'searchByPopularity'),
)
