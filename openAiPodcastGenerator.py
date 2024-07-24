import requests
import json
import openai
try:
    import keys as Keys
    api_key = Keys.openai_key
    organization_id = Keys.openai_organization_id
    project_id = Keys.openai_project_id
except ImportError:
    api_key = input("Please enter your OpenAI API key: ")
    organization_id = input("Please enter your OpenAI organization ID: ")
    project_id = input("Please enter your OpenAI project ID: ")


openai.api_key = api_key
headers = {
    "Authorization": f"Bearer {api_key}",
    "OpenAI-Organization": organization_id,
    "OpenAI-Project": project_id,
}
"""
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
"""
def Introwriter(fullStory, targetLanguage, baseLanguage, level, ):
    promptForIntro = f"""Hi, you are an excellent introduction writer for a Podcast.
      I want you to write me an introduction for a language learning podcast that is for language learners who are learning {targetLanguage} at the {level} level.
       The introduction should be written only in {baseLanguage} and should not include any other languages.
        You should write an introduction that is about the following story: {fullStory}.
        Now that you know the full story, keep in mind that as the last sentence, the listener will also hear this story in the language of {targetLanguage}.
        So, you should tell the listener something like "And now we're going to listen to the full story" in {baseLanguage}.
        Keep the introduction short and sweet."""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a conversation designer."},
            {"role": "user", "content": promptForIntro},
        ],
    )
    return response

def emptyPromptFunction(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o", #alternative model: gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    message_content = response['choices'][0]['message']['content']
   # total_tokens = response['choices'][0]['total_tokens']
    return message_content

def lang_differentiator(sentence, baselanguage, targetlanguage):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """

             You are an expert in differentiating languages for a podcast. Your task is to separate text by language, following these rules:
            1. Use separators (---) followed by the correct ISO language code when switching languages.
            2. Only switch languages for actual words or phrases, not for punctuation or spaces.
            3. Maintain the original sentence structure and punctuation.
            4. Do not add any explanatory text; only provide the differentiated sentence. Your job is also not to help with the 
            5. If you see a single word for a explenation purpose that is in an other language like the rest is has to be differentiated as well.


            """},
            {"role": "user", "content": f""" the first sentence that you need to differentiate is the following: the Sentence, "Я на улице!" means I'm outside. However, "на улице" can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, "на улице" has 2 meanings. /targetLanguage: 'RU' /explainLanguage:'EN' """ },

            {"role": "assistant", "content": f""" ---EN the Sentence, ---RU Я на улице ---EN means I'm outside. However, ---RU на улице ---EN can be outside but it also can mean on the street. So the sentence can also mean I'm on the street. So, ---RU на улице ---EN has 2 meanings. """},

            {"role": "user", "content": f""" "Was läuft bei dir Junge?" means "what's up with you, boy?" in English if we want to be literal. But you can also translate it as: "what's up dude" it is usually used in informal settings. But literally the word "läuft" means walking and "Junge" means boy. One last time the full sentence: "Was läuft bei dir Junge?"'  """}, 

            {"role": "assistant", "content": f""" ---DE "Was läuft bei dir Junge?" ---EN means 'What's up with you, boy?' in English if we want to be literal. But you can also translate it as: 'what's up dude' it is usually used in informal settings. But literally the word ---DE "läuft" ---EN means walking and ---DE Junge ---EN means boy. One last time the full sentence: ---DE Was läuft bei dir Junge? """},

            {"role": "user", "content": f"""{sentence} // languages beeing used are {baselanguage} and {targetlanguage} """ },

        ],
    )
    return response
#print(emptyPromptFunction("""This is just a test. Answer with "yes I do understand" please"""))