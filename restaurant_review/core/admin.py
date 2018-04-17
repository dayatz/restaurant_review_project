from django.contrib import admin
from . import models

admin.site.register(models.Restaurant)
admin.site.register(models.RestaurantPhoto)
admin.site.register(models.RestaurantMenu)
admin.site.register(models.Category)
