from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework_social_oauth2.authentication import SocialAuthentication
from . import serializers, models


class AuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = serializers.UserModelSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        json = user_serializer.data
        json['token'] = token.key
        return Response(json)


class UserRegisterView(CreateAPIView):
    serializer_class = serializers.UserModelSerializer
    queryset = models.User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        print(user)
        headers = self.get_success_headers(serializer.data)
        json = serializer.data
        json['token'] = user.auth_token.key
        return Response(json, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


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
