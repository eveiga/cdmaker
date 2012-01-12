from django.conf.urls.defaults import patterns, url

from music.views import (GetArtistsView, ListArtistsView, ListArtistTracksView,
        CheckoutView, IndexView, orderstatus_service)

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view()),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^music/$', IndexView.as_view(), name='index',),
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
    url(
        r'music/checkout/(.+)/$',
        CheckoutView.as_view(),
        name='checkout'
    ),
    url(r'orderstatusservice.wsdl', orderstatus_service),
    url(r'orderstatusservice', orderstatus_service),
)
