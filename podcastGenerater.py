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
target_language = input("\033[93m" + 'what is the language that you are currently learning? \n' + "\033[0m").upper()

storytext ="write me a story that is about" +input('what should the story be about (you are also allowed to leave this empty)\n') 
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
storytext = f" The story that you are about to write is written only in the language of  {target_language}. {storytext} {endtext}"
baselanguage = input("\033[93m" + 'what is the language that you want to have it teached? \n' + "\033[0m").upper()
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
    
def Introwriter(fullStory, targetLanguage, baseLanguage, level, ):
    promptForIntro =f"""Hi you are an excellent introduction writer for a a Podcast.
      I want that you write me an introduction for a language learning podcast that is for languagelearners  that are learning{targetLanguage} in the Level of {level}.
       The Introduction that you're writing should be written only in the {baseLanguage} and you should use no other languages.
        You should write an introduction that is about the following story: {fullStory}
        now that you know the full story keep in mind as the last sentence the listener will also hear this story in the language of {targetLanguage}
        so you should tell the listener something like "And now we're first going to listen to the full story" in {baseLanguage}.
        keep in mind to keep the introduction short and sweet."""
    currentStory =podcastgenerator(api_key, promptForIntro)
    return currentStory


fertigerPodcast = podcastgenerator(api_key, storytext)
print(fertigerPodcast)
print("\n \n")
print(Introwriter(storytext, target_language, baselanguage, level)["candidates"][0]["content"]["parts"][0]["text"])
print(fertigerPodcast["candidates"][0]["content"]["parts"][0]["text"])