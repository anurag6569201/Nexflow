from django.shortcuts import render

def iot_home(request):
    return render(request,'iot_app/iot_home.html')