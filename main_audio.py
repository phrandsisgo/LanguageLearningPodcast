from audio_save import *
from tts import tts_decisioner
import os
import re
json_name = get_correct_json_data()

short_file = json_name.rstrip(".json")
json_path = create_audio_folder(short_file)
def do_intro():
    if os.path.exists(os.path.join("output",json_path, "intro")):
        return
    full_path = os.path.join("output",json_path, "intro")
    tts_decisioner(get_base_language(json_name), get_intro(json_name), path_name=full_path)
    print("Intro audio file created.")
    return

def do_story():
    print("starting to create story audio file")
    if os.path.exists(os.path.join("output",json_path, "story")):
        return
    full_path = os.path.join("output",json_path, "story")
    tts_decisioner(get_target_language(json_name), get_story(json_name),speed=0.8, path_name=full_path)   
    print("Story audio file created.")
    return

def do_explanations():
    print("Starting to create explanation audio files")
    explanations_path = os.path.join("output", json_path)
    # Check if there are files starting with "explanation" and have the extension ".mp3"
    if os.path.exists(explanations_path) and any(fname.startswith("explanation") and fname.endswith(".mp3") for fname in os.listdir(explanations_path)):
        print("Explanation files already exist.")
        return
    explanations = get_explanations(json_name)
    if explanations is None:
        print("Error: Could not retrieve explanations.")
        return

    target_language = get_target_language(json_name)
    base_language = get_base_language(json_name)

    for idx, explanation in enumerate(explanations, 1):
        explanation_text = explanation.get('explanation')

        if explanation_text is None:
            print(f"Error: Missing explanation text for item {idx}")
            continue

        # Split the explanation into parts based on language tags
        parts = re.split(r'(---\w{2})', explanation_text)
        parts = [part for part in parts if part.strip()]  # Remove empty parts

        for sub_idx, part in enumerate(parts[1:], 1):  # Start from 1 to skip the first tag
            if re.match(r'---\w{2}', part):
                continue

            language_tag = parts[sub_idx - 1]
            language = base_language if language_tag == f'---{base_language.upper()}' else target_language

            # Create audio for each part of the explanation
            explanation_path = os.path.join(explanations_path, f"explanation{idx}-{sub_idx}")
            if not os.path.exists(explanation_path + ".mp3"):
                speed = 0.8 if language == target_language else 1.0
                tts_decisioner(language, part.strip(), speed=speed, path_name=explanation_path)
                print(f"Created audio for explanation {idx}-{sub_idx} in {language} with speed {speed}")

    print("All explanation audio files created.")
do_intro()
do_story()
do_explanations()