from django.conf.urls import patterns, url
from usuarios.views import ShowProfile

urlpatterns = patterns('usuarios.views',
    url(r'^$', 'register'),
    url(r'^confirm/$', 'confirm'),
    url(r'^reconfirm/$', 'resend_confirmation'),
    url(r'^login/$', 'login'),
    url(r'^editprofile/$', 'edit_user_profile'),
    url(r'^profile/$', ShowProfile().show_profile_default),
    url(r'^profile/addalbum/$', ShowProfile().show_add_album),
    
    url(r'^profile/[\d]+/addalbum$', ShowProfile().show_add_album_red),
    url(r'^profile/[\w.@]{0,90}/addalbum$', ShowProfile().show_add_album_red),
    
    url(r'^profile/[\d]+/follow/(?P<user_id>[\d]+)$', ShowProfile().add_follow),
    url(r'^profile/[\w.@]{0,90}/follow/(?P<user_id>[\d]+)$', ShowProfile().add_follow),
    
    url(r'^profile/[\d]+/cancelfollow/(?P<user_id>[\d]+)$', ShowProfile().cancel_follow),
    url(r'^profile/[\w.@]{0,90}/cancelfollow/(?P<user_id>[\d]+)$', ShowProfile().cancel_follow),
    
    url(r'^profile/(?P<user_id>[\d]+)/$',  ShowProfile().show_profile_using_id),
    url(r'^profile/(?P<user_email>[\w.@]{0,90})/$', ShowProfile().show_profile_using_mail),
)
