from mainChat import MainChat
import json

class TerminologyAgent:
    def __init__(self, max_breadth=10):
        self.system_message = "You are a helpful AI Assistant that lists relevant words. You are given a word, and return a list of " + str(max_breadth) + " words that are related to it in format: [\"term1\", \"term2\", ...]. Only respond with the output-list"
        self.chat_instance = MainChat(self.system_message)
        self.max_breadth = max_breadth

    def generateRelatedWords(self, word):
        #self.chat_instance.reset_chat() # else history is too big
        
        response = self.chat_instance.chat(word)
        try:
            response_json = json.loads(response)
            # Ensure the response is a list and truncate it to max_breadth if necessary
            if isinstance(response_json, list):
                return response_json[:self.max_breadth]
            else:
                print("Response was not in the expected format:", response)
                return []
        except json.JSONDecodeError:
            print("Failed to decode JSON from response:", response)
            return []

class SubfieldTree:
    def __init__(self, root_word, max_depth, max_breadth):
        self.T_agent = TerminologyAgent(max_breadth)
        self.tree = {"word": root_word, "children": []}
        self.max_depth = max_depth
        self.max_breadth = max_breadth
    
    def expand_node(self, node, current_depth):
        if current_depth == self.max_depth:
            return
        related_words = self.T_agent.generateRelatedWords(node["word"])
        for w in related_words:
            child_node = {"word": w, "children": []}
            node["children"].append(child_node)
            self.expand_node(child_node, current_depth + 1)
    
    def construct_tree(self):
        self.expand_node(self.tree, 0)
        return self.tree

