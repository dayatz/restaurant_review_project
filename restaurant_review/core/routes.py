from django.urls import path, include

from rest_framework_nested import routers
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
    path('auth/', viewsets.AuthTokenView.as_view()),
    path('auth/register/', viewsets.UserRegisterView.as_view()),
    # path('oauth2/', include('rest_framework_social_oauth2.urls'))
)
