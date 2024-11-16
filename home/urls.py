from django.urls import path,include
from home import views
from rest_framework import routers
from rest_framework import routers
router = routers.DefaultRouter()

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
