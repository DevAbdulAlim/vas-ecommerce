from django.urls import path
from .views import ListView

app_name = 'core'
urlpatterns = [
    path('', ListView.as_view(), name='home'),
]