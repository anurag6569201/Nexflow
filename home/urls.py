from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import AudioSavingViewSet
from .views import SignupView, LoginView
from .views import SaveAudioView

# Create a router and register the API viewset
router = DefaultRouter()
router.register(r'audio', AudioSavingViewSet, basename='audio')

urlpatterns = [
    path('', views.home, name='home'),  # Main application home view
    path('api/', include(router.urls)),  # API routes for the audio_saving model
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout views
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('save/audio/', SaveAudioView.as_view(), name='save_audio'),
]
