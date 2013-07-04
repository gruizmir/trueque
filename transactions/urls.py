from django.conf.urls.defaults import *

urlpatterns = patterns('transactions.views',
    url(r'^bid/(\d+)$', 'newBid'),
    url(r'^choosebid/(\d+)$', 'makeTrade'),
    url(r'^verify/(\d+)$', 'verifyTrade'),
    url(r'^pending/{0,1}$', 'showPending'),
)
