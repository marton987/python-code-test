""" Shiptrader views """
from rest_framework import viewsets

from shiptrader.models import Starship
from shiptrader.serializers import StarshipSerializer


class StarshipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset of Starship
    """
    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer
