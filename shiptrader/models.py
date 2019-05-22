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


class Listing(models.Model):
    """ Listing model """
    name = models.CharField(max_length=255)
    ship_type = models.ForeignKey(Starship, related_name='listings')
    price = models.IntegerField()

    def __str__(self):
        """
        :return: Listing name
        """
        return self.name
