""" Shiptrader tests """
import json

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from shiptrader.factories import StarshipFactory
from shiptrader.models import Starship


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
