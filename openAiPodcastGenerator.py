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

def Introwriter(fullStory, targetLanguage, baseLanguage, level, ):
    promptForIntro = f"""Hi, you are an excellent introduction writer for a Podcast.
      I want you to write me an introduction for a language learning podcast that is for language learners who are learning {targetLanguage} at the {level} level.
       The introduction should be written only in {baseLanguage} and should not include any other languages.
        You should write an introduction that is about the following story: {fullStory}.
        Now that you know the full story, keep in mind that as the last sentence, the listener will also hear this story in the language of {targetLanguage}.
        So, you should tell the listener something like "And now we're going to listen to the full story" in {baseLanguage}.
        Keep the introduction short and sweet."""
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
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

def empty_GPT4o_mini(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    message_content = response['choices'][0]['message']['content']
    return message_content


def lang_differentiator(sentence, baselanguage, targetlanguage):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
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