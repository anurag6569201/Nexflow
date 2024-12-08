from rest_framework import serializers
from .models import AudioSaving


class AudioSavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioSaving
        fields = ['id', 'user', 'audio_file', 'date_time', 'uploaded_at']
        read_only_fields = ['date_time', 'uploaded_at']
