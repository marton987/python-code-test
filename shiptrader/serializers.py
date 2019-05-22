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
    starship_class = serializers.SlugRelatedField(
        write_only=True, queryset=Starship.objects.all(), slug_field='starship_class')

    class Meta:
        model = Listing
        fields = (
            'id', 'name', 'ship_type', 'price', 'listing_time',
            'starship_class',
        )
        extra_kwargs = {
            'ship_type': {'required': False},
            'listing_time': {'required': False},
        }

    def create(self, validated_data):
        """
        Override create function from ListingSerializer to get the ship_type
        from the starship_class

        :param validated_data: Already validated data from the serializer
        :return: New instance
        """
        validated_data['ship_type'] = validated_data.pop('starship_class')
        return super(ListingSerializer, self).create(validated_data)
