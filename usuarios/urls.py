from django.conf.urls import patterns, url

urlpatterns = patterns('usuarios.views',
    url(r'^$', 'register'),
)
