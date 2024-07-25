import requests
import json
import re
from openAiPodcastGenerator import lang_differentiator, emptyPromptFunction
from gemini_functions import *
from savedocs import *

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
storyInput = input('\033[92m' + 'what should the story be about (do not leave this empty)' + '\033[0m')
print("\n \n ")
storyPrompt =f"I want you to write me a story in {target_language} that is about " +storyInput +f"be sure that the story is written in the level of {level} and using only wordsfrom the following language: {target_language}."
print(" \n ")
wordlist = ""
wordlist = input("\033[93m" + "do you have a wordlist of words that you're currently studying? if yes paste it in. \n" + "\033[0m")
print(" \n ")
endtext=""
open_ai_tokens = 0
if level!='N':
    endtext =f"{storyPrompt} that is also purely written in the level of {level} in {target_language}."
if wordlist !="":
    storytext = f"{storyPrompt} Make also sure that all words of the following wordlist are contained in the text {wordlist} and that it is written purely in {target_language}"
#add the language
storytext = f" The story that you are about to write is written only in the language of  {target_language}. {storytext} {endtext}"
baselanguage = input("\033[93m" + 'what is the language that you want to have it teached? \n' + "\033[0m").upper()




def Introwriter(fullStory, targetLanguage, baseLanguage, level, ):
    promptForIntro = f"""Hi, you are an excellent introduction writer for a Podcast.
      I want you to write me an introduction for a language learning podcast that is for language learners who are learning {targetLanguage} at the {level} level.
       The introduction should be written only in {baseLanguage} and should not include any other languages.
        You should write an introduction that is about the following story: "{fullStory}" .

        Now that you know the full story, keep in mind that as the last sentence, the listener will also hear this story in the language of {targetLanguage}.
        So, you should tell the listener something like "And now we're going to listen to the full story" in {baseLanguage}.
        Keep the introduction short and sweet."""
    introduction =podcastgenerator(api_key, promptForIntro)
    return introduction

def betweenPart(baselanguage, story):
    promptForBetween = f"""
    Hi, you are writing a part of a podcast for languagelearners and your part is the transition between the story and the explanation part of the story.
    You will be provided with a story and you should just mention a very brief summary of the story that the listener is about to hear. 
    before your part that you write the listener will hear the full story read in an normal speed. 
    Your job is to write a transition that is in the {baselanguage} language and that is a transition between the story and the explanation of the story.
    because after you the listener will hear the full story again but this time it's gonna be in a slower pace, and with translations and explenations for each sentence.

    The story of the podcast is the following: "{story}".

    Now that you know what the story is about answer only with the betweensection and nothing else. 
    And make sure to only use the {baselanguage} language in your answer.
    """
    inbetween_Part =podcastgenerator(api_key, promptForBetween)
    return inbetween_Part

def updateTokens(currentTokens, newTokens):
    currentTokens += newTokens
    return currentTokens

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


#finishedStory = podcastgenerator(api_key, storyPrompt)
finishedStory = emptyPromptFunction(storyPrompt)
isoBase = get_ISO(baselanguage)
isoTarget = get_ISO(target_language)
print(finishedStory)
if "candidates" in finishedStory:
    finishedStory = finishedStory["candidates"][0]["content"]["parts"][0]["text"]

ensure_output_directory()
storytitle = generateTitle(finishedStory, target_language)["candidates"][0]["content"]["parts"][0]["text"]
print("the title of the story is: " + storytitle)
filepath = generate_filename(storytitle)
create_empty_file(filepath, isoTarget, isoBase)
add_title(filepath, storytitle)
add_story(filepath, finishedStory)
add_wordList(filepath, wordlist)

print("\n \n")
#Intro
introText = Introwriter(finishedStory, target_language, baselanguage, level)
print(introText["candidates"][0]["content"]["parts"][0]["text"])
add_intro(filepath, introText["candidates"][0]["content"]["parts"][0]["text"])
#the story
print("\033[92m" + finishedStory + "\033[0m")
#between part(the transition between the story and the explenation of the story)
betweenPart = betweenPart(baselanguage, finishedStory)
print("\n"+ betweenPart["candidates"][0]["content"]["parts"][0]["text"])
add_betweenpart(filepath, betweenPart["candidates"][0]["content"]["parts"][0]["text"])
storySentences = re.split('[.!?]', finishedStory)

add_story(filepath, finishedStory)
#story explenation
def process_openai_object(openai_object):
    # Wandelt das OpenAIObject in einen JSON-String um
    json_str = json.dumps(openai_object)
    return json.loads(json_str)

for index, sentence in enumerate(storySentences, start=1):
    sentenceExplenation = singleTurnExplainer(sentence, isoBase, isoTarget, wordlist, level, finishedStory)
    print("\n")
    differentiated = lang_differentiator(sentenceExplenation, isoBase, isoTarget)

    # Verarbeite das OpenAIObject
    differentiated_json = process_openai_object(differentiated)

    differentiatedContent = differentiated_json["choices"][0]["message"]["content"]
    differentiatedCount = differentiated_json["usage"]["total_tokens"]

    print(f"Message: {differentiatedContent}")
    print(f"Token count: {differentiatedCount}")
    append_explanation(filepath, sentence, differentiatedContent, index)


#print("\n"+explainSentence(finishedStory["candidates"][0]["content"]["parts"][0]["text"], baselanguage, target_language, wordlist, level))

print("\n \n")
print("\033[92m" + "Now I should write an outro for the podcast" + "\033[0m")