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
    #sentences = re.findall(r'[^.!?]+[.!?]', fullstory) ## With this the punctuation is included in the sentence.
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
            Please try to only write 3-5 sentences as a explanation. for the sentence that you are given.
            When you have done that I will need you to differenciate the text by language. (so that in the production will know which language there is to use)
            """
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


def get_ISO(input):
    print(api_key)
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    starting_prompt = """ 
    
    """
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"""I want you to just return the code of the language with 2 leters of the ISO-Code of the language that is beeing inputted standard. The first input that you need to return is now "japanisch" """
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": "JP"
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"the input is {input}"
                    }
                ]
            },
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        if response.json()["candidates"][0]["content"]["parts"][0]["text"] == "JA":
            response.json()["candidates"][0]["content"]["parts"][0]["text"] = "JP" #found out during testing that the API returns the wrong code for Japanese
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}" 

def differentiator(story, baseLanguage, targetLanguage):
    promptForDifferentiator = f"""
        You're an excellent teacher who explains sentences in an engaging way.
        Your explanations should be written in {baseLanguage} only.
        You will be given a sentence and you will explain it in the {baseLanguage} (baseLanguage).
        Make sure to give the answer with separators (---) when switching languages to separate the languages one from another.
        Always when using a Separator, you will start the sentence with either a "bl" for baseLanguage (that is the language you're explaining in) or "tl" for targetLanguage (which is the language the sentence is in).
        You're always explaining the sentence in {baseLanguage}.
        As soon as you separated the phrase with the --- separator and have a bl then ONLY write in the {baseLanguage}.
        This is so that later on the base & target Language can be separated from each other.
        You will exclusively explain the sentence in {baseLanguage}.
        You will for every sentence focus on a word that could be special in the sentence and explain that as well in the {baseLanguage}.
        Make sure to write the sentence multiple times in your answer.
        When you're writing a bl section, make sure to only use the {baseLanguage} and not use the target language.
        When you're writing a tl section, make sure to only use the targetLanguage that is given by the text and not use the {baseLanguage}.
        Do not just repeat the sentence in {baseLanguage}, try to come up with a valuable explanation, maybe with an interesting fun fact or something.
        Keep in mind that after your explanation, the listener will hear the next sentence and the explanation of that sentence.

        Examples:
        Sentence: 'Я на улице!' / targetLanguage: Russian
        Explanation: ---RU Я на улице ---EN the Sentence, ---RU Я на улице ---EN means I'm outside. However, ---RU на улице ---EN can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, ---RU на улице ---EN has 2 meanings.
        
        Sentence: 'Was läuft bei dir Junge?' / targetLanguage: German
        Explanation: ---DE Was läuft bei dir Junge? ---EN means 'What's up with you, boy?' in English if we want to be literal. But you can also translate it as: 'what's up dude' it is usually used in informal settings. But literally the word ---DE läuft ---EN means walking and ---DE Junge ---EN means boy. One last time the full sentence: ---DE Was läuft bei dir Junge?
    """

def multiTurnExplainer(sentence, baseIso, targetIso, wordList, level):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    startPrompt = f"""
    Hi, you are an excellent teacher for foreign languages and are an expert to distinguish the languages from each other, for a podcast.
    Your explanations should be written in the desired explain language only. 
    You will be given a sentence from a story that is written in the target language that the user is currently learning.
    Your job is to explain the sentence in the explainin language in a way that it sutes the user quite good and he can learn it.
    Do it in a way, so that the user has to guess a word that might be challenging for someone at his level, do it in a way to describe the word without instantly translating it, But don't do it if the sentence is super easy in his level.
    If a word from the wordlist is being used in the sentence, you should explain it extra carefully and put more emphasis on it by using it in other sentences as well.
            I want you to explain the sentence in a way that a language learner who is learning the target language  at the {level} level would understand and also learn something from it.
            If a word from the wordlist is being used in the sentence, you should explain it extra carefully and put more emphasis on it by using it in other sentences as well.
            You will be given the following sentence: "{sentence}".
            If none of the words from the wordlist are used in the sentence, you should explain another word that might be challenging for someone at the {level} level.
            Here is the wordlist that the listener is currently learning: "{wordList}".
            Please try to only write 3-5 sentences as a explanation. for the sentence that you are given.
            When you have done that I will need you to differenciate the text by language. (so that in the production will know which language there is to use)
    the first sentence that you will be given is: "Hallo wie geht es dir?"
    
    """
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": startPrompt
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": "In the bustling city of Meadow brook, lived a young girl named Sophie. She was a bright and curious soul with an imaginative mind."
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": "Can you set it in a quiet village in 1600s France?"
                    }
                ]
            },
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}" 
    

fertigerPodcast = podcastgenerator(api_key, storyPrompt)
isoBase = get_ISO(baselanguage)
isoTarget = get_ISO(target_language)
print(fertigerPodcast)
print("\n \n")
print(Introwriter(storytext, target_language, baselanguage, level)["candidates"][0]["content"]["parts"][0]["text"])
print("\033[92m" + fertigerPodcast["candidates"][0]["content"]["parts"][0]["text"] + "\033[0m")
print("\n"+betweenPart(baselanguage)["candidates"][0]["content"]["parts"][0]["text"])
print("\n"+explainSentence(fertigerPodcast["candidates"][0]["content"]["parts"][0]["text"], baselanguage, target_language, wordlist, level))