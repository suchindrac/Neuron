import csv
import re
import copy
import sys
import json        
import pickle
import os

from node_map import *
from neuron_class import *
from place_holder import *
from supporting_funcs import *
import printing

def process(node_map):
    try:
        while True:
            #
            # Display the prompt
            #
            sentence_orig = input("> ")

            """ To be handled later
            if re.search("^g .*$", sentence_orig):
                var_name = sentence_orig.split(" ")[1]
                display_var(var_name)
                continue
            """
            
            words = sentence_orig.split(" ")
            debug_print("-> Creating place holder map")

            phs_map = create_ph_map(node_map, sentence_orig)
            debug_print("-> Creating nodes")

            #
            # Every sentence input has cur_neurons set to []
            #  at the beginning
            #
            node_map.cur_neurons = []

            #
            # Some neurons are created from the place holder map that is parsed on a
            #  sentence
            #
            node_map.create_neurons_from_text(phs_map)

            #
            # Some neurons are created from independent words which are not part of place
            #  holder structure
            #
            extra_words = identify_extra_words(node_map, sentence_orig)
            extra_words = extra_words.strip()    

            add_extra_words(node_map, extra_words)

            debug_print("-> Cleaning up neurons")
            
            node_map.cleanup_neurons()
            
            debug_print("-> Setting root verbs")
            set_root_verbs(node_map)
            debug_print("-> Getting verbs and nouns")
            verb_nodes, noun_nodes = get_verbs_and_nouns(node_map)
            
            node_map.verb_nodes = verb_nodes
            node_map.noun_nodes = noun_nodes
            
            debug_print("-> Connecting verbs and nouns")
            node_map.connect_verbs_and_nouns()

            node_map.display()

            debug_print("-> Writing to pickle file")
            with open("node_map.pkl", "wb") as fd:
                pickle.dump(node_map, fd)

    except:
        print("Exception hit:")
        print(sys.exc_info())
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "debug":
            printing.debug = True
        
    verbs, verbs_detailed, nouns = read_verbs_and_nouns()
    node_map = NodeMap(verbs, verbs_detailed, nouns)
   
    process(node_map)

    
        
    
