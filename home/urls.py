from django.urls import path, include
from rest_framework.routers import DefaultRouter
from home import views

# Router for Admin Views
router = DefaultRouter()
router.register(r'admin/audio', views.AdminAudioViewSet, basename='admin_audio')

urlpatterns = [
    path('', views.home, name='home'),

    # Admin views
    path('api/', include(router.urls)),

    # API key-based access
    path('api/audio/', views.AudioSavingAPI, name='audio_api'),
]
