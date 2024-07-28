from google.cloud import texttospeech
import os
import sys
import requests
documentation = "https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#client-libraries-install-python"
# Replace 'your_api_key.json' with the path to your API key
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = texttospeech.TextToSpeechClient.from_service_account_json('your-api-key.json') # would be much nicer if we could use the keys.py file to simply put the api key here

try:
    import keys as Keys
    api_key = Keys.openai_key
    organization_id = Keys.openai_organization_id
    project_id = Keys.openai_project_id
except ImportError:
    api_key = input("Please enter your OpenAI API key: ")
    organization_id = input("Please enter your OpenAI organization ID: ")
    project_id = input("Please enter your OpenAI project ID: ")

def openai_tts(text, output_file="output.mp3"):
    # Setze die notwendigen Header
    headers = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Organization": organization_id,
        "OpenAI-Project": project_id,
        "Content-Type": "application/json"
    }

    # Setze die Daten für die Anfrage
    data = {
        "model": "tts-1",
        "voice": "nova",
        "input": text
    }

    # Sende die Anfrage
    response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=data)

    # Überprüfe die Antwort
    if response.status_code == 200:
        with open(f"{output_file}.mp3", "wb") as f:
            f.write(response.content)
        print("Text-to-Speech conversion completed. File saved as '{output_file}.mp3'.")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

def synthesize_text_RU(text, speed=0.9, path_name= None):
    synthesis_input = texttospeech.SynthesisInput(ssml=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ru-RU",  # Russian
        name="ru-RU-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
        pitch=-1.0,
    )

    # Send the request and get the response
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Get the current directory
    current_dir = os.getcwd()

    # Create the Audio folder if it doesn't exist
    audio_dir = os.path.join(current_dir, "Audio")
    os.makedirs(audio_dir, exist_ok=True)
    if path_name is None:
        # Get the number of existing audio files
        existing_files = len(os.listdir(audio_dir))
        # Generate the new file name
        new_file_name = f"{existing_files + 1}Test.mp3"
    else:
        new_file_name = f"{path_name}.mp3"

    output_file = os.path.join(audio_dir, new_file_name)

    # Save the response (as an MP3 file)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("Audioinhalt in 'output_file' geschrieben.")

    return output_file

def synthesize_text_ES(text, speed=0.9, path_name= None):
    # Text, der in Sprache umgewandelt werden soll
    # text = "Hallo,<break time='1.5s'/> wie geht es dir heute?"

    # Konfiguration der Anfrage
    synthesis_input = texttospeech.SynthesisInput(ssml=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="es-ES",  # British English
        name="es-ES-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
        pitch=-5.6
    )

    # Anfrage senden und Antwort erhalten
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Get the current directory
    current_dir = os.getcwd()

    # Create the Audio folder if it doesn't exist
    audio_dir = os.path.join(current_dir, "Audio")
    os.makedirs(audio_dir, exist_ok=True)
    if path_name is None:
        # Get the number of existing audio files
        existing_files = len(os.listdir(audio_dir))
        # Generate the new file name
        new_file_name = f"{existing_files + 1}Test.mp3"
    else:
        new_file_name = f"{path_name}.mp3"
    
    output_file = os.path.join(audio_dir, new_file_name)

    # Die Antwort speichern (als MP3-Datei)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("Audioinhalt in 'output_file' geschrieben.")

    return output_file

def synthesize_text_EN(inputText, speed=1, path_name= None):
    # Text, der in Sprache umgewandelt werden soll
    # text = "Hallo,<break time='1.5s'/> wie geht es dir heute?"

    # Konfiguration der Anfrage
    synthesis_input = texttospeech.SynthesisInput(ssml=inputText)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB",  # British English
        name="en-GB-Wavenet-B",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speed,
        pitch=-5.6
    )

    # Anfrage senden und Antwort erhalten
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    # Get the current directory
    current_dir = os.getcwd()

    # Create the Audio folder if it doesn't exist
    audio_dir = os.path.join(current_dir, "Audio")
    os.makedirs(audio_dir, exist_ok=True)

    if path_name is None:
        # Get the number of existing audio files
        existing_files = len(os.listdir(audio_dir))
        # Generate the new file name
        new_file_name = f"{existing_files + 1}Test.mp3"
    else:
        new_file_name = f"{path_name}.mp3"

    output_file = os.path.join(audio_dir, new_file_name)
    # Die Antwort speichern (als MP3-Datei)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("Audioinhalt in 'output_file' geschrieben.")
    return output_file

synthesize_text_RU("<speak>это было утомительно.</speak>", 0.5)