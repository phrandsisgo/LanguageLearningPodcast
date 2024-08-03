from audio_save import *
from tts import tts_decisioner
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

    explanations = get_explanations(json_name)
    if explanations is None:
        print("Error: Could not retrieve explanations.")
        return

    # Find the highest existing sentence number
    existing_files = [f for f in os.listdir(explanations_path) if f.startswith("sentence") and f.endswith(".mp3")]
    highest_number = 0
    for file in existing_files:
        try:
            number = int(file.replace("sentence", "").replace(".mp3", ""))
            highest_number = max(highest_number, number)
        except ValueError:
            continue

    # Start numbering from the next available number
    start_number = highest_number + 1

    for idx, explanation in enumerate(explanations[highest_number:], start_number):
        sentence_number = explanation.get('sentence_number')
        sentence = explanation.get('sentence')
        explanation_text = explanation.get('explanation')

        if sentence is None or explanation_text is None:
            print(f"Error: Missing data for explanation {idx}")
            continue

        # Create audio for the sentence in target language
        sentence_path = os.path.join(explanations_path, f"sentence{idx}")
        if not os.path.exists(sentence_path + ".mp3"):
            tts_decisioner(get_target_language(json_name), sentence, speed=0.8, path_name=sentence_path)
            print(f"Created audio for sentence {idx}")

        # Create audio for the explanation
        explanation_path = os.path.join(explanations_path, f"explanation{idx}")
        if not os.path.exists(explanation_path + ".mp3"):
            tts_decisioner(get_base_language(json_name), explanation_text, path_name=explanation_path)
            print(f"Created audio for explanation {idx}")

    print("All explanation audio files created.")

do_intro()
do_story()
do_explanations()