import os
import requests
import logging
from dotenv import load_dotenv
from django.shortcuts import get_object_or_404, render
from home.models import TextDetailing, AudioSaving
from datetime import timedelta

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.getenv('SPEECH_KEY')
ENDPOINT = "https://ai-anuragsingh65692019195ai682501652060.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

# Function to call the API and process the response
def call_text_analysis_api(transcription_text):
    try:
        headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY,
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Analyze the following text and extract all relevant and structured insights. "
                        "Organize the information into meaningful categories with clear and concise details. "
                        "The categories should include (but are not limited to):\n\n"
                        "1. **Meetings**: Capture the topic, time, participants, objectives, and additional details.\n"
                        "2. **Tasks**: Identify actionable items, descriptions, and deadlines.\n"
                        "3. **Plans**: Highlight future activities/events with timeframes/locations.\n"
                        "4. **Issues or Observations**: Note any challenges, observations, or reflections.\n"
                        "5. **Tests**: Include any testing efforts with their purpose, outcomes, or next steps.\n\n"
                        "Use your understanding to infer missing details and ensure the output is in JSON format."
                    )
                },
                {
                    "role": "user",
                    "content": transcription_text
                },
            ],
            "temperature": 0.6,
            "top_p": 0.9,
            "max_tokens": 1200
        }

        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        logger.error(f"Failed to make the request. Error: {e}")
        return None

# View to handle the processing and saving to the model
def process_and_save_text_detailing(request, audio_saving_id):
    audio_instance = get_object_or_404(AudioSaving, id=audio_saving_id)
    audio_instance_time=audio_instance.uploaded_at
    # Call the API with the audio's transcription text
    analysis_result = call_text_analysis_api(audio_instance.transcription_text)
    analysis_result = analysis_result['choices'][0]['message']['content']

    analysis_result['choices'][0]['message']['time_start'] = audio_instance_time
    analysis_result['choices'][0]['message']['time_end'] =  audio_instance_time + timedelta(minutes=10)

    if analysis_result:
        # Save the result to the TextDetailing model
        text_detailing = TextDetailing.objects.create(
            user=request.user if request.user.is_authenticated else None,
            text_detailing=audio_instance,
            output_text=analysis_result
        )
        logger.info(f"Text detailing saved successfully: {text_detailing.id}")

        return {
            "success": True,
            "message": "Text detailing processed and saved successfully.",
            "text_detailing_id": text_detailing.id
        }
    else:
        return {
            "success": False,
            "message": "Failed to process text detailing."
        }
