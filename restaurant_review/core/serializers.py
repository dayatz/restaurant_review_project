from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from . import models


class UserModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'],
            validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


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
    rated = serializers.SerializerMethodField()

    def get_rated(self, obj):
        user = self.context.get('request').user
        print(self.context.get('request').user)
        return user.id in obj.rates.values_list('user', flat=True)

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
