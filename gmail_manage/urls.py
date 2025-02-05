from django.urls import path
from gmail_manage import views

app_name = 'gmail_manage'

urlpatterns = [
    path('', views.gmail_manage, name='gmail_manage'),
    path('testing/', views.testing, name='testing'),




    # dynamic data urls
    path('refresh-gmail-data/', views.refresh_gmail_data, name='refresh_gmail_data'),
    path('refresh-gmail-labels/', views.refresh_gmail_labels, name='refresh_gmail_labels'),

    path('fetch-emails/', views.refresh_gmail_at_intervals, name='email_interval_view'),
    path('delete_gmail_by_labels/', views.delete_gmail_by_labels, name='delete_gmail_by_labels'),
    path('delete_gmail_by_id/', views.delete_gmail_by_id, name='delete_gmail_by_id'),


    path("gmail-webhook/", views.gmail_webhook, name="gmail-webhook"),
]
