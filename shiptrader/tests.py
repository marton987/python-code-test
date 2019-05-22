""" Shiptrader tests """
import json

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from shiptrader.factories import StarshipFactory, ListingFactory
from shiptrader.models import Starship, Listing


class StarshipTestCase(APITestCase):
    """
    Test starships endpoint
    """

    def setUp(self):
        """ setUp function """
        StarshipFactory.create_batch(50)

    def test_list_starships(self):
        """ List should contains all starships """
        response = self.client.get(
            reverse('starships-list')
        )

        stored_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, u'Status code does not match')

        count_starships = Starship.objects.count()
        self.assertGreater(count_starships, 0, u'No starships on DB')
        self.assertEqual(len(stored_data), count_starships, u'Number of results does not match')

        fetched_starship = stored_data[0]
        stored_starship = Starship.objects.get(pk=fetched_starship.get('id'))

        # Validate starship values
        self.assertEqual(fetched_starship.get('starship_class'), stored_starship.starship_class,
                         u'starship_class value does not match')
        self.assertEqual(fetched_starship.get('manufacturer'), stored_starship.manufacturer,
                         u'manufacturer value does not match')
        self.assertEqual(fetched_starship.get('length'), stored_starship.length,
                         u'length value does not match')
        self.assertEqual(fetched_starship.get('hyperdrive_rating'), stored_starship.hyperdrive_rating,
                         u'hyperdrive_rating value does not match')
        self.assertEqual(fetched_starship.get('cargo_capacity'), stored_starship.cargo_capacity,
                         u'cargo_capacity value does not match')
        self.assertEqual(fetched_starship.get('crew'), stored_starship.crew,
                         u'crew value does not match')

    def test_get_starships(self):
        """ Get returns a valid starship """
        starship = StarshipFactory()
        response = self.client.get(
            reverse('starships-detail', kwargs={'pk': starship.pk}),
        )

        stored_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, u'Status code does not match')

        # Validate starship values
        self.assertEqual(stored_data.get('starship_class'), starship.starship_class,
                         u'starship_class value does not match')
        self.assertEqual(stored_data.get('manufacturer'), starship.manufacturer,
                         u'manufacturer value does not match')
        self.assertEqual(stored_data.get('length'), starship.length,
                         u'length value does not match')
        self.assertEqual(stored_data.get('hyperdrive_rating'), starship.hyperdrive_rating,
                         u'hyperdrive_rating value does not match')
        self.assertEqual(stored_data.get('cargo_capacity'), starship.cargo_capacity,
                         u'cargo_capacity value does not match')
        self.assertEqual(stored_data.get('crew'), starship.crew,
                         u'crew value does not match')

    def test_get_invalid_starships(self):
        """ User try to fetch details from an invalid starship """
        response = self.client.get(
            reverse('starships-detail', kwargs={'pk': 9999}),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, u'Status code does not match')

    def test_create_starships(self):
        """ User try to create a starship """
        starship_stub = StarshipFactory.stub().__dict__

        response = self.client.post(
            reverse('starships-list'),
            json.dumps(starship_stub),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, u'Status code does not match')

    def test_update_starships(self):
        """ User try to update a starship """
        starship = StarshipFactory()
        starship_stub = StarshipFactory.stub().__dict__

        response = self.client.put(
            reverse('starships-detail', kwargs={'pk': starship.pk}),
            json.dumps(starship_stub),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, u'Status code does not match')

    def test_delete_starships(self):
        """ User try to delete a starship """
        starship = StarshipFactory()

        response = self.client.delete(
            reverse('starships-detail', kwargs={'pk': starship.pk}),
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, u'Status code does not match')


