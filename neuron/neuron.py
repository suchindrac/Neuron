import pprint
import sys
import traceback
import string

nouns_list = []
verbs_list = []

class Neuron:
    def __init__(self, text, node, prev_node, next_node):
        self.node = None
        self.next_chains = []
        self.prev_chains = []
        if not node:
            self.node = self

        self.text = text
        self.conn_nouns = []
        self.conn_verbs = []
        self.weightage = 1
        
def get_node_chain(input_list):
    yield False, input_list[0], input_list[1:]
    yield [input_list[0]], input_list[1], input_list[2:]
    for i in range(2, len(input_list)-1):
        yield input_list[i-1::-1], input_list[i], input_list[i+1:]
    yield input_list[i::-1], input_list[-1], False

class NodeMap():
    def __init__(self):
       self.key_map = {}

    def display(self):
        for key in self.key_map.keys():
            node = self.key_map[key]
            prev_text = []
            next_text = []
            for chain in node.prev_chains:
                prev_text.append([x.text for x in chain])

            for chain in node.next_chains:
                next_text.append([x.text for x in chain])

            conn_nouns = [x.text for x in node.conn_nouns]
            conn_verbs = [x.text for x in node.conn_verbs]
            print(f"{node.text} -> {prev_text} {next_text} {conn_nouns} {conn_verbs}")
            
    def get_node(self, word):
        if word in self.key_map.keys():
            return self.key_map[word]
        else:
            return False
        
    def add_node(self, word):
        if not self.get_node(word):
            node = Neuron(word, None, None, None)
            self.key_map[word] = node

    def ask(self, question):
        question = question.split()
        question = [x.strip(string.punctuation).lower() for x in question]
        question = [x for x in question if x.isalpha()]
        verbs_list_local = [x for x in verbs_list if x in question]

        verb_nodes = [self.get_node(x) for x in verbs_list_local]
        verb_nodes = [x for x in verb_nodes if x != False]

        next_chain_verbs = []
        for node in verb_nodes:
            for chain in node.next_chains:
                next_chain_verbs.append([x.text for x in chain])

        return next_chain_verbs 

    def append_chain(self, phrase):
        verbs = [x for x in verbs_list if x in phrase]
        verb_nodes = [self.key_map[x] for x in verbs]
        
        nouns = [x for x in nouns_list if x in phrase]
        noun_nodes = [self.key_map[x] for x in nouns]
        print(f"Noun nodes: {[x.text for x in noun_nodes]}")
        
        nodes_list = [self.key_map[x] for x in phrase]
    
        generator = get_node_chain(nodes_list)
        while True:
            try:
                nprev, ncur, nnext = next(generator)
           
                if nprev:
                    ncur.prev_chains.extend([nprev])
                if nnext:
                    ncur.next_chains.extend([nnext])
            except:
                break
                
        for node in verb_nodes:
            node.conn_nouns.extend(noun_nodes)

        for node in noun_nodes:
            node.conn_verbs.extend(verb_nodes)

    def add_phrase(self, phrase):
        phrase = phrase.split()
        phrase = [x for x in phrase if x.isalnum()]
        phrase = [x.strip(string.punctuation).lower() for x in phrase]
        
        for word in phrase:
            self.add_node(word)

        self.append_chain(phrase)

if __name__ == "__main__":
    fd = open('nouns.txt', 'r')
    nouns_list = fd.read()
    nouns_list = nouns_list.split("\n")
    nouns_list = [x for x in nouns_list if x != ""]
    fd.close()

    fd = open('verbs.txt', 'r')
    verbs_list = fd.read()
    verbs_list = verbs_list.split("\n")
    verbs_list = [x for x in verbs_list if x != ""]
    fd.close()

    nmap = NodeMap()

    # g = get_node_chain("I like playing tennis".split())
    # while True:
    #     print(next(g))

    fd = open('nouns.txt', 'r')
    nouns_list = fd.read()
    nouns_list = nouns_list.split("\n")
    nouns_list = [x for x in nouns_list if x != ""]
    fd.close()

    fd = open('verbs.txt', 'r')
    verbs_list = fd.read()
    verbs_list = verbs_list.split("\n")
    verbs_list = [x for x in verbs_list if x != ""]
    fd.close()

    nmap = NodeMap()

    # g = get_node_chain("I like playing tennis".split())
    # while True:
    #     print(next(g))

    while True:
        query_or_data = input("> ")
        if "?" in query_or_data:
            answers = nmap.ask(query_or_data)
            print([x for x in answers])
        else:
           nmap.add_phrase(query_or_data)
           nmap.display()
















