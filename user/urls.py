from django.urls import path
from .views import ProfileView, RegisterView, LoginView, LogoutView


app_name = 'user'
urlpatterns = [
    path('profile', ProfileView.as_view(), name='profile'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]