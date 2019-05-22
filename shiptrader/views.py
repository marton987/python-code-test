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

    def list(self, request, *args, **kwargs):
        """
        List all starships.

        **Notes:**

        **Example usage:**

            import requests
            response = requests.get('/api/v1/starships/')

        **Example response:**

            [
                {
                    "id": 1,
                    "starship_class": "Star dreadnought",
                    "manufacturer": "Kuat Drive Yards, Fondor Shipyards",
                    "length": 19000.0,
                    "hyperdrive_rating": 2.0,
                    "cargo_capacity": 250000000,
                    "crew": 279144,
                    "passengers": 38000
                }
            ]

        ---
        responseMessages:
            - code: 200
              message: OK

            consumes:
                - application/json
            produces:
                - application/json
        """
        return super(StarshipViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific starship.

        **Notes:**

        **Example usage:**

            import requests
            response = requests.get('/api/v1/starships/1/')

        **Example response:**

            {
                "id": 1,
                "starship_class": "Star dreadnought",
                "manufacturer": "Kuat Drive Yards, Fondor Shipyards",
                "length": 19000.0,
                "hyperdrive_rating": 2.0,
                "cargo_capacity": 250000000,
                "crew": 279144,
                "passengers": 38000
            }

        responseMessages:
            - code: 200
              message: OK
            - code: 404
              message: Not Found

            consumes:
                - application/json
            produces:
                - application/json
        """
        return super(StarshipViewSet, self).retrieve(request, *args, **kwargs)


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

    def list(self, request, *args, **kwargs):
        """
        List all listings. If you want to sort, you can use
        the query parameter `ordering` and define the type of sort.
        For example:

            /api/v1/listings/1/?ordering=price
            /api/v1/listings/1/?ordering=-price
            /api/v1/listings/1/?ordering=listing_time
            /api/v1/listings/1/?ordering=-listing_time

        If you need to filter the results, you can use the query
        parameter `ship_type__starship_class`.
        For example:

            /api/v1/listings/1/?ship_type__starship_class=Star dreadnought

        **Notes:**

        **Example usage:**

            import requests
            response = requests.get('/api/v1/listings/')

        **Example response:**

            [
                {
                    "id": 1,
                    "name": "Star dreadnought",
                    "ship_type": 1,
                    "price": 12,
                    "listing_time": 6
                }
            ]

        ---
        responseMessages:
            - code: 200
              message: OK

            consumes:
                - application/json
            produces:
                - application/json
        """
        return super(ListingViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific listing.

        **Notes:**

        **Example usage:**

            import requests
            response = requests.get('/api/v1/listings/1/')

        **Example response:**

            {
                "id": 1,
                "name": "Star dreadnought",
                "ship_type": 1,
                "price": 12,
                "listing_time": 6
            }


        responseMessages:
            - code: 200
              message: OK
            - code: 404
              message: Not Found

            consumes:
                - application/json
            produces:
                - application/json
        """
        return super(ListingViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a specific listing.

        **Notes:**

        **Example usage:**

            import requests
            response = requests.post('/api/v1/listings/', {
                "name": "Star dreadnought",
                "starship_class": "Star dreadnought",
                "price": 12,
                "listing_time": 6
            })

        **Example response:**

            {
                "id": 1,
                "name": "Star dreadnought",
                "ship_type": 1,
                "price": 12,
                "listing_time": 6
            }


        responseMessages:
            - code: 200
              message: OK
            - code: 404
              message: Not Found
            - code: 400
              message: Bad Request

            consumes:
                - application/json
            produces:
                - application/json
        """
        return super(ListingViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific listing.

        **Notes:**

        **Example usage:**

            import requests
            response = requests.delete('/api/v1/listings/1')

        **Example response:**

            {}


        responseMessages:
            - code: 204
              message: No Content
            - code: 404
              message: Not Found

            consumes:
                - application/json
            produces:
                - application/json
        """
        return super(ListingViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a specific listing.

        - If you want to deactivate the listing, you need to set the listing_time to 0.
        - If you want to reactivate the listing, you need to set the listing_time greater than 0.

        **Notes:**

        **Example usage:**

            import requests
            response = requests.put('/api/v1/listings/1', {
                "name": "Star dreadnought",
                "starship_class": "Star dreadnought",
                "price": 12,
                "listing_time": 6
            })

        **Example response:**

            {
                "id": 1,
                "name": "Star dreadnought",
                "ship_type": 1,
                "price": 12,
                "listing_time": 6
            }


        responseMessages:
            - code: 200
              message: Ok
            - code: 404
              message: Not Found

            consumes:
                - application/json
            produces:
                - application/json
        """
        return super(ListingViewSet, self).update(request, *args, **kwargs)
