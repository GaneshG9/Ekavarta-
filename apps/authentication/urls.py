from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('verify/', views.VerifyAccountView.as_view(), name='verify'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
] + router.urls