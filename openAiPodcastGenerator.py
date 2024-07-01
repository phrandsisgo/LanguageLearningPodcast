import requests
import json
import re
from openai import OpenAI

try:
    import keys as Keys
    api_key = Keys.gemini_key
except ImportError:
    api_key = input("Please enter your OpenAI API key: ")

client = OpenAI(api_key=api_key)

level = input("\033[93m" + 'what is your language level? \n' + "\033[0m").upper()

while level not in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'N']:
    print("\033[91m" + 'Invalid level. Please enter a level between A1 and C2. Please enter something like A1, A2, B1, B2, C1, C2 or n for none' + "\033[0m")
    level = input('what is your  the level that you are learning your language? \n').upper()
print("\033[92m" + f"your level is {level}" + "\033[0m")
target_language = input("\033[93m" + 'what is the language that you are currently learning? \n' + "\033[0m").upper()

storyInput = input('\033[92m' + 'what should the story be about (do not leave this empty)' + '\033[0m')
storyPrompt =f"I want you to write me a story in {target_language} that is about" +storyInput 
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
print(" \n \n ")

def Introwriter(fullStory, targetLanguage, baseLanguage, level, ):
    promptForIntro = f"""Hi, you are an excellent introduction writer for a Podcast.
      I want you to write me an introduction for a language learning podcast that is for language learners who are learning {targetLanguage} at the {level} level.
       The introduction should be written only in {baseLanguage} and should not include any other languages.
        You should write an introduction that is about the following story: {fullStory}.
        Now that you know the full story, keep in mind that as the last sentence, the listener will also hear this story in the language of {targetLanguage}.
        So, you should tell the listener something like "And now we're going to listen to the full story" in {baseLanguage}.
        Keep the introduction short and sweet."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a conversation designer."},
            {"role": "user", "content": promptForIntro},
        ],
    )
    return response

def emptyPromptFunction(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response
def lang_differentiator(sentence, baselanguage, targetlanguage):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-instruct",
        messages=[
            {"role": "system", "content": """
            You're an excellent for when it comes to differentiating languages from each other for a podcast.
            Make sure to give the answer with separators (---) when switching languages to separate the languages one from another.
            Always when using a Separator, you will start the sentence with the correct ISO-code of the language that you're writing in.
            Do it as it is shown in the example below.
            Be sure to always use the correct ISO-code for the language that you're writing in (always use the correct one that is provided by me).
            Only return the separated text with the correct ISO-code for the language that you're writing in.
            The text you're writing will be later separated by a regex function that will separate the text by the ISO-code.
            make sure that you always pick the correct language even if it is for only a single word.


            """},
            {"role": "user", "content": f""" the first sentence that you need to differentiate is the following: the Sentence, "Я на улице!" means I'm outside. However, "на улице" can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, "на улице" has 2 meanings. /targetLanguage: 'RU' /explainLanguage:'EN' """ },

            {"role": "assistant", "content": f""" ---EN the Sentence, ---RU Я на улице ---EN means I'm outside. However, ---RU на улице ---EN can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, ---RU на улице ---EN has 2 meanings. """},

            {"role": "user", "content": f""""Was läuft bei dir Junge?" means "what's up with you, boy?" in English if we want to be literal. But you can also translate it as: "what's up dude" it is usually used in informal settings. But literally the word "läuft" means walking and "Junge" means boy. One last time the full sentence: "Was läuft bei dir Junge?"' / targetLanguage: 'DE' / explainLanguage: 'EN' """}, 

            {"role": "assistant", "content": f""" ---DE "Was läuft bei dir Junge?" ---EN means 'What's up with you, boy?' in English if we want to be literal. But you can also translate it as: 'what's up dude' it is usually used in informal settings. But literally the word ---DE "läuft" ---EN means walking and ---DE Junge ---EN means boy. One last time the full sentence: ---DE Was läuft bei dir Junge? """},

            {"role": "user", "content": f"""Here's the sentence that you need to differentiate: "{sentence}" in the language of "{baselanguage}" and "{targetlanguage}""" },

        ],
    )
    return response
    return response
print(emptyPromptFunction(storytext))