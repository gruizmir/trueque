from django.conf.urls.defaults import *

urlpatterns = patterns('main.views',
	url(r'^$', 'searchByCategory'),
	url(r'^category/(\w*)$', 'searchByCategory'),
    url(r'^date/(\d*)$', 'searchByDate'),
    url(r'^price/(\d*)$', 'searchByPrice'),
    url(r'^popular/(\d*)$', 'searchByPopularity'),
    url(r'^get_countries/$', 'getCountries'),
    url(r'^get_cities/(\w+)$', 'getCities'),
)
