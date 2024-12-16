from django.shortcuts import render

def gmail_manage(request):
    return render(request, 'apps/gmail/gmail_manage.html')