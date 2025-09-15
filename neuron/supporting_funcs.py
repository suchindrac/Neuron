import csv
import copy

from node_map import *
from neuron_class import *
from place_holder import *

def find_root_verb(node_map, verb):
    root_verb = None
    for verb_line in node_map.verbs_detailed:
        if verb in verb_line:
            root_verb = verb_line[0]
            break
    return root_verb

def read_verbs_and_nouns():
    fd = open('verbs.txt', 'r')
    reader = csv.reader(fd)
    header = next(reader)
    verbs = []
    verbs_detailed = []
    for row in reader:
        row = [x for x in row if x != '']
        verbs.extend(row)
        verbs_detailed.append(row)
    fd.close()

    fd = open('nouns.txt', 'r')
    nouns = fd.read()
    nouns = nouns.split("\n")
    nouns = [x for x in nouns if x != '']
    fd.close()

    return verbs, verbs_detailed, nouns

def read_sentence():
    fd_sentence = open('letter.txt', 'r')
    sentence_orig = fd_sentence.read()
    words = sentence_orig.split()
    words = [x.strip() for x in words]   

    return sentence_orig, words

def create_ph_map(node_map, sentence_orig):
    ph_data = {}

    #
    # Replace each place holder in the string with the word PH
    #
    sentence = copy.copy(sentence_orig)
    for ph in node_map.get_ph_keys():
        sentence = sentence.replace(f" {ph} ", " PH ")

    #
    # At each place holder, read the remaining sentence from the next
    #  word after the place holder
    #
    for ph in node_map.get_ph_keys():
        remaining = read_remaining(sentence_orig, ph)
        if remaining:
            if ph in ph_data.keys():
                ph_data[ph].append([remaining])
            else:
                ph_data[ph] = [remaining]
        else:
            ph_data[ph] = ""

    #
    # Get the remaining sentence after each place holder
    # Split the remaining sentence on the basis of the word PH
    # Pick the part of the sentence which comes before the next place holder
    #  which is indicated by the word PH
    #
    for key in ph_data.keys():
        values = ph_data[key]
        if values == []:
            continue
        for ph in node_map.get_ph_keys():
            values = [x.replace(f" {ph} ", " PH ") for x in values]

        values = [x.split(" PH ")[0] for x in values]
        ph_data[key] = values

    return ph_data

def read_remaining(sentence, cur_word):
    parts = sentence.split(f" {cur_word} ")
   
    if len(parts) > 1:
        return parts[1]

def identify_extra_words(node_map, sentence_orig):
    sorted_phs = sorted(node_map.get_ph_keys(), key=lambda x: len(x), reverse=True)
    for ph in sorted_phs:
        if ph in sentence_orig:
            sentence_orig = sentence_orig.replace(f" {ph} ", ' ')
            
            if ph in node_map.get_km_keys():
                value = node_map.key_map[ph].value
                sentence_orig = sentence_orig.replace(f" {value} ", " ")

    return sentence_orig

def set_of(nodes):
    node_values = []
    nodes_new = []
    for node in nodes:
        # print(f"Node value set_of: {node.text} {node.value}")
        if node.value not in node_values:
            # print(f"Node value set_of: {node.text} {node.value}")
            node_values.append(node.value)
            nodes_new.append(node)

    return nodes_new

def add_extra_words(node_map, extra_words):
    extra_words = extra_words.split(" ")
    extra_words = [x.strip() for x in extra_words]

    prev_keys = node_map.get_km_keys()
    prev_values = [node_map.key_map[x].value for x in prev_keys]

    for extra_word in extra_words:
        if extra_word in prev_keys:
            continue
        if extra_word in prev_values:
            continue
        # print(f"Extra word: {extra_word}")
        n = Neuron(extra_word)
        
        if extra_word in node_map.verbs:
            n.is_verb = True
            n.root_verb = find_root_verb(node_map, extra_word)
        elif extra_word in node_map.nouns:
            n.is_noun = True
            n.person = True
        else:
            n.is_noun = True

        n.value = [extra_word]
        n.text = extra_word

        node_map.key_map[extra_word] = n

def get_verbs_and_nouns(node_map):
    verb_nodes = []
    noun_nodes = []

    pairs = []
    for key in node_map.get_km_keys():
        node = node_map.get_km_node(key)
        value = node.value

        if node.next_is_verb and (value in node_map.verbs):
            verb_nodes.append(node)
        elif node.next_is_noun:
            noun_nodes.append(node)
        elif node.is_verb:
            # print(f"Verb node: {node.text}")
            verb_nodes.append(node)
        elif key in node_map.verbs:
            verb_nodes.append(node)
        elif node.is_noun:
            noun_nodes.append(node)

        if node.is_verb:
            pairs.append((node.text, node.value))

    # print(f"Verb nodes: {[x.text for x in verb_nodes]}")
    verb_nodes = set(verb_nodes)
    
    return verb_nodes, noun_nodes, pairs

def set_root_verbs(node_map):
    for key in node_map.get_km_keys():
        value = node_map.key_map[key].value[0]
        root_verb = find_root_verb(node_map, value)
        if root_verb:
            node_map.key_map[key].root_verb = root_verb
            
