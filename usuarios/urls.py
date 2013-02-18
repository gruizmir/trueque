from django.conf.urls import patterns, url

urlpatterns = patterns('usuarios.views',
    url(r'^$', 'register'),
    url(r'^confirm/$', 'confirm'),
    url(r'^reconfirm/$', 'resend_confirmation'),
    url(r'^login/$', 'login'),
    url(r'^editprofile/$', 'edit_user_profile'),
    url(r'^profile/$', 'show_profile'),
    url(r'^profile/addalbum/$', 'show_add_album')
)
