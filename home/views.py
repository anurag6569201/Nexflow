from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .live_stt import transcribe
from .models import AudioSaving
from .serializers import AudioSavingSerializer
from home.Extraction.audio_data_extraction import process_and_save_text_detailing

class AdminAudioViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        audio_file = request.FILES.get('audio_file')
        if not audio_file:
            return Response({"error": "No audio file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Transcribe the audio file
        transcription_text = transcribe(audio_file)

        return Response({
            "message": "Audio transcribed successfully",
            "transcription_text": transcription_text
        }, status=status.HTTP_200_OK)



def home(request):
    return render(request, 'apps/home/profile.html')


@method_decorator(csrf_exempt, name='dispatch')
class SaveAudioView(View):
    def post(self, request, *args, **kwargs):
        audio_file = request.FILES.get('audio_file')
        if not audio_file:
            return JsonResponse({"error": "No audio file provided."}, status=400)

        # Transcribe the audio file
        transcription_text = transcribe(audio_file)
        audio_instance = AudioSaving.objects.create(
            user=request.user if request.user.is_authenticated else None,
            is_transcribed=True,
            transcription_text=transcription_text
        )

        audio_id=audio_instance.id
        process_and_save_text_detailing(request,audio_id)

        return JsonResponse({
            'message': 'Audio transcribed successfully',
            'transcription_text': transcription_text
        }, status=200)



def msg(request):
    audios = AudioSaving.objects.all()
    context = {
        'audios': audios
    }
    return render(request, 'apps/msg/msg.html', context)