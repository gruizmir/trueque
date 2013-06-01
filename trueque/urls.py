from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^products/', include('products.urls')),
    url(r'^search/', include('main.urls')),
    url(r'^register/', 'usuarios.views.register'),
    url(r'^login/', 'usuarios.views.login'),
    url(r'^logout', 'usuarios.views.logout'),
    url(r'^about', 'main.views.about'),
    url(r'^transactions/', include('transactions.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^usuarios/', include('usuarios.urls')),
    url(r'^album/', include('albums.urls')),
    url(r'^$', 'main.views.search' ),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
