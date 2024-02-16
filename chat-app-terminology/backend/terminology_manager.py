import json

class TerminologyManager:
    def __init__(self, terminology_file, terms_to_learn_file):
        self.terminology_file = terminology_file
        self.terms_to_learn_file = terms_to_learn_file
        self.terminology = {}
        self.terms_to_learn = []

        self.load_data()

    def load_data(self):
        with open(self.terminology_file, 'r') as file:
            self.terminology = json.load(file)
        with open(self.terms_to_learn_file, 'r') as file:
            self.terms_to_learn = json.load(file)

    def save_data(self):
        with open(self.terminology_file, 'w') as file:
            json.dump(self.terminology, file, indent=4)
        with open(self.terms_to_learn_file, 'w') as file:
            json.dump(self.terms_to_learn, file, indent=4)

    def get_terminology(self):
        return self.terminology
    
    def get_all_terminology_terms(self):
        all_terms = []
        all_terms += (self.get_terminology()['shortterm'])
        all_terms += (self.get_terminology()['longterm'])
        return all_terms
    
    def get_terms_to_learn(self):
        return self.terms_to_learn
    
    def get_category_of_term_in_terminology(self, term):
        for category, terms in self.terminology.items():
            if term in terms:
                return category
        return None
    
    def is_term_in_terminology(self, term):
        if(term in self.get_all_terminology_terms()):
            return True
        return False
    
    def add_term_to_terminology(self, category, term):
        if category in self.terminology:
            if term not in self.terminology[category]:
                self.terminology[category].append(term)
        else:
            self.terminology[category] = [term]
        self.save_data()

    def remove_term_from_terminology(self, category, term):
        if category in self.terminology and term in self.terminology[category]:
            self.terminology[category].remove(term)
            self.save_data()

    def add_category_to_terms_to_learn(self, title, words):
        self.terms_to_learn.append({"title": title, "words": words})
        self.save_data()

    def add_word_to_terms_to_learn(self, title, word):
        for category in self.terms_to_learn:
            if category["title"] == title:
                if word not in category["words"]:
                    category["words"].append(word)
                    break
        self.save_data()

    def remove_word_from_terms_to_learn(self, title, word):
        for category in self.terms_to_learn:
            if category["title"] == title and word in category["words"]:
                category["words"].remove(word)
                break
        self.save_data()

# Example usage:
# terminology_manager = TerminologyManager('./data/terminology.json', './data/termstolearn.json')
# print(terminology_manager.get_terminology())
# terminology_manager.add_term_to_terminology('shortterm', 'average')
# print(terminology_manager.get_all_terminology_terms())


import json

class LearningObjectiveManager:
    def __init__(self, learningobjectives_file):
        self.learningobjectives_file = learningobjectives_file
        self.learningobjectives = {}
        self.load_data()

    def load_data(self):
        with open(self.learningobjectives_file, 'r') as file:
            self.learningobjectives = json.load(file)

    def get_learningobjectives(self):
        return self.learningobjectives

# Example usage:
# print(terminology_manager.get_terminology())
# terminology_manager.add_term_to_terminology('shortterm', 'average')
# print(terminology_manager.get_all_terminology_terms())
