# -*- coding: utf-8 -*-
from soaplib.core.service import soap, DefinitionBase
from soaplib.core.model.primitive import String, Integer
from soaplib.core import Application
from django.views.generic import FormView, ListView, TemplateView, DetailView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from music.forms import GetArtistForm, GetUserInfoForm, GetOrderStatusForm
from music.services import MusicBackofficeClient, OrderBackofficeClient
from soap_handler import DjangoSOAPAdaptor
from music.models import Order

class GetArtistsView(FormView):
    template_name = 'get_artists.html'
    form_class = GetArtistForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GetArtistsView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        artist_name = form.cleaned_data['artist_name']

        return HttpResponseRedirect(
            reverse('list_artists', args=[artist_name])
        )


class ListArtistsView(ListView):
    template_name = 'list_artists.html'
    context_object_name = 'artists'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListArtistsView, self).dispatch(*args, **kwargs)

    def _helper_artist_info_dict(self, artist):
        return {
            'name':artist.get('name'),
            'image':artist.get('image')[1].get('#text'),
            'url':reverse('list_artist_tracks', args=[artist.get('name')]),
        }

    def get_queryset(self):
        artists = MusicBackofficeClient().search_artist(self.args[0])

        return [
            self._helper_artist_info_dict(artist)
            for artist
            in artists['results']['artistmatches']['artist']
        ]


class ListArtistTracksView(FormView):
    template_name = 'list_artist_tracks.html'
    context_object_name = 'tracks'
    form_class = GetUserInfoForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListArtistTracksView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        user_name = form.cleaned_data['name']
        address = form.cleaned_data['address']
        blacklist = ['name','address','csrfmiddlewaretoken']
        tracks = [f for f in form.data.keys() if f not in blacklist]

        msg = OrderBackofficeClient().submit_order(tracks, user_name, address)

        #Save order_id with status In Progress
        Order.objects.create(slug=int(msg), status="Registered",)

        return HttpResponseRedirect(
            reverse('checkout', args=[msg])
        )

    def _helper_track_info_dict(self, track):
        return {
            'name':track.get('name')
        }

    def get_context_data(self, **kwargs):
        tracks = MusicBackofficeClient().get_artist_tracks(self.args[0])

        new_tracks = [
            self._helper_track_info_dict(track)
            for track
            in tracks['toptracks']['track']
        ]

        kwargs['tracks'] = new_tracks

        return kwargs


class CheckoutView(TemplateView):
    template_name = 'checkout.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CheckoutView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['uri_index'] = reverse('index')
        kwargs['order_id'] = self.args[0]
        return kwargs


class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['uri_artists'] = reverse('get_artists')
        kwargs['uri_order'] = reverse('get_order')

        return kwargs

class GetOrderStatusView(FormView):
    template_name = 'get_order_status.html'
    form_class = GetOrderStatusForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(GetOrderStatusView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        slug = form.cleaned_data['slug']

        return HttpResponseRedirect(
            reverse('list_order', args=[slug])
        )


class ListOrderView(DetailView):
    context_object_name = 'order'
    model = Order
    template_name = 'list_order.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListOrderView, self).dispatch(*args, **kwargs)


class OrderStatusService(DefinitionBase):
    @soap(Integer, String, _returns=String)
    def changeStatusOrder(self, order, status):
        Order.objects.filter(slug=int(order)).update(status=status)
        return "OK"


orderstatus_service = DjangoSOAPAdaptor(
    Application(
        [OrderStatusService], 'tns'
    )
)
