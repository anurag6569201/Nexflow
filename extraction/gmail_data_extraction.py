import requests
import os
import json
import logging
from django.shortcuts import get_object_or_404, render
from extraction.models import EmailDetailing
import os
import requests
import logging
from dotenv import load_dotenv
from django.shortcuts import get_object_or_404, render

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.getenv('SPEECH_KEY')
ENDPOINT = "https://ai-anuragsingh65692019195ai682501652060.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"

def call_gmail_analysis_api(email_data):
    """
    Analyzes email content using an LLM API and extracts structured insights.
    
    Args:
        email_data (str): Raw email content as a string.
        
    Returns:
        dict: Parsed and structured JSON response with categorized insights.
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY,
        }

        # Request payload
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Analyze the following gmail. "
                        "Organize the information into meaningful categories with clear and concise details. "
                        "The categories should include (but are not limited to):\n\n"
                        "1. **Meetings**: Capture the topic, time, participants, objectives, and additional details.\n"
                        "2. **Tasks**: Identify actionable items, descriptions, and deadlines.\n"
                        "3. **Plans**: Highlight future activities/events with timeframes/locations.\n"
                        "4. **Issues or Observations**: Note any challenges, observations, or reflections.\n"
                        "5. **Tests**: Include any testing efforts with their purpose, outcomes, or next steps.\n\n"
                        "6. **Labels**: Categorize emails based on labels and provide insights on email distribution.\n"
                        "7. **Summarize**: Summarize the email body and dont add body data in response.\n"
                        "Use your understanding to infer missing details and ensure the output is in JSON format."
                    ),
                },
                {
                    "role": "user",
                    "content": f'''{email_data}''',
                },
            ],
            "temperature": 0.6,
            "top_p": 0.9,
            "max_tokens": 1200,
        }

        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        logger.error(f"Failed to make the request. Error: {e}")
        return None


def process_and_save_gmail_detailing(request, gmails_data):
    analysis_result = call_gmail_analysis_api(gmails_data)
    analysis_result = analysis_result['choices'][0]['message']['content']

    if analysis_result:
        # Save the result to the TextDetailing model
        emails_detailing = EmailDetailing.objects.create(
            user=request.user if request.user.is_authenticated else None,
            output_text=analysis_result
        )
        logger.info(f"Email detailing saved successfully: {emails_detailing.id}")

        return {
            "success": True,
            "message": "Email detailing processed and saved successfully.",
            "emails_detailing_id": emails_detailing.id
        }
    else:
        return {
            "success": False,
            "message": "Failed to process Email detailing."
        }
