from subFieldTree import SubfieldTree
from utils import save_wordtree_in_output
import json
import os

root_word = "Julius Caesar"
max_depth = 3
max_breadth = 3

model = os.getenv("AZURE_OPENAI_MODEL")

file_name = root_word.replace(" ", "_") + "_" + str(model) + "_" + str(max_depth) + "_" + str(max_breadth) + "_without_reset" +  ".json"

tree_constructor = SubfieldTree(root_word, max_depth, max_breadth)
word_tree = tree_constructor.construct_tree()
save_wordtree_in_output(word_tree, file_name)
