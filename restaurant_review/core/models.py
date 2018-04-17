import os

from django.db import models
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField


def upload_path(instance, filename):
    """ Generate upload location based on restaurant id """
    return os.path.join('restaurant_%s' % instance.id, filename)


def upload_path_review(instance, filename):
    """ Generate upload location to subdir based on restaurant id """
    return os.path.join('restaurant_%s/review/' % instance.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    restaurant_bookmarks = models.ManyToManyField(
        'Restaurant',
        related_name='bookmarks')


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Restaurant(models.Model):
    category = models.ManyToManyField(Category, blank=True, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    rate = models.FloatField(default=0)
    img = VersatileImageField(upload_to=upload_path)

    open_time = models.TimeField(blank=True, null=True)
    close_time = models.TimeField(blank=True, null=True)

    location_lat = models.CharField(max_length=250, blank=True, null=True)
    location_lng = models.CharField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RestaurantPhoto(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='photos')
    img = VersatileImageField(upload_to=upload_path)

    def __str__(self):
        return self.restaurant.title


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    img = VersatileImageField(upload_to=upload_path)


class RestaurantRating(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = VersatileImageField(upload_to=upload_path_review)
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
