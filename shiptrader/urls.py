"""" Shiptrader URLs """
from django.conf.urls import include, url
from rest_framework import routers

from shiptrader import views

router = routers.SimpleRouter(trailing_slash=False)
# Shiptrader routes
router.register(r'starships', views.StarshipViewSet, 'starships')


urlpatterns = [
    url('', include(router.urls)),
]
