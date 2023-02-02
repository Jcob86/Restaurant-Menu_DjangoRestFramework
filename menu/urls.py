from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()

urlpatterns = router.urls
urlpatterns += [path('test', views.test)]
