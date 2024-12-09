from django.urls import path, include
from rest_framework.routers import DefaultRouter
from home import views
from home.views import SaveAudioView

app_name = 'home'

# Router for Admin Views
router = DefaultRouter()
router.register(r'audio', views.AdminAudioViewSet, basename='audio')


urlpatterns = [
    path('', views.home, name='home'),

    # Admin views
    path('api/', include(router.urls)),
    path('save/audio/', SaveAudioView.as_view(), name='save_audio'),

]
