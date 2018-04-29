from django.db import models
from django.db.models import Avg
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField
from rest_framework.authtoken.models import Token


def upload_path(instance, filename):
    """ Generate upload location based on restaurant id """
    return 'restaurant_{0}/{1}'.format(instance.id, filename)


def upload_path_review(instance, filename):
    """ Generate upload location to subdir based on restaurant id """
    return 'restaurant_{0}/review/{1}'.format(instance.id, filename)


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
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=150)
    description = models.TextField()
    rate = models.DecimalField(default=0, max_digits=3, decimal_places=1)
    img = VersatileImageField(upload_to=upload_path)

    open_time = models.TimeField(blank=True, null=True)
    close_time = models.TimeField(blank=True, null=True)

    location_lat = models.CharField(max_length=250, blank=True, null=True)
    location_lng = models.CharField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RestaurantPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='photos')
    img = VersatileImageField(upload_to=upload_path)

    def __str__(self):
        return self.restaurant.title


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name='menus')
    img = VersatileImageField(upload_to=upload_path)

    def __str__(self):
        return self.restaurant.title


class RestaurantRating(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='rates')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(blank=True, null=True)


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = VersatileImageField(
        upload_to=upload_path_review, blank=True, null=True)
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=RestaurantRating)
def save_rate_to_restaurant(sender, instance, *args, **kwargs):
    restaurant = instance.restaurant
    restaurant.rate = sender.objects.aggregate(s=Avg('rate'))['s']
    restaurant.save()
