import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import tempfile

load_dotenv()

def transcribe(audio_file):
    # Load Azure Speech configuration
    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv('SPEECH_KEY'),
        region=os.getenv('SPEECH_REGION')
    )
    speech_config.speech_recognition_language = "en-IN"

    # Save the uploaded audio file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        for chunk in audio_file.chunks():
            temp_audio_file.write(chunk)
        temp_audio_path = temp_audio_file.name

    # Configure audio input
    audio_config = speechsdk.audio.AudioConfig(filename=temp_audio_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    transcription = []
    done = False

    # Event handlers
    def handle_recognized(evt):
        transcription.append(evt.result.text)

    def handle_canceled(evt):
        nonlocal done
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {evt.error_details}")
        done = True

    def handle_session_stopped(evt):
        nonlocal done
        done = True

    # Attach event handlers
    speech_recognizer.recognized.connect(handle_recognized)
    speech_recognizer.canceled.connect(handle_canceled)
    speech_recognizer.session_stopped.connect(handle_session_stopped)

    try:
        print("Starting transcription...")
        speech_recognizer.start_continuous_recognition()

        # Wait for transcription to finish
        import time
        while not done:
            time.sleep(0.5)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Stop and clean up the recognizer
        speech_recognizer.stop_continuous_recognition()
        del speech_recognizer
        print("Stopped recognition.")

        # Ensure temporary file cleanup
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

    # Combine transcription results
    print(transcription)
    return " ".join(transcription)
