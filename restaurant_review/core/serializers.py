from rest_framework import serializers
from . import models


class CategoryModelSerailizer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class RestaurantModelSerializer(serializers.ModelSerializer):
    category = CategoryModelSerailizer(many=True)

    class Meta:
        model = models.Restaurant
        fields = '__all__'


class RestaurantPhotoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantPhoto
        fields = '__all__'


class RestaurantReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RestaurantReview
        fields = '__all__'
