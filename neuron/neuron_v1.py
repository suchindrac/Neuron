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
    # try:
        while True:
            #
            # Display the prompt
            #
            sentence_orig = input("> ")

            #
            # * User enters sentence below:
            # I went to house of Athreya situated at Jayanagar
            #  to drink a cup of whiskey on the weekend by bus every week
            #
            """ To be handled later
            if re.search("^g .*$", sentence_orig):
                var_name = sentence_orig.split(" ")[1]
                display_var(var_name)
                continue
            """
            
            words = sentence_orig.split(" ")
            debug_print("-> Creating place holder map")

            phs_map = create_ph_map(node_map, sentence_orig)

            #
            # * Place holder map is below:
            #
            # {'situated at': ['Jayanagar'], 'had been': [], 'in front of': [], 'by using': [],
            #  'once every': [], 'will be': [], 'owned by': [], 'I': [], 'will': [], 'is_a': [],
            #  'been': [], 'at': ['Jayanagar'], 'in': [], 'by': ['bus'], 'every': ['week'],
            #  'to': ['house'], 'on': ['the weekend'], 'from': [], 'for': [], 'go to that': [],
            #  'was': [], 'of': ['Athreya'], 'feel like': [], 'and': [], 'before': [],
            #  'after': [], 'now': [], 'that': [], 'to that': []}
            #
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
            # * Key map is below:
            #
            # {
            #    'Jayanagar': <neuron_class.Neuron object at 0x1046a7f70>,
            #    'bus': <neuron_class.Neuron object at 0x1046a7fd0>,
            #    'week': <neuron_class.Neuron object at 0x104854af0>,
            #    'house': <neuron_class.Neuron object at 0x104854b20>,
            #    'the weekend': <neuron_class.Neuron object at 0x104854b50>,
            #    'Athreya': <neuron_class.Neuron object at 0x104854b80>,
            #    'I': <neuron_class.Neuron object at 0x104854c40>,
            #    'went': <neuron_class.Neuron object at 0x104854c70>,
            #    'drink': <neuron_class.Neuron object at 0x104854ca0>,
            #    'a': <neuron_class.Neuron object at 0x104854d00>,
            #    'cup': <neuron_class.Neuron object at 0x104854d30>,
            #    'whiskey': <neuron_class.Neuron object at 0x104854d90>
            #  }
            #
            
            #
            # Some neurons are created from independent words which are not part of place
            #  holder structure
            #
            extra_words = identify_extra_words(node_map, sentence_orig)
            extra_words = extra_words.strip()    

            #
            # * Extra words are below:
            #
            # I went drink a cup whiskey week
            #
            add_extra_words(node_map, extra_words)

            debug_print("-> Cleaning up neurons")
            
            node_map.cleanup_neurons()
            
            debug_print("-> Setting root verbs")
            set_root_verbs(node_map)

            #
            # * Root verbs are set as below:
            #
            # Jayanagar -> None
            # bus -> bus
            # week -> None
            # house -> house
            # the weekend -> None
            # Athreya -> None
            # I -> None
            # went -> go
            # drink -> drink
            # a -> None
            # cup -> cup
            # whiskey -> None
            #
            debug_print("-> Getting verbs and nouns")
            verb_nodes, noun_nodes = get_verbs_and_nouns(node_map)

            #
            # * Verb nodes and noun nodes are as follows
            #
            # Verb nodes:
            # went -> ['went']
            # bus -> ['bus']
            # house -> ['house']
            # cup -> ['cup']
            # drink -> ['drink']
            #
            # Noun nodes:
            # week -> ['week']
            # a -> ['a']
            # I -> ['I']
            #
            
            node_map.verb_nodes = verb_nodes
            node_map.noun_nodes = noun_nodes
            
            debug_print("-> Connecting verbs and nouns")
            node_map.connect_verbs_and_nouns()

            #
            # * Nodes and connections are below:
            #
            #  Jayanagar -> ['Jayanagar']
            #  bus -> ['bus']
            #  week -> ['week']
            #  house -> ['house']
            #  the weekend -> ['the weekend']
            #  Athreya -> ['Athreya']
            #  I -> ['I']
            #  went -> ['went']
            #  drink -> ['drink']
            #  a -> ['a']
            #  cup -> ['cup']
            #  whiskey -> ['whiskey']
            #         
            #  <bus> with root verb <bus> is connected to:
            #  {'a', 'I', 'the weekend', 'week', 'Jayanagar', 'whiskey', 'Athreya'}
            #  <house> with root verb <house> is connected to:
            #  {'a', 'I', 'the weekend', 'week', 'Jayanagar', 'whiskey', 'Athreya'}
            #  <went> with root verb <go> is connected to:
            #  {'a', 'I', 'the weekend', 'week', 'Jayanagar', 'whiskey', 'Athreya'}
            #  <drink> with root verb <drink> is connected to:
            #  {'a', 'I', 'the weekend', 'week', 'Jayanagar', 'whiskey', 'Athreya'}
            #  <cup> with root verb <cup> is connected to:
            #  {'a', 'I', 'the weekend', 'week', 'Jayanagar', 'whiskey', 'Athreya'}
            #
            node_map.display()

            debug_print("-> Writing to pickle file")
            with open("node_map.pkl", "wb") as fd:
                pickle.dump(node_map, fd)

    # except:
    #     print("Exception hit:")
    #     print(sys.exc_info())
    #     sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1] == "debug":
            printing.debug = True
        
    verbs, verbs_detailed, nouns = read_verbs_and_nouns()
    node_map = NodeMap(verbs, verbs_detailed, nouns)
   
    process(node_map)

    
        
    
