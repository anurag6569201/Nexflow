from django.urls import path
from iot_app import views

app_name = 'iot_app'

urlpatterns = [
    path('', views.iot_home, name='iot_home'),
]
