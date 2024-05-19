import requests
import json
import re

try:
    import keys as Keys
    api_key = Keys.gemini_key
except ImportError:
    api_key = input("Please enter your gemini API key: ")

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

def multiTurnConversation(api_key, conversation_history):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key
    headers = {'Content-Type': 'application/json'}
    data = {
      "contents": conversation_history
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

def chat_with_model(api_key, starting_message, system_message=None):
  conversation_history = []
  if system_message:
      conversation_history.append({
          "role": "system",
          "parts": [
              {
                  "text": system_message
              }
          ]
      })
  conversation_history.append({
      "role": "user",
      "parts": [
          {
              "text": starting_message
          }
      ]
  })
  while True:
    response = podcastgenerator(api_key, conversation_history)
    # Get the model's response text
    print("\033[95m" + response + "\033[0m")

    # Get user input for the next turn
    user_input = input("You: ")
    conversation_history.append({
        "role": "user",
        "parts": [
            {
                "text": user_input
            }
        ]
    })

    # Optionally provide a system message for the next turn
    system_message = input("System (optional): ")
    if system_message:
        conversation_history.append({
            "role": "system",
            "parts": [
                {
                    "text": system_message
                }
            ]
        })

# Example usage
api_key = "YOUR_API_KEY"  # Replace with your actual API key
starting_message = "Write a story about a magic backpack."
chat_with_model(api_key, starting_message)