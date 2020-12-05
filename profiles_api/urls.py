from django.urls import path, include

from rest_framework.routers import DefaultRouter # For register ViewSets

from profiles_api import views

# For resgister ViewSets
router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls))
]
