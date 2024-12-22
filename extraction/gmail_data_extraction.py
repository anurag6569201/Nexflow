import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# API Configuration
API_KEY = "your_api_key_here"
ENDPOINT = "https://your-llm-endpoint.com/api"

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
                    "content": email_data,
                },
            ],
            "temperature": 0.6,
            "top_p": 0.9,
            "max_tokens": 1200,
        }

        # API call
        logging.info("Sending request to LLM API...")
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Raise HTTP errors for debugging
        logging.info("Received response from LLM API.")

        # Parse JSON response
        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return {"error": "API request failed", "details": str(e)}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse API response: {e}")
        return {"error": "Failed to parse API response", "details": str(e)}
