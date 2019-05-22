""" Shiptrader serializers """
from rest_framework import serializers

from shiptrader.models import Starship, Listing


class StarshipSerializer(serializers.ModelSerializer):
    """
    Starship serializer
    """
    class Meta:
        model = Starship
        fields = (
            'id', 'starship_class', 'manufacturer', 'length',
            'hyperdrive_rating', 'cargo_capacity', 'crew', 'passengers',
        )


class ListingSerializer(serializers.ModelSerializer):
    """
    Listing serializer
    """
    class Meta:
        model = Listing
        fields = (
            'id', 'name', 'ship_type', 'price',
        )