class ListingTestCase(APITestCase):
    """
    Test listings endpoint
    """

    def setUp(self):
        """ setUp function """
        self.starship = StarshipFactory()
        ListingFactory.create_batch(20)

    def test_list_listings(self):
        """ List should contains all listings """
        response = self.client.get(
            reverse('listings-list')
        )

        stored_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, u'Status code does not match')

        count_listings = Listing.objects.count()
        self.assertGreater(count_listings, 0, u'No listings on DB')
        self.assertEqual(len(stored_data), count_listings, u'Number of results does not match')

        fetched_listing = stored_data[0]
        stored_listing = Listing.objects.get(pk=fetched_listing.get('id'))

        # Validate listing values
        self.assertEqual(fetched_listing.get('name'), stored_listing.name, u'name value does not match')
        self.assertEqual(fetched_listing.get('price'), stored_listing.price, u'price value does not match')
        self.assertEqual(fetched_listing.get('ship_type'), stored_listing.ship_type.pk,
                         u'ship_type value does not match')

    def test_filter_listings(self):
        """ User should be able to filter listings against starship_class """
        starship_class = 'random_text'
        starship = StarshipFactory(starship_class=starship_class)
        listing = ListingFactory(ship_type=starship)

        response = self.client.get(
            reverse('listings-list'),
            {'ship_type__starship_class': starship_class}
        )

        stored_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, u'Status code does not match')

        count_listings = Listing.objects.count()
        self.assertGreater(count_listings, 0, u'No listings on DB')
        self.assertNotEqual(len(stored_data), count_listings, u'Number of results is matching')
        self.assertEqual(len(stored_data), 1, u'Filtered result is not being showed')

        fetched_listing = stored_data[0]

        # Validate listing values
        self.assertEqual(fetched_listing.get('id'), listing.pk, u'Id value does not match')
        self.assertEqual(fetched_listing.get('name'), listing.name, u'name value does not match')
        self.assertEqual(fetched_listing.get('price'), listing.price, u'price value does not match')
        self.assertEqual(fetched_listing.get('ship_type'), listing.ship_type.pk,
                         u'ship_type value does not match')

    def test_filter_listings_invalid(self):
        """ User should be able to filter listings against starship_class with existing starships """
        starship_class = 'random_text'

        response = self.client.get(
            reverse('listings-list'),
            {'ship_type__starship_class': starship_class}
        )

        stored_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, u'Status code does not match')

        count_listings = Listing.objects.count()
        self.assertGreater(count_listings, 0, u'No listings on DB')
        self.assertNotEqual(len(stored_data), count_listings, u'Number of results is matching')
        self.assertEqual(len(stored_data), 0, u'Filtered result already exists')

    def test_get_listings(self):
        """ Get returns a valid listing """
        listing = ListingFactory()
        response = self.client.get(
            reverse('listings-detail', kwargs={'pk': listing.pk}),
        )

        stored_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, u'Status code does not match')

        # Validate listing values
        self.assertEqual(stored_data.get('name'), listing.name, u'name value does not match')
        self.assertEqual(stored_data.get('price'), listing.price, u'price value does not match')
        self.assertEqual(stored_data.get('ship_type'), listing.ship_type.pk, u'ship_type value does not match')

    def test_get_invalid_listings(self):
        """ User try to fetch details from an invalid listing """
        response = self.client.get(
            reverse('listings-detail', kwargs={'pk': 9999}),
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, u'Status code does not match')

    def test_create_listings(self):
        """ User try to create a listing """
        listing_stub = ListingFactory.stub(ship_type=self.starship.pk).__dict__

        response = self.client.post(
            reverse('listings-list'),
            json.dumps(listing_stub),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, u'Status code does not match')

    def test_update_listings(self):
        """ User try to update a listing """
        listing = ListingFactory()
        listing_stub = ListingFactory.stub(ship_type=self.starship.pk).__dict__

        response = self.client.put(
            reverse('listings-detail', kwargs={'pk': listing.pk}),
            json.dumps(listing_stub),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, u'Status code does not match')

    def test_delete_listings(self):
        """ User try to delete a listing """
        listing = ListingFactory()

        response = self.client.delete(
            reverse('listings-detail', kwargs={'pk': listing.pk}),
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED, u'Status code does not match')
