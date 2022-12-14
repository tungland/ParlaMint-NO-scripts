
import pandas as pd
from glob import glob
import spacy
import nltk
import os
from lxml import etree
from tqdm import tqdm
from lxml.etree import parse, Element, tostring
import argparse
from time import time
from tqdm.contrib.concurrent import process_map

ns = {'tei' : "http://www.tei-c.org/ns/1.0"}


def add_attribs(element, dct):
    for key in dct.keys():
        element.attrib[key] = dct[key]

def update_id_attribs(file, doc):
    "Add the '.ana' etxtension to all xml:id attributes in annotated corpus"
    
    name = os.path.splitext(
                        os.path.basename(file)
                    )[0]
    
    for tag in doc.iter():
        if '{http://www.w3.org/XML/1998/namespace}id' in tag.attrib:
            if tag.tag == "{http://www.tei-c.org/ns/1.0}TEI":
                 tag.attrib['{http://www.w3.org/XML/1998/namespace}id'] =  tag.attrib['{http://www.w3.org/XML/1998/namespace}id'] + '.ana'
                
                
            else:
                id_ext = tag.attrib['{http://www.w3.org/XML/1998/namespace}id'].split('.')[-1]                
                tag.attrib['{http://www.w3.org/XML/1998/namespace}id'] = name + '.ana.' + id_ext
        

def update_title(doc):
    """Add .ana to title"""
    
    titles = doc.xpath("/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title", namespaces={"tei" : "http://www.tei-c.org/ns/1.0"})
        
    for title in titles:
        title.text = title.text.replace('[ParlaMint SAMPLE]', '[ParlaMint.ana SAMPLE]')
    
def add_prefix_list(doc):
    "Add prefix list"
    
    prefix_list = etree.fromstring(""" <listPrefixDef>
                                   <prefixDef ident="ud-syn"
                                   matchPattern="(.+)" replacementPattern="#$1">
    <p>Private URIs with this prefix point to elements giving their name. In this document they are simply local references into the UD-SYN taxonomy categories in the corpus root TEI header.</p>
    </prefixDef>
    </listPrefixDef>""")
    encodingDesc = doc.xpath("/tei:TEI/tei:teiHeader/tei:encodingDesc", namespaces=ns)[0]
    
    print(type(prefix_list), type(encodingDesc))
    
    #_ = etree.SubElement(encodingDesc, prefix_list)
    encodingDesc.append(prefix_list)

def annotate_parlamint(files, destination):

    #nlp = spacy.load("annotation/ParlaModel-joint/")
    #model-best
    nlp = spacy.load("annotation/model-best/")
    
    for file in tqdm(files):
        name = file.split('/')[-1].split('.')[0]
        print(file)

        doc = parse(file) 
        
        # Update xml:id
        update_id_attribs(file, doc)
        
        # Update title
        update_title(doc)
        
        # Add prefix list
        #add_prefix_list(doc)
           
        for seg in (doc.xpath("/tei:TEI/tei:text/tei:body/tei:div/tei:u/tei:seg", namespaces={'tei' : "http://www.tei-c.org/ns/1.0" })):
            if seg.text == '':
                continue       
            
            try:
                sents = nltk.tokenize.sent_tokenize(seg.text, language='norwegian')
            except Exception as e:
                with open(f'errors.txt{name}', 'w') as f:
                    f.write(f"{doc}, {seg.attrib}, {e}")
                continue
            
            seg.text = ''
            
            # Get seg id
            seg_id = seg.attrib['{http://www.w3.org/XML/1998/namespace}id']
            
            s_count = 1
            for sent in sents:
                #s = Element("s")
                w_id_dict = dict()
                s = etree.SubElement(seg, 's')
                
                # Add sent_id
                s_id = seg_id + '.' + str(s_count)
                s.set("{http://www.w3.org/XML/1998/namespace}id", s_id)       
                s_count += 1         
                
                n = nlp(sent)
                
                w_count = 1
                for t in n:
                    # Set element name
                    if t.is_punct:
                        ws = etree.SubElement(s, 'pc')
                        w = ws
                        
                    else: 
                        ws = etree.SubElement(s, 'w')
                        w = etree.SubElement(ws, 'w')
                        
                        # Add lemma
                        w.set('lemma', str(t.lemma_))
                        
                    ws.text = str(t)
                        
                    # Add word id
                    w_id = s_id + '.' + str(w_count)
                    ws.set("{http://www.w3.org/XML/1998/namespace}id", w_id)       
                    w_count += 1
                    
                    
                    w.set("{http://www.w3.org/XML/1998/namespace}id", w_id + '.1') 
                    
                    # add id to dct
                    w_id_dict[t.i] = w_id + '.1'
                    
                    
                    
                    
                    # Add morph
                    if t.morph:
                        upos = f"UPosTag={str(t.tag_)}|{str(t.morph)}"
                    else:
                        upos = f"UPosTag={str(t.tag_)}"

                    w.set('msd', upos)
                    
                    # Named entities
                    if t.ent_type_:
                        if t.ent_type_ == 'PER':
                            loc = 'PER'
                        elif t.ent_type_ == 'ORG':
                            loc = 'ORG'
                        elif t.ent_type_ in ['GPE_LOC', 'LOC']:                      
                            loc = 'LOC'
                        else:
                            loc = 'MISC'
                
                        
                        if  t.ent_iob_ == 'B':
                            name_tag = etree.SubElement(s, 'name')
                            
                            # TODO remove
                            # name_tag.set('pos', t.ent_iob_)
                            
                        name_tag.append(ws)
                        
                        #name_tag.set('name', loc)
                        
                    
                        
                        
                    # Add info on right token
                    if (not t.whitespace_) and (not t.is_sent_end) :
                        w.set('join', 'right')                       
                    # TODO: also triggers on end of text. 
                    
                # Add syntactic parses
                linkGrp = etree.SubElement(s, 'linkGrp')
                linkGrp.set("targFunc", 'head argument')
                linkGrp.set("type", 'UD-SYN')
                
                for t in n:
                    link = etree.SubElement(linkGrp, 'link')
                    # lower and replace
                    link.set("ana", f"ud-syn:{t.dep_.lower().replace(':', '_')}")
                    link.set("target", f"#{w_id_dict[t.head.i]} #{w_id_dict[t.i]}")
                    
                
                # TODO: add linkGrp elements                                                                                                                    
                    
                    
        doc.write(os.path.join(destination, name + '.ana.xml'))
    
    del nlp

    


if __name__ == "__main__":
    #source = "../output/*"
    #destination = "parlamint_annotated"
    source = "sample_output/*.xml"
    destination = 'sample_annotation'
    if not os.path.exists(destination):
        os.mkdir(destination)

    files = glob(source)
    #files.remove("sample_output/ParlaMint-NO.xml")
    #print(files)

    annotate_parlamint(files, destination)

