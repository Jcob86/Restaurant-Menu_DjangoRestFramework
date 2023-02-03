from django.shortcuts import render
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from menu.permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .models import Cart, Dish, DishImage
from .serializers import CartSerializer, DishImageSerializer, DishSerializer, MenuSerializer

# ViewSet to get and manage Cart/Menu, non public API (Admin status required)
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.annotate(dishes_count=Count('dishes')).all()
    serializer_class = CartSerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        if Dish.objects.filter(cart_id=kwargs['pk']):
            return Response({'error': 'Cart cannot be deleted because it has dishes'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

# ViewSet to get and manage Dishes, non public API (Admin status required)
class DishViewSet(ModelViewSet):
    queryset = Dish.objects.prefetch_related('images').all()
    serializer_class = DishSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {'request': self.request}

# ViewSet to get and manage images of dishes, non public API (Admin status required)
class DishImageViewSet(ModelViewSet):
    serializer_class = DishImageSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {'dish_id': self.kwargs['dish_pk']}

    def get_queryset(self):
        return DishImage.objects.filter(dish_id=self.kwargs['dish_pk'])

# ViewSet to get Menu, public API(login not required, but if user is Admin it is possible to manage Carts)
class MenuViewSet(ModelViewSet):
    queryset = Cart.objects.annotate(dishes_count=Count('dishes')).filter(dishes_count__gt=0)
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'added', 'last_update']
    ordering_fields = ['title', 'dishes_count']


    def destroy(self, request, *args, **kwargs):
        if Dish.objects.filter(cart_id=kwargs['pk']):
            return Response({'error': 'Cart cannot be deleted because it has dishes'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)