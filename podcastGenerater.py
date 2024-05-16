import requests
import json


try:
    import keys as Keys
    api_key = Keys.gemini_key
except ImportError:
    api_key = input("Please enter your gemini API key: ")

level = input("\033[93m" + 'what is your level? \n' + "\033[0m").upper()
while level not in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'N']:
    print("\033[91m" + 'Invalid level. Please enter a level between A1 and C2. Please enter something like A1, A2, B1, B2, C1, C2 or n for none' + "\033[0m")
    level = input('what is your  the level that you are learning your language? \n').upper()
print("\033[92m" + f"your level is {level}" + "\033[0m")
language = input("\033[93m" + 'what is the language that you are currently learning? \n' + "\033[0m").upper()

storytext =f"write me a story that is about {input('what should the story be about (you are also allowed to leave this empty)')}  "
print(" \n ")
wordlist = ""
wordlist = input("\033[93m" + "do you have a wordlist of words that you're currently studying? if yes paste it in. \n" + "\033[0m")
print(" \n ")
endtext=""
if level!='N':
    endtext =f"{storytext} that is also purely written in the level of {level}."
if wordlist !="":
    storytext = f"{storytext} make sure that all words of the following wordlist are contained in the text {wordlist}"
#add the language
storytext = f" The story that you are about to write is written only in the language of  {language}. {storytext} {endtext}"
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