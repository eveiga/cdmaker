from django.conf.urls.defaults import patterns, include, url

from music.views import GetArtistsView, ListArtistsView, ListArtistTracksView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^music/get_artists/', GetArtistsView.as_view(), name='get_artists',),
    url(r'^music/list_artists/(.+)/$',
        ListArtistsView.as_view(),
        name='list_artists'
    ),
    url(
        r'^music/list_artist_tracks/(.+)/$',
        ListArtistTracksView.as_view(),
        name='list_artist_tracks',
    ),
)
