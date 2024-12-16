from django.urls import path
from gmail_manage import views

app_name = 'gmail_manage'

urlpatterns = [
    path('', views.gmail_manage, name='gmail_manage'),
]
