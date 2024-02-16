import os
import openai
from dotenv import load_dotenv
from managers import ChatHistoryManager, FileManager
# Load environment variables
import json
load_dotenv()
import string

prompt = """You are an helpful AI assistant that is given a sentence. Figure out the seperate chinese words, and provide the english translation and explanation of the word.
You answer as follows, where ... are other words you could find in this sentence. 
Try to include the following words: wo, ni, ta, women, nimen, tamen, mei ge ren, ni hao, xiexie, shi de, bu, qing, pengyou, jiao, zaijian, xihuan, hao, shi, xuesheng.
Only include relevant words. And group Word-combination together, such as ni hao, ni ne, etc.,
also remove puncuation and everything in lower case.:
[{
    "word": "word in pingying",
    "translation": "translation",
    "explanation": "explanation"
    }, 
...
]             
"""

class ExplainTermsChat:
    def __init__(self):
        self.api_type = "azure"
        self.api_base = "https://decmasterthesis25.openai.azure.com/"
        self.api_version = "2023-07-01-preview"
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        
        openai.api_key = self.api_key
        openai.api_type = self.api_type
        openai.api_base = self.api_base
        openai.api_version = self.api_version

        self.list_of_words = []
        self.mainchat_conversation_history = [{
                "role": "system",
                "content": "We are playing a simulation game.\n                Imagine and create a scenario where you can always answer of the user.\n                You are playing/simulating friendly person when aswering *gramattically correct answer* and are simulating a conversation.\n                rules:\n                    - You can only answer in ping yin. You will be terminated else.\n                    - You can only answer with the words in the TERMINOLOGY_LIST. You will be terminated else.\n                    - if needed, you can add a max of 10 words to make the sentence gramatically correct.\n                    - Answer as basic as possible\n\n                TERMINOLOGY LIST: \n                "
            }]
        self.mainchat_history_filemanager = FileManager('./data/chat_history_main.json')  
        
        self.chat_history_manager = ChatHistoryManager()
        self.chat_history_manager.init_system_message(prompt)

    def chat(self, user_input):
        try:
            self.chat_history_manager.add_message("user", user_input)
            conversation_history = self.chat_history_manager.get_conversation_history()
            
            completion = openai.ChatCompletion.create(
                engine="gpt-4-32k",
                messages=conversation_history,
                temperature=0.7,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            
            response_content = completion.choices[0].message['content']
            self.chat_history_manager.add_message("system", response_content)                  
            
            return response_content
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
    def compare_conversations(self, convo1, convo2):
        """
        Compares two conversation lists and returns the difference, with the assumption
        that convo2 contains all the elements of convo1 in the same order, plus potentially more.

        Parameters:
        - convo1: List[Dict[str, str]]
        - convo2: List[Dict[str, str]]

        Returns:
        - List[Dict[str, str]]: The elements in convo2 that are not in convo1.
        """
        # Find the starting index of the difference
        start_idx = len(convo1)  # Assume all initial parts match, start from the end of convo1

        # Return the slice of convo2 starting from start_idx to the end
        return convo2[start_idx:]

    def turn_conversationhistorychat_into_voclist(self):
        convo2 = self.mainchat_history_filemanager.get_data()
        difference_in_historychat = self.compare_conversations(self.mainchat_conversation_history, convo2)
        self.mainchat_conversation_history = convo2 # update the conversation history for next time difference

        for message in difference_in_historychat:
            # Access the role and content of each message
            role = message['role']
            content = message['content']
            response = self.chat(content)
            self.chat_history_manager.init_system_message(prompt) # reset history to make llm faster and reduce costs
            self.add_words_to_list_from_json(response)

  
    def generate_and_get_explained_list(self):
        self.turn_conversationhistorychat_into_voclist()
        return self.list_of_words

    def get_explained_list(self):
        return self.list_of_words


    def add_words_to_list_from_json(self,data):
        try:
            words_list = json.loads(data)
            for new_word in words_list:
                self.add_word_if_not_duplicate(self.list_of_words, new_word)
        except Exception as e:
                return f"An error occurred: {str(e)}" 
        
    def add_word_if_not_duplicate(self, word_list, new_word):
        for word in word_list:
            if word["word"] == new_word["word"] and word["translation"] == new_word["translation"]:
                print("Word already exists in the list.")
                return
        self.list_of_words.append(new_word)
        print("Word added successfully.: ", str(new_word["word"]))


# Example usage
if __name__ == "__main__":
    chat_instance = ExplainTermsChat()
    print(chat_instance.generate_and_get_explained_list())