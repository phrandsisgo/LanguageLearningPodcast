import os
import json
from datetime import datetime

def generate_filename(title):
    #Generates a filename based on title, date and time
    now = datetime.now()
    date_time = now.strftime("%Y%m%d-%H%M%S")
    return f"{title}-{date_time}"


def generate_filepath(title):
    # Generates a filepath based on title, date, and time
    now = datetime.now()
    date_time = now.strftime("%Y%m%d-%H%M%S")
    filename = f"{title}-{date_time}.json"
    return os.path.join('output', filename)

def ensure_output_directory():
    #Ensures that the output directory exists
    if not os.path.exists('output'):
        os.makedirs('output')


def create_empty_file(filepath):
    # Creates an empty JSON file with initial structure
    initial_data = {
        "intro": "",
        "story": "",
        "explanations": []
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(initial_data, f, ensure_ascii=False, indent=2)


def add_intro(filepath, intro):
    # Adds the intro to the JSON file
    with open(filepath, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data['intro'] = intro
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

def add_story(filepath, story):
    # Adds the story to the JSON file
    with open(filepath, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data['story'] = story
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

def append_explanation(filepath, explanation):
    # Appends an explanation to the existing file
    with open(filepath, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data['explanations'].append(explanation)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

def save_output(title, content, token_usage=None):
    #Saves the content and token usage in a file in the output directory with a generated filename
    ensure_output_directory()
    filename = generate_filename(title)
    full_path = os.path.join('output', f"{filename}.json")
    
    output_data = {
        "content": content
    }
    
    if token_usage is not None:
        output_data["token_usage"] = token_usage
    
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    return full_path

def load_output(filepath):
    #Loads the content from a specific file
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def edit_content(filepath):
    #Opens a file for editing and saves the changes
    data = load_output(filepath)
    content = data['content']
    
    print("Aktueller Inhalt:")
    for key, value in content.items():
        print(f"{key}: {value}")
    
    for key in content.keys():
        edited = input(f"Bearbeiten Sie den Inhalt von '{key}' (leer lassen für keine Änderung):\n")
        if edited:
            content[key] = edited
    
    data['content'] = content
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def analyze_output(filepath):
    #Analyzes the content of an output file and returns statistics
    data = load_output(filepath)
    content = data['content']
    token_usage = data['token_usage']
    
    stats = {
        "token_usage": token_usage,
        "content_stats": {}
    }
    
    for key, value in content.items():
        stats["content_stats"][key] = {
            'chars': len(value)
        }
    
    return stats

#nun kann ich diese Funktionen noch im Hauptskript folgendermassen verwenden:
#has to translated to english but I'm too tired to do it now
"""

from save_docs import save_output, edit_content, analyze_output
from your_other_modules import generate_story, lang_differentiator, generate_title

# Generiere Titel
title = generate_title()

# Generiere Geschichte
story, story_token_usage = generate_story()  # Angenommen, diese Funktion gibt auch Token-Nutzung zurück

# Führe Sprachdifferenzierung durch
differentiated, diff_token_usage = lang_differentiator(story, base_language, target_language)  # Ebenso hier

# Speichere alle Daten
token_usage = {
    "story_generation": story_token_usage,
    "language_differentiation": diff_token_usage
}

filepath = save_output(title, {
    'title': title,
    'original_story': story,
    'differentiated_story': differentiated
}, token_usage)

# Erlaube Bearbeitung
edit_content(filepath)

# Analysiere die Ausgabe
stats = analyze_output(filepath)
print(f"Statistiken: {stats}")

# Hier würden Sie mit der TTS-Vertonung fortfahren...
"""