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
                engine="gpt-4",
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

# Example usage
if __name__ == "__main__":
    system_message_agent_1 = """
We are playing a simulation game. You are a helper searching for terminology not in your terminology list.
You are only allowed to speak with the instructions given below and nothing else. 

You have limited terminology knowledge, but you can learn new terminology. 
Imagine know have a TERMINOLOGY-LIST of a typical 16 year old teenager as database.
Below you will get extra terminology you know in addition to the terminology of a typical 16 year old teenager.
If words are not existent in the TERMINOLOGY-LIST, you answer with "DONT UNDERSTAND:" followed with the list. 
and give a list of words why you are answering with 'DONT UNDERSTAND:'.
If a verb is in the TERMINOLOGY-LIST, you also know the conjugations.

IF you get an explanation of the new terms, analyze the text for new terms that are not in your TERMINOLOGY-LIST.
IF all terms in the text are in the TERMINOLOGY-LIST, list all terms and end with TERMINATE as last word.

Extra words you know: """
    chat_instance = MainChat(system_message_agent_1)

    system_message_explainer = """You are a helpful AI Assistant that explains words. You explain all terms after 'DONT UNDERSTAND: *a list of words*',, 
    THEN you should answer with explanations for those words in less than 2 sentences.
    IF you understand everything, then asnwer with 'quit'
    """

    chat_instance_explainer = MainChat(system_message_explainer)
    print("Welcome to the AI chat! Type 'quit' to exit.")
    user_input = ''
    while True:
        quit_input = input("You: ")
        if(user_input == ''):
            user_input = 'What is reinforcement learning in AI?'
        if quit_input.lower() == 'quit':
            print("Goodbye!")
            break
        response = chat_instance.chat(user_input.strip())
        explained = chat_instance_explainer.chat(response.strip())

        print("Term-AI:", response)
        print("Explainer-AI:", explained)

    print('\n \n')
    print('---------------')
    print(chat_instance_explainer.chat_history)
    print(chat_instance.chat_history)
