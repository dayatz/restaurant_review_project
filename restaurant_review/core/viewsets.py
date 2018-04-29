# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions, authentication
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from url_filter.integrations.drf import DjangoFilterBackend

from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework_social_oauth2.authentication import SocialAuthentication
from . import serializers, models, permissions as custom_permissions


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
    authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Restaurant.objects\
        .prefetch_related('category', 'menus', 'photos')
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['title']

    def get_serializer_context(self):
        return {'request': self.request}

    # @method_decorator(cache_page(60 * 60))
    # def dispatch(self, request, *args, **kwargs):
    #     return super(RestaurantModelViewset, self)\
    #         .dispatch(request, *args, **kwargs)

    @action(
        detail=True,
        permission_classes=[custom_permissions.ReviewPermission],
        authentication_classes=[authentication.TokenAuthentication],
        methods=['POST'])
    def rate(self, request, pk=None):
        rating, created = models.RestaurantRating.objects.get_or_create(
            restaurant_id=pk,
            user=request.user
        )
        rating.rate = request.data.get('rate')
        rating.save()
        return Response({'status': 'success',
                         'rate': request.data.get('rate'),
                         'restaurant_rate': rating.restaurant.rate})

    @action(detail=False,
            permission_classes=[
                permissions.IsAuthenticated,
                custom_permissions.ReviewPermission],
            authentication_classes=[authentication.TokenAuthentication],
            methods=['GET', 'POST'])
    def bookmarks(self, request):
        if request.POST:
            restaurant_id = request.data.get('id')
            if request.user.userprofile\
                    .restaurant_bookmarks.filter(id=restaurant_id).exists():
                request.user.userprofile\
                    .restaurant_bookmarks.remove(restaurant_id)
                status = 'removed'
            else:
                request.user.userprofile\
                    .restaurant_bookmarks.add(restaurant_id)
                status = 'added'
            return Response({'status': status})

        restaurants = request.user.userprofile.restaurant_bookmarks\
            .prefetch_related('category', 'menus', 'photos')
        serializer = serializers.RestaurantModelSerializer(
            restaurants, many=True, context={'request': request})
        return Response(serializer.data)


class CategoryModelViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CategoryModelSerailizer
    queryset = models.Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [OAuth2Authentication, SocialAuthentication]


class RestaurantReviewModelViewset(viewsets.ModelViewSet):
    serializer_class = serializers.RestaurantReviewModelSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [custom_permissions.ReviewPermission]

    def get_queryset(self):
        return models.RestaurantReview.objects\
            .select_related('user')\
            .filter(restaurant_id=self.kwargs.get('restaurant_pk'))

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
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
