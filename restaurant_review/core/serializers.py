from rest_framework import serializers
from . import models


class CategoryModelSerailizer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class RestaurantMenuModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantMenu
        fields = '__all__'
        extra_kwargs = {
            'restaurant': {'required': False}
        }


class RestaurantPhotoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantPhoto
        fields = '__all__'
        extra_kwargs = {
            'restaurant': {'required': False}
        }


class RestaurantModelSerializer(serializers.ModelSerializer):
    category = CategoryModelSerailizer(many=True)
    menus = RestaurantMenuModelSerializer(read_only=True, many=True)
    photos = RestaurantPhotoModelSerializer(many=True, read_only=True)

    class Meta:
        model = models.Restaurant
        fields = '__all__'


class RestaurantReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantReview
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'restaurant': {'required': False},
        }
