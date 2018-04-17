from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r'restaurants', viewsets.RestaurantModelViewset)

urlpatterns = router.urls
