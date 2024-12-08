from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import AudioSaving
from .serializers import AudioSavingSerializer
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'apps/home/profile.html')

# View for Admin Access via Web
class AdminAudioViewSet(viewsets.ModelViewSet):
    queryset = AudioSaving.objects.all()
    serializer_class = AudioSavingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Restrict to admin users only

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# API Access for API Key Holders
class AudioSavingAPI():
    permission_classes = [IsAuthenticated, IsAdminUser]  # Restrict access to API key holders

    def get(self, request, *args, **kwargs):
        audio_files = AudioSaving.objects.all()
        serializer = AudioSavingSerializer(audio_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = AudioSavingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=None)  # API key access means no logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
