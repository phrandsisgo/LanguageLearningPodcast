from audio_save import *
from tts import tts_decisioner
json_name = get_correct_json_data()

short_file = json_name.rstrip(".json")
json_path = create_audio_folder(short_file)
print(f"Created folder: {json_path}")
print(f"json name is {json_name}")
print(get_intro(json_name))
print (get_base_language(json_name))
full_path = os.path.join("output",json_path, "intro")
tts_decisioner(get_base_language(json_name), get_intro(json_name), path_name=full_path)