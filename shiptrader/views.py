""" Shiptrader views """
from rest_framework import viewsets

from shiptrader.models import Starship, Listing
from shiptrader.serializers import StarshipSerializer, ListingSerializer
from django_filters.rest_framework import DjangoFilterBackend


class StarshipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset of Starship
    """
    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer


class ListingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset of Listing
    """
    queryset = Listing.objects.active()
    serializer_class = ListingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('ship_type__starship_class',)
