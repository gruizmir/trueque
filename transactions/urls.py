from django.conf.urls.defaults import *

urlpatterns = patterns('transactions.views',
    url(r'^bid/(\d+)$', 'newBid'),
)
