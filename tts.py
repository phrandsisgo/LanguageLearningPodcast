from google.cloud import texttospeech
import os
import sys
import requests
documentation = "https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#client-libraries-install-python"
# Replace 'your_api_key.json' with the path to your API key
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = texttospeech.TextToSpeechClient.from_service_account_json('linguatech-tts.json') 

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

    # Save the answer (as MP3-File)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("Audioinhalt in 'output_file' geschrieben.")

    return output_file

def synthesize_text_EN(inputText, speed=1, path_name= None):

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
    # Save the answer (as MP3-File)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("Audioinhalt in 'output_file' geschrieben.")
    return output_file

def synthesize_text_DE(inputText, speed=1, path_name= None):
        synthesis_input = texttospeech.SynthesisInput(ssml=inputText)
        voice = texttospeech.VoiceSelectionParams(
            language_code="de-DE",  # German
            name="de-DE-Polyglot-1",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed,
            pitch=-0.50
        )

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
            existing_files = len(os.listdir(audio_dir))
            new_file_name = f"{existing_files + 1}Test.mp3" # Generate the new file name
        else:
            new_file_name = f"{path_name}.mp3"

        output_file = os.path.join(audio_dir, new_file_name)
        # Save the answer (as MP3-File)
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
            print("audio written to 'output_file'.")
        return output_file

def synthesize_text_FR(inputText, speed=1, path_name= None):
        synthesis_input = texttospeech.SynthesisInput(ssml=inputText)
        voice = texttospeech.VoiceSelectionParams(
            language_code="fr-FR",  # French
            name="fr-FR-Polyglot-1",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed,
            pitch=-0.50
        )
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        current_dir = os.getcwd()# Get the current directory

        # Create the Audio folder if it doesn't exist
        audio_dir = os.path.join(current_dir, "Audio")
        os.makedirs(audio_dir, exist_ok=True)

        if path_name is None:
            existing_files = len(os.listdir(audio_dir))
            new_file_name = f"{existing_files + 1}Test.mp3" # Generate the new file name
        else:
            new_file_name = f"{path_name}.mp3"

        output_file = os.path.join(audio_dir, new_file_name)
        # Save the answer (as MP3-File)
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
            print("audio written to 'output_file'.")
        return output_file

def synthesize_text_PT(inputText, speed=1, path_name= None):
        synthesis_input = texttospeech.SynthesisInput(ssml=inputText)
        voice = texttospeech.VoiceSelectionParams(
            language_code="pt-BR",  # Portuguese
            name="pt-BR-Wavenet-D",
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speed,
            pitch=-2.80
        )
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        current_dir = os.getcwd()# Get the current directory

        # Create the Audio folder if it doesn't exist
        audio_dir = os.path.join(current_dir, "Audio")
        os.makedirs(audio_dir, exist_ok=True)

        if path_name is None:
            existing_files = len(os.listdir(audio_dir))
            new_file_name = f"{existing_files + 1}Test.mp3" # Generate the new file name
        else:
            new_file_name = f"{path_name}.mp3"

        output_file = os.path.join(audio_dir, new_file_name)
        # Save the answer (as MP3-File)
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
            print("audio written to 'output_file'.")
        return output_file
# languages available so far: EN, DE, ES, RU , FR, PT
synthesize_text_PT("<speak>Quando tem feijoada na casa de Maria, ela convida alguns amigos para almoçar junto com ela.</speak>", 0.8, "hallo pt") # Test