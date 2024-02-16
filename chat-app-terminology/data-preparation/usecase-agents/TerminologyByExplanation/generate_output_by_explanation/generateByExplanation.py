from mainChat import MainChat
import os
from utils import save_output_as_json

class ExplainerTerminologyAgent:
    def __init__(self):
        self.system_message_agent_1 = """
We are playing a simulation game. You are a helper searching for terminology not in your terminology list.
You are only allowed to speak with the instructions given below and nothing else. 

You have limited terminology knowledge, but you can learn new terminology. 
Imagine know have a TERMINOLOGY-LIST of a typical 13 year old teenager as database.
Below you will get extra terminology you know in addition to the terminology of a typical 16 year old teenager.
If words are not existent in the TERMINOLOGY-LIST, you answer with "DONT UNDERSTAND:" followed with the list. 
and give a list of words why you are answering with 'DONT UNDERSTAND:'.

IF you get an explanation of the new terms, analyze the text (both the term and the explanation) for new terms that are not in your TERMINOLOGY-LIST.
IF all terms in the text (including in the explanation) are in the TERMINOLOGY-LIST, reply TERMINATE
IF certain words are not in the list, you answer with "DONT UNDERSTAND:" followed with the list of words not in your TERMINOLOGY-LIST.
ELSE you answer with "DONT UNDERSTAND:" followed with the list of words not in your TERMINOLOGY-LIST.
If a verb is in the TERMINOLOGY-LIST, you also know the conjugations.
Only respond with the output.

Extra words you know: """

        self.system_message_explainer = """You are a helpful AI Assistant that explains words. You explain all terms after 'DONT UNDERSTAND: *a list of words*',, 
THEN you should answer with explanations for those words, rich of words related to the origal word. List each word.
Only respond with the output.
IF "TERMINATE" is in the prompt then answer with 'QUITTINGNOW'
"""

        self.chat_instance = MainChat(self.system_message_agent_1)
        self.chat_instance_explainer = MainChat(self.system_message_explainer)
        self.words_learned = []

    def play(self, user_input):
        response = self.chat_instance.chat(user_input.strip())
        explained = self.chat_instance_explainer.chat(response.strip())
        self.addWordsLearned(response)

        print("Term-AI:", response)
        print("Explainer-AI:", explained)

        # range to be sure it doesn't call itself forever
        for i in range(3): 
            response = self.chat_instance.chat(explained.strip())
            explained = self.chat_instance_explainer.chat(response.strip())
            print("Term-AI:\n", response)
            print("Explainer-AI:", explained)
            self.addWordsLearned(response)
            if('QUITTINGNOW') in explained:
                break
    
    def addWordsLearned(self, text):
        words = text.replace('DONT UNDERSTAND:', '').split()        
        for word in words:
            if word not in self.words_learned:
                self.words_learned.append(word)

    def getWordsLearned(self):
        return self.words_learned
            

# Example usage
explainer_chat = ExplainerTerminologyAgent()
root_word = 'Julius Caesar'
explainer_chat.play(root_word)

model = os.getenv("AZURE_OPENAI_MODEL")
file_name = root_word.replace(" ", "_") + "_" + str(model) + "_byExplanation_2" + ".json"

save_output_as_json(explainer_chat.getWordsLearned(), file_name)

