import random
import string

def get_random_string(size=20):
    return "".join(random.choice(string.ascii_lowercase) for i in range(size))

class Neuron:
    def __init__(self, text):
        self.text = text
        self.uuid = get_random_string()
        self.next_is_noun = False
        self.next_is_verb = False
        self.next_is_noun_or_verb = False        
        self.past_tense = False
        self.future_tense = False
        self.present_tense = False
        self.continuous = False
        self.is_verb = False
        self.is_noun = False
        self.place = False
        self.location = False
        self.owned_by = False
        self.character = False
        self.mode = False
        self.frequency = False
        self.person = False
        self.time = False
        self.action = False
        self.root_verb = None
        self.conn_nouns = []
        self.conn_verbs = []
