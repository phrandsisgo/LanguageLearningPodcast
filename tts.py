from google.cloud import texttospeech
import os
import sys
documentation = "https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#client-libraries-install-python"
# Replace 'your_api_key.json' with the path to your API key
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = texttospeech.TextToSpeechClient.from_service_account_json('your-api-key.json') # would be much nicer if we could use the keys.py file to simply put the api key here

def synthesize_text_RU(text, speed=0.9):
    # Text to be converted to speech
    # text = "Hello,<break time='1.5s'/> how are you today?"

    # Configuration of the request
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

    # Get the number of existing audio files
    existing_files = len(os.listdir(audio_dir))
    # Generate the new file name
    new_file_name = f"{existing_files + 1}Test.mp3"
    output_file = os.path.join(audio_dir, new_file_name)

    # Save the response (as an MP3 file)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print("Audioinhalt in 'output_file' geschrieben.")

    return output_file

synthesize_text_RU("<speak>это было утомительно.</speak>", 0.5)