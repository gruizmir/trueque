from django.conf.urls import patterns, include, url

urlpatterns = patterns('albums.views',
	url(r'^toalbum/(\d+)$', 'showAlbums'),
	url(r'^savetoalbum/(\d+)$', 'saveAlbumData'),
)
