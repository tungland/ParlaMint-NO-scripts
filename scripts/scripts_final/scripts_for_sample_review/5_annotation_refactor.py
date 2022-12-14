"""Refactor Spacy annotation scrips

ParlaMint -> ParlaMint.ana
"""

import pandas as pd

import spacy
import nltk
import os
import lxml.etree as et
import argparse
from glob import glob
from tqdm import tqdm

from constants import NS

def link_grp():
    pass

def tag_named_entities(token, elem, s_elem, name_tag):
    if token.ent_type_ == 'PER':
        loc = 'PER'
    elif token.ent_type_ == 'ORG':
        loc = 'ORG'
    elif token.ent_type_ in ['GPE_LOC', 'LOC']:                      
        loc = 'LOC'
    else:
        loc = 'MISC'                
    
    if  token.ent_iob_ == 'B':
        name_tag = et.SubElement(s_elem, 'name')
    
    name_tag.append(elem)
    return name_tag    
    
def process_token(token, id, s_elem):
    
    if token.is_punkt:
        elem = et.SubElement(s_elem, 'pc')
    else:
        elem = et.SubElement(s_elem, 'w')
    
    # Add text
    elem.text = str(token).strip()    
    
    ## Add attributes
    
    # ID
    elem.set("{http://www.w3.org/XML/1998/namespace}id", id)
    
    # lemma
    if token.is_punkt:
        elem.set('lemma', str(token.lemma_).strip())
    
    # Upos
    if token.morph:
        upos = f"UPosTag={str(token.tag_)}|{str(token.morph)}"
    else:
        upos = f"UPosTag={str(token.tag_)}"
        
    # Named entities:
    if token.ent_type_:
        tag_named_entities(token, elem, s_elem)            

def process_sent(sent, sent_id, s_elem):
    nlp = spacy.load("annotation/model-best/")  
    
    tokens = nlp(sent)
    
    w_count = 1
    for token in tokens:
        if not token.is_space():
            word_id = sent_id + '.' + w_count            
            process_token(token, word_id, s_elem)
            w_count += 1

def process_seg(seg):
    sents = nltk.tokenize.sent_tokenize(seg.text, language='norwegian')
    seg_id = seg.attrib['{http://www.w3.org/XML/1998/namespace}id']
    seg.text = ''
    
    sent_count = 1
    for sent in sents:
        sent_id = seg_id + '.' + str(sent_count)
        s_elem = et.SubElement(seg, 's')  
        s_elem.set("{http://www.w3.org/XML/1998/namespace}id", sent_id)      
        process_sent(sent, sent_id, s_elem)
        sent_count += 1
    

def annotate_doc(xml, dest):
    
    # TODO: update header
    # TODO update ids
    
    
    nlp = spacy.load("annotation/model-best/")
    
    for seg in xml.findall("//seg", NS):
        process_seg(seg)
    
    
   