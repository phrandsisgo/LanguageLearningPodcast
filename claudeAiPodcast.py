import anthropic
import os
from keys import anthropic_key

# Initialisieren Sie den Client mit dem API-Schlüssel aus keys.py
client = anthropic.Anthropic(
    api_key=anthropic_key,
)

message = client.messages.create(
  model="claude-3-5-sonnet-20240620",
  max_tokens=4000,
  temperature=0,
  system=" Your Task is to write short stoies about stuff that the user wants.",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Write me a short story about louis who is frustrated to find a new apartment in Zürich."
        }
      ]
    }
  ]
)
print(message.content)

