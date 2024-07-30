import os
import inquirer
import json


def create_audio_folder(foldername):
    try:
        folder_path = os.path.join("output", foldername)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"full folder path: {folder_path}")
        return folder_path
    except Exception as e:
        print(f"An error occurred while creating the audio folder: {str(e)}")
        return None

def get_correct_json_data():
    json_files = [file for file in os.listdir("output/") if file.endswith(".json")]
    
    if not json_files:
        print("No JSON files found in the output/ directory.")
        return None

    questions = [
        inquirer.List('file',
                      message="Please choose the JSON file you would like to use:",
                      choices=json_files,
                      ),
    ]

    answers = inquirer.prompt(questions)
    return answers['file']


def get_intro(jsonPath):
    # Check if the file exists
    jsonPath = os.path.join("output", jsonPath)
    if not os.path.exists(jsonPath):
        print(f"Error: The file {jsonPath} does not exist.")
        return None

    # Read the JSON file
    try:
        with open(jsonPath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(f"Error: The file {jsonPath} is not a valid JSON file.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")
        return None

    # Extract the intro from the JSON data
    intro = data.get('intro')
    
    if intro is None:
        print("Error: The 'intro' field is missing from the JSON data.")
        return None

    return intro
# Usage test
print(f"this is the path: {create_audio_folder('mark')}")
