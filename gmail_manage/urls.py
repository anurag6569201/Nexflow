from django.urls import path
from gmail_manage import views

app_name = 'gmail_manage'

urlpatterns = [
    path('', views.gmail_manage, name='gmail_manage'),




    # dynamic data urls
    path('refresh-gmail-data/', views.refresh_gmail_data, name='refresh_gmail_data'),
    path('refresh-gmail-labels/', views.refresh_gmail_labels, name='refresh_gmail_labels'),

    path('fetch-emails/', views.refresh_gmail_at_intervals, name='email_interval_view'),
]
