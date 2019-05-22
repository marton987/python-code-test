import requests

from django.core.management.base import BaseCommand, CommandError

from shiptrader.models import Starship


class Command(BaseCommand):
    help = '''Command to import Starships from remote server.

Example:
manage.py import_starships --endpoint https://swapi.co/api/starships/
    '''

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands.

        :param parser: BaseCommand parser
        :return: None
        """
        parser.add_argument(
            '--endpoint',
            type=str,
            dest='endpoint',
            help='Endpoint to retrieve starships.',
            default=False)

    @staticmethod
    def _insert_starships(starship):
        """
        Helper function that inserts starship dictionary in the database
        :param starship: Dictionary with starship values
        :return: (Starship object, Boolean) True if created
        """
        starship_class = starship.get('starship_class')
        manufacturer = starship.get('manufacturer')
        length = starship.get('length').replace(',', '') if starship.get('length') != 'unknown' else 0
        hyperdrive_rating = starship.get('hyperdrive_rating').replace(',', '') \
            if starship.get('hyperdrive_rating') != 'unknown' else 0
        cargo_capacity = starship.get('cargo_capacity') if starship.get('cargo_capacity') != 'unknown' else 0
        crew = starship.get('crew') if starship.get('crew') != 'unknown' else 0
        passengers = starship.get('passengers') if starship.get('passengers') != 'unknown' else 0

        starship_data = {
            'starship_class': starship_class,
            'manufacturer': manufacturer,
            'length': float(length),
            'hyperdrive_rating': float(hyperdrive_rating),
            'cargo_capacity': int(cargo_capacity),
            'crew': int(crew),
            'passengers': int(passengers),
        }

        return Starship.objects.update_or_create(**starship_data)

    def _get_insert_starships(self, endpoint):
        """
        Helper function that will be called recursively until starship's
        endpoint contains results.

        :param endpoint: Endpoint URL to be fetched
        :return: Number of results fetched by the server.
        """
        try:
            resp = requests.get(endpoint)
            data = resp.json()
        except requests.exceptions.MissingSchema:
            raise CommandError(u'Starships endpoint is invalid')
        except ValueError:
            raise CommandError(u'Starships endpoint does not contains a JSON valid response')

        # Insert starship on DB
        for starship in data.get('results'):
            self._insert_starships(starship)

        # Check if exists another page to fetch results
        next_endpoint = data.get('next')
        if next_endpoint:
            self._get_insert_starships(next_endpoint)

        return data.get('count')

    def handle(self, *args, **options):
        """
        The actual logic of the command.

        :param args: Arguments of the command
        :param options: Options submitted to the command
        :return: None
        """
        endpoint = options['endpoint']
        result = self._get_insert_starships(endpoint)

        self.stdout.write(u'Inserted {} records'.format(result))


