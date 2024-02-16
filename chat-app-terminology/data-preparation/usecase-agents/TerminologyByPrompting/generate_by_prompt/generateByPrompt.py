from mainChat import MainChat
from utils import save_output_as_json
import json

system_message = """You are a helpful AI Assistant that return a list of related words to the input word. Only respond with the output. Go as deep and broad as possible."""

root_word = "Julius Caesar"
chat_instance = MainChat(system_message)
output = chat_instance.chat(root_word)
output_as_list = output.split(", ")

file_name = root_word.replace(" ", "_") + "_byPrompting.json"
save_output_as_json(output_as_list, file_name)