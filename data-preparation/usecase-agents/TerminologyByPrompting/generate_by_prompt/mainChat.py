import os
import openai
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
import json

class MainChat:
    def __init__(self, system_message):
        self.api_type = "azure"
        self.api_base = "YOUR API BASE"
        self.api_version = "YOUR API VERSION"
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.model = os.getenv("AZURE_OPENAI_MODEL")

        self.system_message = system_message
        
        openai.api_key = self.api_key
        openai.api_type = self.api_type
        openai.api_base = self.api_base
        openai.api_version = self.api_version
        
        self.chat_history = []
        self.chat_history.append({"role": "system", "content": system_message})

    def chat(self, user_input, system_message = None):
        try:
            message_text = {"role": "user", "content": user_input}
            self.chat_history.append(message_text)

            completion = openai.ChatCompletion.create(
                engine=self.model,
                messages=self.chat_history,
                temperature=0.7,
                max_tokens=2000,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            
            response_content = completion.choices[0].message['content'].strip()
            self.chat_history.append({"role": "system", "content": response_content})
        
            return response_content
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def reset_chat(self):
        self.chat_history = []
        self.chat_history.append({"role": "system", "content": self.system_message})
