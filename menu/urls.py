from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from . import views

router = SimpleRouter()
router.register('carts', views.CartViewSet)
router.register('dishes', views.DishViewSet)

dishes_router = routers.NestedDefaultRouter(router, 'dishes', lookup='dish')
dishes_router.register('images', views.DishImageViewSet, basename='dish-images')


urlpatterns = router.urls + dishes_router.urls
