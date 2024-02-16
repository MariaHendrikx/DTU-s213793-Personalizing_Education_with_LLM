import os
import json

def extract_words(node):
    # Initialize an empty list to hold words
    words = []
    
    # Base case: if the node is None, just return the empty list
    if node is None:
        return words
    
    # Add the current node's word to the list
    words.append(node['word'])
    
    # If the node has children, iterate through each child
    for child in node.get('children', []):
        # Recursively call extract_words on each child and extend the words list with the results
        words.extend(extract_words(child))
    
    return words

def save_output_as_json(data, file_name):
    # Prepare the output directory
    output_dir = "../output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the output file path
    output_file_path = os.path.join(output_dir, file_name)

    # Save the word_tree to a file
    with open(output_file_path, 'w') as file:
        json.dump(data, file, indent=2)

    print(f"Word tree saved to {output_file_path}")


def load_file(file_path):
    """Load and return the JSON data from the given file path."""
    with open(file_path, 'r') as file:
        return json.load(file)

file_names_ = "Artificial_Intelligence_gpt-4_3_16_without_reset.json Artificial_Intelligence_gpt-35-turbo_2_2.json Artificial_Intelligence_gpt-35-turbo_4_2_without_reset.json Artificial_Intelligence_gpt-35-turbo_4_4.json Artificial_Intelligence_gpt-35-turbo_4_16_without_reset.json Artificial_Intelligence_gpt-35-turbo_8_2.json Artificial_Intelligence_gpt4_2_2.json Artificial_Intelligence_gpt4_2_16.json Artificial_Intelligence_gpt4_3_3.json Artificial_Intelligence_gpt4_4_4.json Artificial_Intelligence_gpt4_8_2.json computer_science_gpt-4_3_3_without_reset.json Julius_Caesar_gpt-4_3_6_without_reset.json"

# Split the long string of file paths into a list
file_names = file_names_.split(" ")

for file_name in file_names:
    full_path = os.path.join("./", file_name)  # Adjust this path
    try:
        tree = load_file(file_name)
        word_list = extract_words(tree)
        save_output_as_json(word_list, os.path.basename(file_name).replace(".json", "_word_list.json"))
    except FileNotFoundError:
        print(f"File not found: {full_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {full_path}")