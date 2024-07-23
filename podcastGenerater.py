import requests
import json
import re
from openAiPodcastGenerator import lang_differentiator
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
        You should write an introduction that is about the following story: "{fullStory}" .

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


def explainSentence1(fullstory, baseLanguage, targetLanguage, wordlist=None, level=None):
    sentences = re.split('[.!?]', fullstory)
    #sentences = re.findall(r'[^.!?]+[.!?]', fullstory) ## With this the punctuation is included in the sentence.
    promptForExplanation = ""
    combineedExplanations = ""
    print("\033[91m" + str(sentences) + "\033[0m")
    print("\033[91m" + " \n those should've been the sentences" + "\033[0m")
    if wordlist:
        for sentence in sentences:
            promptForExplanation = f"""
            As an expert language teacher for a podcast, explain the following sentence from a {targetLanguage} story to a {level} level learner of {targetLanguage}. The explanation should be in {baseLanguage}.

            full story for context: "{fullstory}"

            Current sentence to explain: "{sentence.strip()}"

            Guidelines:
            1. Start with a smooth transition (e.g., "Let's move on to the next part." or "Now, we encounter an interesting phrase.")
            2. Explain the sentence, focusing on its meaning and any challenging words or structures.
            3. If the sentence contains words from this list: {wordlist}, provide extra explanation and examples.
            4. Include cultural notes or usage tips if relevant.
            5. Aim for a concise yet informative explanation (maximum should be 7 sentences that you use and don't go over that threshhold).
            6. End with a brief summary or a question to engage the listener.

            Remember, your explanation should flow naturally as part of a podcast, maintaining listener engagement between sentences.
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
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    promptForDifferentiator = f"""
        You're an excellent for when it comes to differentiating languages from each other for a podcast.
        Make sure to give the answer with separators (---) when switching languages to separate the languages one from another.
        Always when using a Separator, you will start the sentence with the correct ISO-code of the language that you're writing in.
        Do it as it is shown in the example below.
        Be sure to always use the correct ISO-code for the language that you're writing in (always use the correct one that is provided by me).
        Only return the separated text with the correct ISO-code for the language that you're writing in.
        The text you're writing will be later separated by a regex function that will separate the text by the ISO-code.
        make sure that you always pick the correct language even if it is for only a single word.

        the first sentence that you need to differentiate is the following: the Sentence, "Я на улице!" means I'm outside. However, "на улице" can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, "на улице" has 2 meanings.
   

    """
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": promptForDifferentiator #muss noch umgeschrieben werden
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": """ ---EN the Sentence, ---RU Я на улице ---EN means I'm outside. However, ---RU на улице ---EN can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, ---RU на улице ---EN has 2 meanings."""
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": """ "Was läuft bei dir Junge?" means "what's up with you, boy?" in English if we want to be literal. But you can also translate it as: "what's up dude" it is usually used in informal settings. But literally the word "läuft" means walking and "Junge" means boy. One last time the full sentence: "Was läuft bei dir Junge?"' / targetLanguage: 'DE' / explainLanguage: 'EN'"""
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": """ ---DE Was läuft bei dir Junge? ---EN means 'What's up with you, boy?' in English if we want to be literal. But you can also translate it as: 'what's up dude' it is usually used in informal settings. But literally the word ---DE "läuft" ---EN means walking and ---DE Junge ---EN means boy. One last time the full sentence: ---DE Was läuft bei dir Junge? """
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": """ "Je suis dans la cuisine" bedeutet "Ich bin in der Küche" auf Deutsch. Das Wort "cuisine" bedeutet "Küche". noch einmal der ganzer Satz zur Wiederholung:  "Je suis dans la cuisine" ' / targetLanguage: 'FR' / explainLanguage: 'DE'"""
                    }
                ]
            },
            {
                "role": "model",
                "parts": [
                    {
                        "text": """ ---FR Je suis dans la cuisine ---DE bedeutet 'Ich bin in der Küche' auf Deutsch. Das Wort ---FR "cuisine" ---DE bedeutet 'Küche'. noch einmal der ganzer Satz zur Wiederholung: ---FR "Je suis dans la cuisine" """
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"""{story}" in the language of "{baseLanguage}" and "{targetLanguage}" """
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
    #return differentiator["candidates"][0]["content"]["parts"][0]["text"]

def multiTurnExplainer(sentence, baseIso, targetIso, wordList, level):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    startPrompt = f"""
    Hi, you are an excellent teacher for foreign languages and are an expert to distinguish the languages from each other, for a podcast.
    Your explanations should be written in the desired explain language only. 
    You will be given a sentence from a story that is written in the target language that the user is currently learning.
    Your job is to explain the sentence in the explainin language in a way that it sutes the user quite good and he can learn it.
    Do it in a way, so that the user has to guess a word that might be challenging for someone at his level, do it in a way to describe the word without instantly translating it, But don't do it if the sentence is super easy in his level.

   And to give you a step by step guide on how to do it. here's a step by step guide:
    1. Start with the sentence that you are given. and read it in the language of the target language.
    2. if the sentence is super easy for the targeted level of the learner, then you can just explain the sentence in the language of the explain language and also add a simple translation.
    3. If the sentence is a bit more challenging, then you should explain the sentence in the language of the explain language and give also some examples on where the sentence might be used in other circumstances.
    4. If the sentence contains a word from the wordlist, also give some examples on how the word could be used in other sentences.
    5. End it with a simple translation of the sentence in the language of the explain language. followed by saying "next sentence" in the explain language. (so it can be used in a Loop for a podcast)

    So for your first sentence, I want you to explain the following sentence: "Je coupe les légumes pour la soupe" from the target language "FR" explained in the "DE" language. for the Level A2 and the wordlist is the following "[
    "Ingrédients (Zutaten)",
    "Recette (Rezept)",
    "Cuisiner (kochen)",
    "Éplucher (schälen)",
    "Couper (schneiden)",
    "Mélanger (mischen)",
    "Bouillir (sieden, kochen)",
    
    
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
                        "text": """Je coupe les légumes pour la soupe. Bei Ihnen das Wort "coupe" vorkommt konzentrieren wir uns zuerst darauf.
                         das Wort "coupe" kann auch in Sätzen wie "tu coupes une pomme" also "du schneidest ein Apfel  oder "il coupe le pain" was so viel bedeutet wie "er schneidet das Brot" verwendet werden.
                         Also in deinem Satz wäre "Ich und dann etwas das Gemüse für die Suppe".  
                         Wie du es vielleicht schon erraten hast, bedeutet "coupe" schneiden.
                        Also zusammengefasst bedeutet der Satz "Ich schneide das Gemüse für die Suppe" 
                         """
                    }
                ]
            },
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"""As a next sentence I want you to explain the following sentence: "{sentence}" from the target language {targetIso} explained in the {baseIso} language
                        and this is the wordlist that the user is currently learning: "{wordList}" and the level that the user is learning is {level}"""
                    }
                ]
            },
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}" 
    
def generateTitle(story, language):
    startPrompt = f"""
    Hi, you are an excellent title writer for a podcast.
    Your job is to generate a title for a language learning podcast.
    That title should be in the {language} language and should be a title to the following story:
    "{story}".
    """
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": startPrompt}]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print(f"Title of the story is: {response.json()['candidates'][0]['content']['parts'][0]['text']}")
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"


def singleTurnExplainer(sentence, baseIso, targetIso, wordList, level, fullStory):
    startPrompt = f"""
            As an expert language teacher for a podcast, explain the following sentence from a {targetIso} story to a {level} level learner of {targetIso}. The explanation should be in {baseIso}.

            for context here's the full story for context: {fullStory}

            Current sentence to explain: "{sentence}"

            Guidelines:
            1. Start with a smooth transition (e.g., "Let's move on to the next part." or "Now, we encounter an interesting phrase.")
            2. Explain the sentence, focusing on its meaning and any challenging words or structures.
            3. If the sentence contains words from this list: {wordlist}, provide extra explanation and examples.
            4. Include cultural notes or usage tips if relevant.
            5. Aim for a concise yet informative explanation (maximum 7 sentences please don't go over that threshhold).
            6. End with a brief summary or a question to engage the listener.
            7. Also try your best to not give any helps on how the words are supposed to sound like phonetically.
            8. Super important is that you only use the languages {baseIso} and {targetIso} in the explanation and nothing else.
            9. At least once the sentence should come fully translated in the language of {baseIso}.

            Remember, your explanation should flow naturally as part of a podcast, maintaining listener engagement between sentences.
            """
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": startPrompt}]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"

finishedStory = podcastgenerator(api_key, storyPrompt)
isoBase = get_ISO(baselanguage)
isoTarget = get_ISO(target_language)
print(finishedStory)

ensure_output_directory()
storytitle = generateTitle(finishedStory["candidates"][0]["content"]["parts"][0]["text"], target_language)["candidates"][0]["content"]["parts"][0]["text"]
print("the title of the story is: " + storytitle)
filepath = generate_filename(storytitle)
create_empty_file(filepath, isoTarget, isoBase)
add_story(filepath, finishedStory["candidates"][0]["content"]["parts"][0]["text"])

print("\n \n")
#Intro
finishedStory =finishedStory["candidates"][0]["content"]["parts"][0]["text"]
introText = Introwriter(finishedStory, target_language, baselanguage, level)
print(introText["candidates"][0]["content"]["parts"][0]["text"])
add_intro(filepath, introText["candidates"][0]["content"]["parts"][0]["text"])
#the story
print("\033[92m" + finishedStory + "\033[0m")
#between part(the transition between the story and the explenation of the story)
print("\n"+betweenPart(baselanguage)["candidates"][0]["content"]["parts"][0]["text"])
storySentences = re.split('[.!?]', finishedStory)

add_story(filepath, finishedStory)
#story explenation
def process_openai_object(openai_object):
    # Wandelt das OpenAIObject in einen JSON-String um
    json_str = json.dumps(openai_object)
    return json.loads(json_str)

for sentence in storySentences:
    sentenceExplenation = singleTurnExplainer(sentence, isoBase, isoTarget, wordlist, level, finishedStory)
    print("\n")
    differentiated = lang_differentiator(sentenceExplenation, isoBase, isoTarget)

    # Verarbeite das OpenAIObject
    differentiated_json = process_openai_object(differentiated)

    differentiatedContent = differentiated_json["choices"][0]["message"]["content"]
    differentiatedCount = differentiated_json["usage"]["total_tokens"]

    print(f"Message: {differentiatedContent}")
    print(f"Token count: {differentiatedCount}")


#print("\n"+explainSentence(finishedStory["candidates"][0]["content"]["parts"][0]["text"], baselanguage, target_language, wordlist, level))

print("\n \n")
print("\033[92m" + "Now I should write an outro for the podcast" + "\033[0m")