import os
import openai
from dotenv import load_dotenv
from managers import ChatHistoryManager, FileManager
# Load environment variables
load_dotenv()

prompt = """We are playing a simulation game.
Imagine and create a scenario where you can always answer of the user.
You are playing/simulating friendly person when aswering *gramattically correct answer* and are simulating a conversation.
rules:
- You can only answer in ping yin. You will be terminated else.
- You can only answer with the words in the TERMINOLOGY_LIST. You will be terminated else.
- if needed, you can add a max of 10 words to make the sentence gramatically correct.
- Answer as basic as possible
TERMINOLOGY LIST: """

class MainChat:
    def __init__(self):
        self.api_type = "azure"
        self.api_base = "https://decmasterthesis25.openai.azure.com/"
        self.api_version = "2023-07-01-preview"
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        
        openai.api_key = self.api_key
        openai.api_type = self.api_type
        openai.api_base = self.api_base
        openai.api_version = self.api_version
        
        self.chathistory_filemanager = FileManager('./data/chat_history_main.json')  
        self.chathistory_manager = ChatHistoryManager()
        self.chathistory_manager.init_system_message(prompt)
        self.chathistory_filemanager.safe_data(self.get_conversation_history())
        
    def get_conversation_history(self):
        return self.chathistory_manager.get_conversation_history()

    def chat(self, user_input):
        try:
            self.chathistory_manager.add_message("user", user_input)
            conversation_history = self.get_conversation_history()
            
            completion = openai.ChatCompletion.create(
                engine="gpt-4",
                messages=conversation_history,
                temperature=0.6,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            
            response_content = completion.choices[0].message['content'].strip()
            self.chathistory_manager.add_message("system", response_content)

            self.chathistory_filemanager.safe_data(self.get_conversation_history())

            return response_content
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
    
# Example usage
if __name__ == "__main__":
    chat_instance = MainChat()
    print("Welcome to the AI chat! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        response = chat_instance.chat(user_input)
        print("AI:", response)