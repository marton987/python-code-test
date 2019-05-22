""" Shiptrader Models """
from django.db import models


class Starship(models.Model):
    """ Starship model """
    starship_class = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)

    length = models.FloatField()
    hyperdrive_rating = models.FloatField()
    cargo_capacity = models.BigIntegerField()

    crew = models.IntegerField()
    passengers = models.IntegerField()

    def __str__(self):
        """
        :return: Starship class
        """
        return self.starship_class


class ListingQuerySet(models.QuerySet):
    """ Listing Queryset """

    def active(self):
        """Filter active listings"""
        return self.filter(listing_time__gt=0)


class Listing(models.Model):
    """ Listing model """
    objects = ListingQuerySet.as_manager()

    name = models.CharField(max_length=255)
    ship_type = models.ForeignKey(Starship, related_name='listings')
    price = models.IntegerField()
    listing_time = models.IntegerField(default=1)

    def __str__(self):
        """
        :return: Listing name
        """
        return self.name
