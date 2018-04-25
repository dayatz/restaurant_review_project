from django.urls import path, include

from rest_framework_nested import routers
from rest_framework.authtoken import views as auth_views
from . import viewsets

router = routers.DefaultRouter()
router.register(r'restaurants', viewsets.RestaurantModelViewset)
router.register(r'categories', viewsets.CategoryModelViewset)

restaurant_router = routers.NestedDefaultRouter(
    router, r'restaurants', lookup='restaurant')
restaurant_router.register(
    r'reviews', viewsets.RestaurantReviewModelViewset,
    base_name='restaurant-reviews')
restaurant_router.register(
    r'menus', viewsets.RestaurantMenuModelViewset,
    base_name='restaurant-menu')
restaurant_router.register(
    r'photos', viewsets.RestaurantPhotoModelViewset,
    base_name='restaurant-photo')

urlpatterns = router.urls + restaurant_router.urls
urlpatterns += (
    path('auth/', auth_views.obtain_auth_token),
    path('rest_auth/', include('rest_auth.urls'))
    # path('oauth2/', include('rest_framework_social_oauth2.urls'))
)
