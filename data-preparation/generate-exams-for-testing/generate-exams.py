import requests
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

def read_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()
    
def save_content_to_file(content, exam_number, language, CEFR_level):
    output_directory = "output"  # Make sure this directory exists
    output_filename = f"{language}_CEFR_{CEFR_level}_exam{exam_number}.md"
    output_path = os.path.join(output_directory, output_filename)

    os.makedirs(output_directory, exist_ok=True)  # Create directory if it doesn't exist

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Content saved to {output_path}")


def get_gpt4_response(language="English", CEFR_level="A1"):
    openai.api_type = "azure"
    openai.api_base = os.getenv("AZURE_OPENAI_BASE_URL") 
    openai.api_version = "2023-09-15-preview"
    openai.api_key = os.getenv("AZURE_OPENAI_KEY")
    deployment_name = 'gpt-4-32k'
    
    exam_content = read_file_content('example-exam.md')

    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[
            {"role": "system", "content": f"You are a helpful assistant. You are creating exam questions to test the user in CEFR level {CEFR_level} in the language {language}? Always use the same template to answer. Each exam should be completely different from the others."},
            {"role": "user", "content": "Can you give the exam questions to me?"},
            {"role": "assistant", "content": exam_content},
            {"role": "user", "content": f"Can you generate the exam questions for me just like before?: language: {language}, CEFR level: {CEFR_level}?"}
        ]
    )

    return response['choices'][0]['message']['content']


def main():
    languages = ["English", "Spanish", "Greek"]
    CEFR_levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
    exam_number = 0

    for language in languages:
        for CEFR_level in CEFR_levels:
            for exam_number in range(3):
                response = get_gpt4_response(language, CEFR_level)
                save_content_to_file(response, exam_number, language, CEFR_level)

if __name__ == "__main__":
    main()
