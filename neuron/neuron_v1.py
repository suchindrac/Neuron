import csv
import re
import copy
import sys
import json        
import pickle

from node_map import *
from neuron_class import *
from place_holder import *
from supporting_funcs import *

def process(node_map):
#     try:
        while True:
            sentence_orig = input("> ")
            if re.search("^g .*$", sentence_orig):
                var_name = sentence_orig.split(" ")[1]
                display_var(var_name)
                continue
            words = sentence_orig.split(" ")

            phs_map = create_ph_map(node_map, sentence_orig)
            node_map.create_neurons_from_text(phs_map)
            # node_map.print_km_data()
            # node_map.print_ph_data()
            extra_words = identify_extra_words(node_map, sentence_orig)
            extra_words = extra_words.strip()    

            add_extra_words(node_map, extra_words)

            node_map.cleanup_neurons()
            set_root_verbs(node_map)
            verb_nodes, noun_nodes = get_verbs_and_nouns(node_map)
            
            # verb_nodes = set_of(verb_nodes)
            noun_nodes = set(noun_nodes)
            
            node_map.verb_nodes = verb_nodes
            node_map.noun_nodes = noun_nodes
            
            node_map.connect_verbs_and_nouns(verb_nodes, noun_nodes)
            # node_map.correct_nodes()

            node_map.display()

            with open("node_map.pkl", "wb") as fd:
                pickle.dump(node_map, fd)
"""
    except:
        print("Exception hit:")
        print(sys.exc_info())
        sys.exit(1)
"""
if __name__ == "__main__":
    verbs, verbs_detailed, nouns = read_verbs_and_nouns()
    node_map = NodeMap(verbs, verbs_detailed, nouns)
   
    process(node_map)

    
        
    
