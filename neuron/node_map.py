import json
import itertools

import copy
from supporting_funcs import *
from neuron_class import *
from place_holder import *

class NodeMap:
    def __init__(self, verbs, verbs_d, nouns):
        self.verbs = verbs
        self.verbs_detailed = verbs_d
        self.nouns = nouns
        self.key_map = {}
        self.place_holders = {}
        self.verb_nodes = []
        self.noun_nodes = []
        
        fd = open('phrase_logic.json', 'r')
        ph_dict = fd.read()
        ph_dict = json.loads(ph_dict)
        fd.close()

        ph_dict = ph_dict["connector definitions"]
        
        for ph in ph_dict.keys():
            ph_o = PlaceHolder(ph)
            for (flag_key, flag_value) in ph_dict[ph].items():
                setattr(ph_o, flag_key, flag_value)
                self.place_holders[ph] = ph_o

    def get_km_node(self, key):
        return self.key_map[key]

    def del_km_node(self, key):
        return self.key_map.pop(key)
        
    def print_km_data(self):
        print("Key map data:")
        for key in self.get_km_keys():
            node = self.get_km_node(key)
            print(f"{key}")

    def print_ph_data(self):
        print("Place holder data:")
        for key in self.get_ph_keys():
            node = self.get_ph_value(key)
            print(f"{key} -> {node.__dict__}")
            
    def get_km_keys(self):
        return list(self.key_map.keys())
    
    def get_ph_keys(self):
        return list(self.place_holders.keys())

    def get_ph_value(self, ph):
        return self.place_holders[ph]
    
    def get_ph_flag(self, ph, flag):
        ph_dict = self.place_holders[ph].__dict__
        ph_keys = ph_dict.keys()
        
        if flag in ph_keys:
            return ph_dict[flag]
        else:
            return False

    def display(self):
        print("The following nodes are created:")
        for node in self.verb_nodes:
            # print(f"Verb node: {node.value}")
            text = node.text
            values = node.value

            for value in values:
                conn_nouns = node.conn_nouns
                to_print = f"<{text}> with root verb "
                to_print += f"<{node.root_verb}> is connected to:\n"
                cns_to_display = []
                for x in conn_nouns:
                    if x.value != []:
                        if type(x.value) == str:
                            cns_to_display.append(x.value)
                        elif type(x.value) == list:
                            cns_to_display.append(x.value[0])
                cns_to_display = set(cns_to_display)
                to_print += f"{cns_to_display}"
                print(to_print)

    def cleanup_neurons(self):
        for key in self.get_km_keys():
            if self.key_map[key].value == []:
                rem = self.key_map.pop(key)
                print(f"Key {key} with value {rem} cleaned")

    def create_neurons_from_text(self, ph_data):
        prev_keys = self.get_km_keys()
        prev_values = [self.key_map[x].value for x in prev_keys]
        # print(ph_data)
        for key in ph_data.keys():
            if ph_data[key] == "":
                continue

            if key in prev_keys:
                continue

            if ph_data[key] in prev_values:
                continue
            
            
            #
            # Set the place holder flags for neuron
            #
            
            if key in self.place_holders.keys():
                value = ph_data[key]

                n = Neuron(key)
                ph_o = self.place_holders[key]
                
                for k in ph_o.__dict__:
                    v = ph_o.__dict__[k]
                    setattr(n, k, v)
                
                root_verb = find_root_verb(self, key)
                setattr(n, 'root_verb', root_verb)
                setattr(n, 'value', value)

                try:
                    is_a = getattr(n, 'is_a')
                except AttributeError:
                    setattr(n, 'is_a', "not known")
                    
                if value != [] and value[0] != "":
                    # print(f"Node {key} with value {value} added")
                    self.key_map[key] = n
            
    def connect_verbs_and_nouns(self, verb_nodes, noun_nodes):
        for node in verb_nodes:
            node.conn_nouns = []

        for node in noun_nodes:
            node.conn_verbs = []
            node.conn_nouns = []
        for verb_node in verb_nodes:
            for noun_node in noun_nodes:
                verb_node.conn_nouns.append(noun_node)
                noun_node.conn_verbs.append(verb_node)
