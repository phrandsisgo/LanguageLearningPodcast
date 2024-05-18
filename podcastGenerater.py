import requests
import json
import re

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

storyPrompt =f"I want you to write me a story in {target_language} that is about" +input('what should the story be about (do not leave this empty)') 
print(" \n \n ")
wordlist = ""
wordlist = input("\033[93m" + "do you have a wordlist of words that you're currently studying? if yes paste it in. \n" + "\033[0m")
print(" \n ")
endtext=""
if level!='N':
    endtext =f"{storyPrompt} that is also purely written in the level of {level} in {target_language}."
if wordlist !="":
    storytext = f"{storyPrompt} make sure that all words of the following wordlist are contained in the text {wordlist} and that it is written purely in {target_language}"
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
    promptForIntro = f"""Hi, you are an excellent introduction writer for a Podcast.
      I want you to write me an introduction for a language learning podcast that is for language learners who are learning {targetLanguage} at the {level} level.
       The introduction should be written only in {baseLanguage} and should not include any other languages.
        You should write an introduction that is about the following story: {fullStory}.
        Now that you know the full story, keep in mind that as the last sentence, the listener will also hear this story in the language of {targetLanguage}.
        So, you should tell the listener something like "And now we're going to listen to the full story" in {baseLanguage}.
        Keep the introduction short and sweet."""
    introduction =podcastgenerator(api_key, promptForIntro)
    return introduction

def betweenPart(baselanguage):
    promptForBetween = f"""Hi, you are writing a part of a podcast.
    your job is it to translate the following sentence in the language of {baselanguage}:
    "you heard now the full story, wow I hope there were a few words that you understood and some that are completely new to you. let's go over each sentence now and learn them together. " """
    inbetween_Part =podcastgenerator(api_key, promptForBetween)
    return inbetween_Part

def explainSentence(fullstory, baseLanguage, targetLanguage, wordlist=None, level=None):
    sentences = re.split('[.!?]', fullstory)
    promptForExplanation = ""
    combineedExplanations = ""
    print("\033[91m" + str(sentences) + "\033[0m")
    print("\033[91m" + " \n those should've been the sentences" + "\033[0m")
    if wordlist:
        for sentence in sentences:
            promptForExplanation = f"""
            Hi, you are an excellent teacher for foreign languages and are an expert to distinguish the languages from each other, for a podcast.
            You will be given a sentence from a story that is written in the language of {targetLanguage}.
            Your job is to explain the sentence in the language of {baseLanguage}.
            I want you to explain the sentence in a way that a language learner who is learning {targetLanguage} at the {level} level would understand and also learn something from it.
            If a word from the wordlist is being used in the sentence, you should explain it extra carefully and put more emphasis on it by using it in other sentences as well.
            You will be given the following sentence: "{sentence}".
            If none of the words from the wordlist are used in the sentence, you should explain another word that might be challenging for someone at the {level} level.
            Here is the wordlist that the listener is currently learning: "{wordlist}".
            Please try to only write 3-5 sentences as a explanation. for the sentence that you are given."""
            currentExplanation = podcastgenerator(api_key, promptForExplanation)["candidates"][0]["content"]["parts"][0]["text"]
            combineedExplanations = combineedExplanations + currentExplanation
            print("\033[91m" + currentExplanation + "\033[0m")
            print("\n\n")
            print("next phrase (with wordlist)")
            

    else:
        for sentence in sentences:
            promptForExplanation = f"""Hi, you are an excellent teacher for foreign languages, for a podcast.
            You will be given a sentence from a story that is written in the language of {targetLanguage}.
            Your job is to explain the sentence in the language of {baseLanguage}.
            I want you to explain the sentence in a way that a language learner who is learning {targetLanguage} at the {level} level would understand and also learn something from it.
            You will be given the following sentence: "{sentence}".
            If none of the words from the wordlist are used in the sentence, you should explain another word that might be challenging for someone at the {level} level."""
            currentExplanation = podcastgenerator(api_key, promptForExplanation)["candidates"][0]["content"]["parts"][0]["text"]
            combineedExplanations = combineedExplanations + currentExplanation
            print("\033[91m" + currentExplanation + "\033[0m")
            print("\n\n")
            print("next phrase")
    
    return combineedExplanations
    

fertigerPodcast = podcastgenerator(api_key, storyPrompt)
print(fertigerPodcast)
print("\n \n")
print(Introwriter(storytext, target_language, baselanguage, level)["candidates"][0]["content"]["parts"][0]["text"])
print("\033[92m" + fertigerPodcast["candidates"][0]["content"]["parts"][0]["text"] + "\033[0m")
print("\n"+betweenPart(baselanguage)["candidates"][0]["content"]["parts"][0]["text"])
print("\n"+explainSentence(fertigerPodcast["candidates"][0]["content"]["parts"][0]["text"], baselanguage, target_language, wordlist, level))