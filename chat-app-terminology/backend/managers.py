import os
import openai
from dotenv import load_dotenv
from terminology_manager import TerminologyManager, LearningObjectiveManager
import datetime
import json

class ChatHistoryManager:
    def __init__(self):
        self.init_system_message()

    def add_message(self, role, content):
        self.message_text.append({"role": role, "content": content})
    
    def get_conversation_history(self):
        return self.message_text
    
    def init_system_message(self, prompt = "You are an helpful AI assistant"):
        self.message_text = [{"role": "system", "content": prompt}]

    def delete_conversation_history(self):
        self.init_system_message()

class FileManager:
    def __init__(self, file):
        self.file = file
        self.data = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.file, 'r') as file:
                self.data = json.load(file)
        except Exception as e:
           print(f"Error in File Manager: {str(e)}")

    def safe_data(self, data):
        try:
            with open(self.file, 'w') as file:
                json.dump(data, file)
        except Exception as e:
           print(f"Error in File Manager: {str(e)}")
       

    def get_data(self):
        self.load_data()
        return self.data
