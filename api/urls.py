
from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'trainings', views.TrainingFragmentViewSet)
router.register(r'requests', views.RequestFragmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
