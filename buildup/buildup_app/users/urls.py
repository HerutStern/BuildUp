from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from buildup_app.users import views

router = DefaultRouter()

urlpatterns = [
    path('auth/login', TokenObtainPairView.as_view()),
    path('auth/refresh', TokenRefreshView.as_view()),
    path('auth/signup', views.signup),
    path('auth/user', views.user),
]

urlpatterns.extend(router.urls)