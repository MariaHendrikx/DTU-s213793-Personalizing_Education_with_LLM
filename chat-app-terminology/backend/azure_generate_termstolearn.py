import os
import openai
from dotenv import load_dotenv
from terminology_manager import TerminologyManager, LearningObjectiveManager
import json

class OpenAIGenerateTermsToLearn:
    def __init__(self, api_key, terminology_file_path='./data/terminology.json', terms_to_learn_path='./data/termstolearn.json', learning_objectives_path='./data/learningobjectives.json'):
        self.api_key = api_key
        self.terminology_manager = TerminologyManager(terminology_file_path, terms_to_learn_path)
        self.learning_objective_manager = LearningObjectiveManager(learning_objectives_path)
        self.setup_openai()

    def setup_openai(self):
        openai.api_type = "azure"
        openai.api_base = "https://decmasterthesis25.openai.azure.com/"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = self.api_key

    def save_terms_to_learn(self, termstolearn):
        with open('./data/termstolearn.json', 'w', encoding='utf-8') as f:
            json.dump(termstolearn, f, ensure_ascii=False, indent=4)

    def get_default_learning_objectives(self):
        with open('./data/default_learningobjectives.json', 'r') as file:
            return json.load(file)


    def generate_terms_to_learn(self):
        message_text = [{"role":"system","content":"You are an AI assistant that only answers with the OUTPUT asked for."},
                {"role":"user","content":"""
given the following learning objectives, can you create a list of "terms to learn" categorized? only answer with the output list

INPUT: 
[
    {
        "objective": "Basic Communication",
        "description": "Understanding and using familiar everyday expressions and very basic phrases aimed at satisfying needs of a concrete type. This includes greetings, introductions, and asking for basic personal information."
    },
    {
        "objective": "Interaction Skills",
        "description": "Ability to participate in a simple conversation on familiar topics. The learner should be able to interact simply if the other person talks slowly and clearly and is ready to help."
    },
    {
        "objective": "Basic Vocabulary and Grammar",
        "description": "Understanding and using familiar words and simple phrases for concrete purposes. Ability to form simple sentences about personal details, local geography, employment, etc."
    }
]"""},
                {"role":"system","content":"""{
  "Terms to Learn": {
    "Basic Communication": [
      "Greetings",
      "Introductions",
      "Basic personal information (name, age, nationality)"
    ],
    "Interaction Skills": [
      "Simple conversation",
      "Familiar topics"
    ],
    "Basic Vocabulary and Grammar": [
      "Familiar words",
      "Simple phrases",
      "Simple sentences",
      "Personal details",
      "Local geography",
      "Employment"
    ]
  }
}
"""},
{"role":"user","content":"""Can you now fill out all the terms related to this in JSON?"""},
                {"role":"system","content": """[
    {
        "title": "Basic Communication --> Greetings",
        "terms": [
            "hello",
            "hi",
            "hey",
            "good",
            "morning",
            "afternoon",
            "evening",
            "how",
            "are",
            "you",
            "good morning",
            "good afternoon",
            "good evening",
            "how are you?",
            "how's it going?",
            "what's up?"
        ]
    },
    {
        "title": "Basic Communication --> Introductions",
        "terms": [
            "I'm",
            "My name is",
            "I am",
            "This is",
            "meet",
            "pleased to meet you",
            "nice to meet you",
            "let me introduce",
            "introduction"
        ]
    },
    {
        "title": "Basic Communication --> Basic personal information",
        "terms": [
            "name",
            "I am from",
            "I live in",
            "age",
            "I work as",
            "My job is",
            "nationality",
            "languages",
            "I speak"
        ]
    },
    {
        "title": "Interaction Skills --> Simple conversation",
        "terms": [
            "talk",
            "speak",
            "say",
            "tell me",
            "Can you",
            "Could you",
            "Would you mind",
            "discuss",
            "conversation",
            "communicate"
        ]
    },
    {
        "title": "Interaction Skills --> Familiar topics",
        "terms": [
            "weather",
            "hobbies",
            "sports",
            "music",
            "movies",
            "food",
            "travel",
            "books",
            "family",
            "work",
            "school"
        ]
    },
    {
        "title": "Basic Vocabulary and Grammar --> Familiar words",
        "terms": [
            "home",
            "family",
            "work",
            "school",
            "food",
            "water",
            "friend",
            "book",
            "shop",
            "market"
        ]
    },
    {
        "title": "Basic Vocabulary and Grammar --> Simple phrases",
        "terms": [
            "Can I have",
            "I would like",
            "Where is",
            "How much",
            "What time",
            "Do you have",
            "Is there",
            "I need",
            "Please",
            "Thank you"
        ]
    },
    {
        "title": "Basic Vocabulary and Grammar --> Simple sentences",
        "terms": [
            "I am from",
            "I live in",
            "I work as",
            "I like to",
            "I want to",
            "I have to",
            "I need to",
            "I am going to",
            "I can",
            "I cannot"
        ]
    },
    {
        "title": "Basic Vocabulary and Grammar --> Personal details",
        "terms": [
            "name",
            "age",
            "address",
            "phone number",
            "email",
            "birthday",
            "occupation",
            "nationality",
            "marital status",
            "hobbies"
        ]
    },
    {
        "title": "Basic Vocabulary and Grammar --> Local geography",
        "terms": [
            "city",
            "town",
            "village",
            "country",
            "mountain",
            "river",
            "lake",
            "sea",
            "ocean",
            "forest"
        ]
    },
    {
        "title": "Basic Vocabulary and Grammar --> Employment",
        "terms": [
            "job",
            "work",
            "company",
            "office",
            "factory",
            "manager",
            "employee",
            "colleague",
            "salary",
            "interview"
        ]
    }
]

"""},{"role":"user","content":"""
given the following learning objectives, can you create a list of "terms to learn" categorized? only answer with the output list
AND after that: Can you now fill out all the terms related to this in JSON?
between each output: put --------
      
INPUT: """ + str(self.learning_objective_manager.get_learningobjectives())},
]

        completion = openai.ChatCompletion.create(
            engine="gpt-4-32k",
            messages=message_text,
            temperature=0.7,
            max_tokens=4096,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        result = completion.choices[0].message['content'].split("--------")
        termstolearn = json.loads(result[1])
        self.save_terms_to_learn(termstolearn)

        return termstolearn