from rest_framework import serializers
from .models import Cart, Dish, DishImage


class CartSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Dish
        fields = ['id', 'title', 'cart', 'description', 'price', 'preparation_time','added', 'last_update', 'is_vegetarian', 'images']


# class MenuSerializer(serializers.ModelSerializer):
#     pass