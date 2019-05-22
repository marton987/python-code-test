import random

import factory.fuzzy
import faker

from shiptrader.models import Starship

fake = faker.Factory.create()


class StarshipFactory(factory.DjangoModelFactory):
    """ Starship factory """
    starship_class = factory.LazyAttribute(lambda o: fake.name())
    manufacturer = factory.LazyAttribute(lambda o: fake.sentence())
    length = factory.fuzzy.FuzzyFloat(0.1, 100.7)
    hyperdrive_rating = factory.fuzzy.FuzzyFloat(0.1, 50.7)
    cargo_capacity = random.randrange(1, 500000)
    crew = random.randrange(1, 10)
    passengers = random.randrange(1, 50)

    class Meta:
        model = Starship
