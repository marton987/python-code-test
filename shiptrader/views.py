""" Shiptrader views """
from rest_framework import viewsets

from shiptrader.models import Starship, Listing
from shiptrader.serializers import StarshipSerializer, ListingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class StarshipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset of Starship
    """
    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer


class ListingViewSet(viewsets.ModelViewSet):
    """
    Viewset of Listing
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('ship_type__starship_class',)
    ordering_fields = ('price', 'listing_time')

    def get_queryset(self):
        """
        Override queryset if the user is not updating or deleting to display
        only active listings
        :return: Queryset of listings
        """
        queryset = super(ListingViewSet, self).get_queryset()

        if self.action not in ['update', 'delete']:
            queryset = queryset.active()

        return queryset
