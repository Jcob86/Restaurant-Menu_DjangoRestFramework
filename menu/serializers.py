from rest_framework import serializers
from datetime import datetime
from .models import Cart, Dish, DishImage


class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        return value.strftime("%Y-%m-%d")


class CartSerializer(serializers.ModelSerializer):
    added = CustomDateField()
    last_update = CustomDateField()
    class Meta:
        model = Cart
        fields = ['id', 'title', 'description', 'added', 'last_update', 'dishes_count']

    dishes_count = serializers.IntegerField(read_only=True)


class DishImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        dish_id = self.context['dish_id']
        return DishImage.objects.create(dish_id=dish_id, **validated_data)
    
    class Meta:
        model = DishImage
        fields = ['id', 'image']


class DishSerializer(serializers.ModelSerializer):
    images = DishImageSerializer(many=True, read_only=True)
    added = CustomDateField()
    last_update = CustomDateField()

    class Meta:
        model = Dish
        fields = ['id', 'title', 'cart', 'description', 'price', 'preparation_time','added', 'last_update', 'is_vegetarian', 'images']


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)
    added = CustomDateField()
    last_update = CustomDateField()
    class Meta:
        model = Cart
        fields = ['id', 'title', 'description', 'added', 'last_update', 'dishes_count', 'dishes']
    
    dishes_count = serializers.IntegerField(read_only=True)
