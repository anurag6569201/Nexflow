import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

def recognize_from_audio_file():
    # Load environment variables for Azure Speech Service
    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv('SPEECH_TO_TEXT_RESOURCE_KEY'),
        region=os.getenv('SPEECH_TO_TEXT_SERVICE_REGION')
    )
    speech_config.speech_recognition_language = "en-IN"

    # Path to your audio file
    audio_file_path = '/Users/anuragsingh/Documents/GitHub/TrackIT/media/audio_files/output.wav'

    # Configure the audio file input
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Recognizing speech from audio file...")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    # Handle the recognition results
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

recognize_from_audio_file()
