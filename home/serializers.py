from rest_framework import serializers
from .models import AudioSaving

class AudioSavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioSaving
        fields = ['user', 'blob_url', 'date_time', 'uploaded_at']
