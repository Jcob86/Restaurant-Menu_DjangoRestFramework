from django.shortcuts import render
from django.db.models.aggregates import Count
from menu.permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .models import Cart, Dish, DishImage
from .serializers import CartSerializer, DishImageSerializer, DishSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.annotate(dishes_count=Count('dishes')).all()
    serializer_class = CartSerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        if Dish.objects.filter(cart_id=kwargs['pk']):
            return Response({'error': 'Cart cannot be deleted because it has dishes'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class DishViewSet(ModelViewSet):
    queryset = Dish.objects.prefetch_related('images').all()
    serializer_class = DishSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {'request': self.request}


class DishImageViewSet(ModelViewSet):
    serializer_class = DishImageSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {'dish_id': self.kwargs['dish_pk']}

    def get_queryset(self):
        return DishImage.objects.filter(dish_id=self.kwargs['dish_pk'])