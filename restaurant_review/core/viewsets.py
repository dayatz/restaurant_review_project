from rest_framework import viewsets, permissions
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework_social_oauth2.authentication import SocialAuthentication
from . import serializers, models


class RestaurantModelViewset(viewsets.ModelViewSet):
    serializer_class = serializers.RestaurantModelSerializer
    queryset = models.Restaurant.objects\
        .prefetch_related('category', 'menus', 'photos')


class CategoryModelViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CategoryModelSerailizer
    queryset = models.Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [OAuth2Authentication, SocialAuthentication]


class RestaurantReviewModelViewset(viewsets.ModelViewSet):
    serializer_class = serializers.RestaurantReviewModelSerializer

    def get_queryset(self):
        return models.RestaurantReview.objects.filter(
            restaurant_id=self.kwargs.get('restaurant_pk'))


class RestaurantMenuModelViewset(viewsets.ModelViewSet):
    serializer_class = serializers.RestaurantMenuModelSerializer

    def get_queryset(self):
        return models.RestaurantMenu.objects.filter(
            restaurant_id=self.kwargs.get('restaurant_pk'))

    def perform_create(self, serializer):
        serializer.save(restaurant_id=self.kwargs.get('restaurnt_pk'))


class RestaurantPhotoModelViewset(viewsets.ModelViewSet):
    serializer_class = serializers.RestaurantPhotoModelSerializer

    def get_queryset(self):
        return models.RestaurantPhoto.objects.filter(
            restaurant_id=self.kwargs.get('restaurant_pk'))

    def perform_create(self, serializer):
        serializer.save(restaurant_id=self.kwargs.get('restaurnt_pk'))
