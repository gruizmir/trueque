from django.conf.urls import patterns, url
from usuarios.views import ShowProfile

urlpatterns = patterns('usuarios.views',
    url(r'^confirm/$', 'confirm'),
    url(r'^reconfirm/$', 'resend_confirmation'),
    url(r'^profile/editprofile/{0,1}$', 'edit_user_profile'),
    url(r'^profile/$', ShowProfile().show_profile_default),
    
    url(r'^profile/addalbum/{0,1}$', ShowProfile().show_add_album),
    url(r'^profile/[\d]+/addalbum/{0,1}$', ShowProfile().show_add_album_red),
    url(r'^profile/[\w.@]{0,90}/addalbum/{0,1}$', ShowProfile().show_add_album_red),
    
    url(r'^profile/showalbum/$', ShowProfile().show_album),
    url(r'^profile/[\d]+/showalbum/$', ShowProfile().show_album),
    url(r'^profile/[\w.@]{0,90}/showalbum/$', ShowProfile().show_album),
    
    url(r'^profile/followers$', ShowProfile().show_followers),
    url(r'^profile/following$', ShowProfile().show_following),
    
    url(r'^profile/mail$', ShowProfile().show_mail),
    url(r'^profile/mail/inbox/$', ShowProfile().show_mail),
    url(r'^profile/mail/compose/$', ShowProfile().show_mail_compose),
    url(r'^profile/mail/sent/$', ShowProfile().show_mail_sent),

    url(r'^profile/follow/(?P<user_id>[\d]+)$', ShowProfile().add_follow),
    url(r'^profile/follow/(?P<user_id>[\d]+)$', ShowProfile().add_follow),

    url(r'^profile/cancelfollow/(?P<user_id>[\d]+)$', ShowProfile().cancel_follow),
    url(r'^profile/cancelfollow/(?P<user_id>[\d]+)$', ShowProfile().cancel_follow),

    url(r'^profile/(?P<user_id>[\d]+)/{0,1}$',  ShowProfile().show_profile_using_id),
    url(r'^profile/(?P<user_email>[\w.@]{0,90})/{0,1}$', ShowProfile().show_profile_using_mail),
    
)
