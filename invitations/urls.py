from django.conf.urls import patterns, url

urlpatterns = patterns('invitations.views',
    url(r'^send/$', 'sendInvitations'),
)
