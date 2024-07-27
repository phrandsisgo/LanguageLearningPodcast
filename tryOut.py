import requests

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
        with open(f"output/{output_file}.mp3", "wb") as f:
            f.write(response.content)
        print(f"Text-to-Speech conversion completed. File saved as 'output/{output_file}.mp3'.")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
openai_tts("Hallo ich wollte nachfragen was du heute machst.","find" )