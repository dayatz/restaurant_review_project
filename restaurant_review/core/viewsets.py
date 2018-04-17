from rest_framework import viewsets
from . import serializers, models


class RestaurantModelViewset(viewsets.ModelViewSet):
    serializer_class = serializers.RestaurantModelSerializer
    queryset = models.Restaurant.objects.all()


class CategoryModelViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CategoryModelSerailizer
    queryset = models.Category.objects.all()
