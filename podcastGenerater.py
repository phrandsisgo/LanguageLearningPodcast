import requests
import json
import keys as Keys


api_key = Keys.gemini_key
level = input('what is your level? \n')
print (f"your level is {level}" )
storytext =f"write me a story that is about {input('what should the story be about ')} that is very short( 5-6 sentences) that is also written in the level of {level}"
print(" \n ")
def podcastgenerator(api_key, text):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": text
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"
print(podcastgenerator(api_key, storytext))