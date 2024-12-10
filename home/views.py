from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.conf import settings
from azure.storage.blob import BlobServiceClient
from .models import AudioSaving
from .serializers import AudioSavingSerializer
import uuid
import os
from django.shortcuts import render
from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas
from datetime import datetime, timedelta
import base64
import ssl
import urllib.request
import json
from .speech_to_text import transcribe


class AdminAudioViewSet(viewsets.ModelViewSet):
    queryset = AudioSaving.objects.all()
    serializer_class = AudioSavingSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        # Save the uploaded file to Azure Blob Storage
        audio_file = self.request.FILES['audio_file']  # Get the uploaded audio file
        gathered_urls = self.upload_audio_to_blob(audio_file)

        # Save the metadata (SAS URL) in the database
        
        serializer.save(blob_url=gathered_urls[0],audio_file_name=gathered_urls[1],file_blog_uri=gathered_urls[2],base_64_string=gathered_urls[3], user=self.request.user)
        transcribe(gathered_urls[2])

    def upload_audio_to_blob(self, audio_file):
        """
        Uploads an audio file to Azure Blob Storage and returns the SAS URI.
        """
        # Initialize Azure Blob Service Client
        blob_service_client = BlobServiceClient(account_url=f"https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
                                                 credential=settings.AZURE_STORAGE_ACCOUNT_KEY)

        # Create a unique file name for the audio file
        file_name = str(uuid.uuid4()) + os.path.splitext(audio_file.name)[-1]

        # Create a container client to interact with the container
        container_client = blob_service_client.get_container_client(settings.AZURE_STORAGE_CONTAINER_NAME)

        # Upload the file to the Azure Blob Storage
        blob_client = container_client.get_blob_client(file_name)
        blob_client.upload_blob(audio_file, overwrite=True)

        sas_token = generate_blob_sas(
            account_name=settings.AZURE_STORAGE_ACCOUNT_NAME,
            container_name=settings.AZURE_STORAGE_CONTAINER_NAME,
            blob_name=file_name,
            account_key=settings.AZURE_STORAGE_ACCOUNT_KEY,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=12)  # Set expiry time for the SAS URL
        )

        blob_url=blob_client.url
        audio_file_name=file_name
        sas_url = f"{blob_url}?{sas_token}"
        base_64_string = "None"
        
        gathered_urls=[blob_url, audio_file_name, sas_url,base_64_string]
        return gathered_urls  

def home(request):
    return render(request, 'apps/home/profile.html')
    

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AudioSaving
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

@method_decorator(csrf_exempt, name='dispatch')
class SaveAudioView(View):
    def upload_audio_to_blob(self, audio_file):
        """
        Uploads an audio file to Azure Blob Storage and returns the SAS URL.
        """
        try:
            # Initialize Azure Blob Service Client
            blob_service_client = BlobServiceClient(
                account_url=f"https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
                credential=settings.AZURE_STORAGE_ACCOUNT_KEY
            )

            # Generate a unique file name
            file_name = str(uuid.uuid4()) + os.path.splitext(audio_file.name)[-1]

            # Get container client
            container_client = blob_service_client.get_container_client(settings.AZURE_STORAGE_CONTAINER_NAME)

            # Upload the file
            blob_client = container_client.get_blob_client(file_name)
            blob_client.upload_blob(audio_file, overwrite=True)

            sas_token = generate_blob_sas(
                account_name=settings.AZURE_STORAGE_ACCOUNT_NAME,
                container_name=settings.AZURE_STORAGE_CONTAINER_NAME,
                blob_name=file_name,
                account_key=settings.AZURE_STORAGE_ACCOUNT_KEY,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(hours=12)  # Set expiry time for the SAS URL
            )

            blob_url=blob_client.url
            audio_file_name=file_name
            sas_url = f"{blob_url}?{sas_token}"
            base_64_string = 'None'
            
            gathered_urls=[blob_url, audio_file_name, sas_url,base_64_string]
            return gathered_urls
        except Exception as e:
            raise Exception(f"Failed to upload file to Azure Blob Storage: {str(e)}")

    def post(self, request, *args, **kwargs):
        # Check if the request contains a file
        audio_file = request.FILES.get('audio_file')
        if not audio_file:
            return JsonResponse({'error': 'No audio file provided'}, status=400)

        try:
            # Upload to Azure Blob Storage
            gathered_urls = self.upload_audio_to_blob(audio_file)

            # Save the record in the database
            audio_instance = AudioSaving(
                blob_url=gathered_urls[0],
                audio_file_name=gathered_urls[1],
                file_blog_uri=gathered_urls[2], 
                base_64_string=gathered_urls[3],
                user=self.request.user
            )
            audio_instance.save()
            transcribe(gathered_urls[2])
            return JsonResponse({
                'message': 'Audio saved successfully',
                'audio_id': audio_instance.id,
            }, status=201)

        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Failed to save audio', 'details': str(e)}, status=500)
        















def msg(request):
    audios = AudioSaving.objects.all()
    context = {
        'audios': audios
    }
    return render(request, 'apps/msg/msg.html', context)