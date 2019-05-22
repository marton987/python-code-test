""" Shiptrader views """
from rest_framework import viewsets

from shiptrader.models import Starship, Listing
from shiptrader.serializers import StarshipSerializer, ListingSerializer


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
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
