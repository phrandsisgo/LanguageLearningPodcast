from audio_save import *

json_name = get_correct_json_data()

short_file = json_name.rstrip(".json")
json_path = create_audio_folder(short_file)
print(f"Created folder: {json_path}")
print(f"json name is {json_name}")
print(get_intro(json_name))
