import json
import itertools

import copy
from supporting_funcs import *
from neuron_class import *
from place_holder import *
from printing import *

class NodeMap:
    def __init__(self, verbs, verbs_d, nouns):
        self.verbs = verbs
        self.verbs_detailed = verbs_d
        self.nouns = nouns
        self.key_map = {}
        self.place_holders = {}
        self.verb_nodes = []
        self.noun_nodes = []
        self.neurons = []
        self.cur_neurons = []

        #
        # Read the place holder dictionary and create place
        #  holder objects with key-value type of flags
        #
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

    #
    # Get a node (neuron) by its UUID
    #  Note: Every neuron is assigned a UUID by default
    #
    def get_node_by_uuid(self, uuid):
        for node in self.key_map.values():
            if node.uuid == uuid:
                return node

        return False

    #
    # Get a key map node from a key
    #
    def get_km_node(self, key):
        return self.key_map[key]

    #
    # Delete a key map node
    #
    def del_km_node(self, key):
        return self.key_map.pop(key)

    #
    # Print key map data
    #  Note: Key map data means key-value pairs stored as part of key map objects
    #
    def print_km_data(self):
        debug_print("    Key map data:")
        for key in self.get_km_keys():
            node = self.get_km_node(key)
            debug_print(f"{key}")

    #
    # Print place holder data
    #  Note: Place holder data means key-value pairs of place holders
    #
    def print_ph_data(self):
        debug_print("    Place holder data:")
        for key in self.get_ph_keys():
            node = self.get_ph_value(key)
            debug_print(f"{key} -> {node.__dict__}")

    #
    # Get all the keys of the key map
    #
    def get_km_keys(self):
        return list(self.key_map.keys())

    #
    # Get the place holder keys
    #
    def get_ph_keys(self):
        return list(self.place_holders.keys())

    #
    # Get a place holder value based on key
    #
    def get_ph_value(self, ph):
        return self.place_holders[ph]

    #
    # Get a place holder flag (value corresponding to a key stored in a place holder object)
    #
    def get_ph_flag(self, ph, flag):
        ph_dict = self.place_holders[ph].__dict__
        ph_keys = ph_dict.keys()
        
        if flag in ph_keys:
            return ph_dict[flag]
        else:
            return False

    #
    # Display what you want
    #
    def display(self):
        print("-> The following nodes are created:")
        for key in self.get_km_keys():
            node = self.get_km_node(key)
            print(f"    {node.text} -> {node.value}")
        print("-> The following connections are created:")
        for key in self.get_km_keys():
            node = self.get_km_node(key)
            if node.root_verb == None:
                continue
            text = node.text
            values = node.value

            for value in values:
                conn_nouns = node.conn_nouns
                to_print = f"    <{node.text}> with root verb "
                to_print += f"<{node.root_verb}> is connected to:\n"
                cns_to_display = []
                for x in conn_nouns:
                    if x.value != []:
                        if type(x.value) == str:
                            cns_to_display.append(x.value)
                        elif type(x.value) == list:
                            cns_to_display.append(x.value[0])
                cns_to_display = set(cns_to_display)
                to_print += f"    {cns_to_display}"
                print(to_print)

    #
    # If a key has null value ([]), then delete it
    #
    def cleanup_neurons(self):
        for key in self.get_km_keys():
            if self.key_map[key].value == []:
                rem = self.key_map.pop(key)
                debug_print(f"    Key {key} with value {rem} cleaned")

    #
    # Get a node using its value as input
    #
    def get_node_from_value(self, value):
        for k in self.get_km_keys():
            if value == self.key_map[k].value:
                return self.get_km_node(k)

        return False

    #
    # Create neurons from text input by user
    #
    def create_neurons_from_text(self, ph_data):
        prev_keys = self.get_km_keys()

        debug_print(f"Previous keys: {prev_keys}")
        debug_print(f"    Place holder data:\n{ph_data}\n")
        
        for key in ph_data.keys():
            if ph_data[key] == "":
                continue

            #
            # Set the place holder flags for neuron based on rules below:
            #  a. If the key is in the place holder keys
            #  b. Note: Temporarily ignore keys which have more than one value
            #  c. Ignore nodes which are already created in the key map (have a key in the key map)
            #
            if key in self.place_holders.keys():
                value = ph_data[key]

                if len(value) != 1:
                    continue

                if value[0] in prev_keys:
                    debug_print(f"Node {value[0]} already there")
                    continue

                #
                # Neuron is created based on value
                #  Note: As of now it is value[0], to be handled later
                #
                n = Neuron(value[0])
                ph_o = self.place_holders[key]

                #
                # Set the flags in the place holder, to the neuron created
                #
                for k in ph_o.__dict__:
                    v = ph_o.__dict__[k]
                    setattr(n, k, v)

                #
                # Find the root verb for each key
                #  and assign it to the 'root_verb' attribute of the neuron class
                #
                root_verb = find_root_verb(self, key)
                if root_verb:
                    setattr(n, 'root_verb', root_verb)

                #
                # Set the text and value for a neuron
                #
                setattr(n, 'text', value[0])
                setattr(n, 'value', [value[0]])

                #
                # Set the attribute is_a in a neuron, which
                #  represents whether a neuron is a verb or a noun
                #
                try:
                    is_a = getattr(n, 'is_a')
                except AttributeError:
                    setattr(n, 'is_a', "not known")

                #
                # Print the message indicating that a neuron has been added
                #
                if value != [] and value[0] != "":
                    debug_print(f"    Node {value[0]} with value {value} added")
                    self.key_map[value[0]] = n
                    self.cur_neurons.append(n)

    #
    # Connect the verbs and nouns in the _current sentence added_
    #
    def connect_verbs_and_nouns(self):
        verb_nodes = [x for x in self.cur_neurons if x.root_verb != None]
        noun_nodes = [x for x in self.cur_neurons if x.root_verb == None]
        
        for verb_node in verb_nodes:
            for noun_node in noun_nodes:
                debug_print(f"Connecting {verb_node.text} with {noun_node.text}")
                verb_node.conn_nouns.append(noun_node)
                # noun_node.conn_verbs.append(verb_node)
