from django.urls import path
from home import views
from django.views.generic import TemplateView


app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),

    # readme urls
    path('profile/readme/edit/', views.readme_edit, name='readme_edit'),
]
