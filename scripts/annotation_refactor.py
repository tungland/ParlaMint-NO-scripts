"""Refactor Spacy annotation scrips

ParlaMint -> ParlaMint.ana
"""
import spacy
import nltk
import os
import lxml.etree as et
import argparse
from glob import glob
from tqdm import tqdm
from dhlab.nbtokenizer import tokenize
from stortingsdata.constants import NS

from stortingsdata.dhlab_sent_tokenizer import dhlab_sent_tokenize

from stortingsdata.utils import debug, pprint
import logging

from datetime import datetime

now = datetime.now().strftime("%Y%m%d%H%M%S")

logging.basicConfig(filename=f"/home/larsm/projects/parlamint/logs/docannotator_partial_{now}.log",
                    level=logging.ERROR
                    )

spacy.require_gpu()


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input")
args = parser.parse_args()



class DocAnnotater:
    def __init__(self, file) -> None:
        self.name = file
        parser = et.XMLParser(remove_blank_text=True)
        xml = et.parse(file, parser)

        self.update_ids_and_names(xml, file)

        #self.nlp = spacy.load("annotation/model-best/")
        
        self.nlp = spacy.load("/home/larsm/projects/parlamint/ParlaMint-NO-scripts/scripts/annotation/spacy-models/model-best")
        #
        for seg in tqdm(xml.findall("//seg", NS)):
            self.process_seg(seg)

        destination = file.split('.')[0] + '.ana.xml'

        xml.write(destination, pretty_print=True, encoding='utf-8')

    def process_seg(self, seg):
        # Check for notes
        self.note = False
        if self.check_for_note(seg):
            #print("processing note...")
            text = self._merge_note_tail(seg)
            self.process_note(seg)
            
            self.note = True
        else:
            text = seg.text
        # Create note dict with index + elem
        
        
        sents = nltk.tokenize.sent_tokenize(text, language='norwegian')
        #sents = list(dhlab_sent_tokenize(text))
        
        #assert " ".join(sents) == text, f"{seg.attrib}\t{sents}\t{text}"
        
        #assert len(sents) == len(sents_2), f"{et.tostring(seg).decode()}    {sents} {sents_2}   {text}"
                
        seg_id = seg.attrib['{http://www.w3.org/XML/1998/namespace}id']
        seg.text = ''

        sent_count = 1
        for sent in sents:
            sent_id = seg_id + '.' + str(sent_count)
            s_elem = et.SubElement(seg, 's')
            s_elem.set("{http://www.w3.org/XML/1998/namespace}id", sent_id)
            self.process_sent(sent, sent_id, s_elem)
            sent_count += 1
        
        if self.note:
            self.insert_note(seg)


    def process_sent(self, sent, sent_id, s_elem):
        #nlp = spacy.load("/home/larsm/my_projects/stortingsdata/annotation/model-best/")

        tokens_1 = self.nlp(sent)

        # filter nonestadard whitespace
        tokens = [x for x in tokens_1 if not x.is_space]
        if len(tokens) != len(tokens_1):
            logging.error(f"{str(s_elem.attrib)} has whitespace")
        
        # Set word id dict
        self.word_ids = dict()

        w_count = 1
        for token in tokens:
           # if not token.is_space:
            word_id = sent_id + '.' + str(w_count)
            self.process_token(token, word_id, s_elem)
            w_count += 1

        self.syntactic_parses(tokens, s_elem)
        
    def process_token(self, token, id, s_elem):
        if token.is_punct:
            elem = et.SubElement(s_elem, 'pc')
        else:
            elem = et.SubElement(s_elem, 'w')

        # Add text
        elem.text = str(token).strip()

        ## Add attributes

        # ID
        elem.set("{http://www.w3.org/XML/1998/namespace}id", id)

        # lemma
        if not token.is_punct:
            elem.set('lemma', str(token.lemma_).strip())

        # Upos
        if token.morph:
            upos = f"UPosTag={str(token.tag_)}|{str(token.morph)}"
        else:
            upos = f"UPosTag={str(token.tag_)}"
        elem.set('msd', upos)


        # Named entities:
        if token.ent_type_:
            self.tag_named_entities(token, elem, s_elem)

        # Add id for syntactic parse
        self.word_ids[token.i] = id
        
        # Add join info
        # Add info on right token
        if (not token.whitespace_) and (not token.is_sent_end) :
            elem.set('join', 'right') 


    def tag_named_entities(self, token, elem, s_elem):
        """Add named entity info to names.
        """
        if token.ent_type_ == 'PER':
            loc = 'PER'
        elif token.ent_type_ == 'ORG':
            loc = 'ORG'
        elif token.ent_type_ in ['GPE_LOC', 'LOC']:
            loc = 'LOC'
        else:
            loc = 'MISC'

        if  token.ent_iob_ == 'B':
            self.name_tag = et.SubElement(s_elem, 'name')
            self.name_tag.attrib["type"] = loc

        self.name_tag.append(elem)

    def syntactic_parses(self, tokens, s_elem):
        """Add syntactic parse info to sentence.
        Uses self.words_ids to fin word ids.

        :param tokens: spacy tokens
        :type tokens: spacy nlp
        :param s_elem: <s>
        :type s_elem: et.Element
        """
        linkGrp = et.SubElement(s_elem, 'linkGrp')
        linkGrp.set("targFunc", 'head argument')
        linkGrp.set("type", 'UD-SYN')

        # Remove multiple roots
        
        root_count = 0
        for t in tokens:
            link = et.SubElement(linkGrp, 'link')
            
            # DEBUG
            #assert t.i in self.word_ids.keys(), f"{t.i}\t-{t}- token"
            #assert t.head.i in self.word_ids.keys(), f"{t.i}\t-{t}- token"
           
            
            # lower and replace
            ## Set value
            value = f"ud-syn:{t.dep_.lower().replace(':', '_')}"
            target = self.word_ids.get(t.head.i, 0)
            self_id = self.word_ids.get(t.i, 0)
            
            if value == "ud-syn:root":
                root_count += 1
                if root_count > 1:                
                    logging.warning("Multiple roots in %s", str(s_elem.attrib))
                    value = "ud-syn:parataxis"
                    target = root_id
                    
                    
                else:
                    # Normal root
                    # Set extra root to point to this
                    root_id = self_id
                    target = s_elem.attrib['{http://www.w3.org/XML/1998/namespace}id']
                    
            #
            link.set("ana", value)
            link.set("target", f"#{target} #{self_id}")

    @staticmethod
    def check_for_note(elem):
        return elem.find("note", NS) is not None
    
    def process_note(self, seg):
        notes = seg.findall("note", NS)
        self.note_dct = dict()
        
        ind = len(tokenize(seg.text))       
        
        for note in notes:
            self.note_dct[ind] = note
            if note.tail:
                ind += len(tokenize(note.tail))    
            
            note.tail = ''        
            seg.remove(note)        

    def insert_note(self, seg):
        sents = seg.findall('s')
        assert len(sents) > 0, f" Did not find sents {et.tostring(seg)}"

        for key, val in self.note_dct.items():
            logging.info("inserting in-segment note %s %s", key, val)
            s, ind = self._find_sentence(sents, key + 1)
            logging.warning("Inserting note %s at %s", str(s.attrib), str(ind))
            s.insert(ind, val)
     
    def _find_sentence(self, sent_list, ind):
        """Finds index to insert sub sentence note in sentence
        
        sent_list: list of sentence elements
        ind: Index within original sentence
        """
        
        for sent in sent_list:
            # Check for names in sentence
            
            if self._name_in_sent(sent):
                ind = self._fix_name(sent, ind)           
            
            if len(sent) > ind:
                return sent, ind
            else:
                ind -= len(sent)
        
        # Append note to end of sentence
        return sent, -1        
        #raise ValueError("find sentence missed the target")

        
    @staticmethod
    def _name_in_sent(sent):
        return sent.find("name") is not None
    
    def _count_words_in_name(self, sent):
        names = sent.findall("name")
        for name in names:
            yield name.getparent().index(name), len(name.findall("w"))
        
    def _fix_name(self, sent, note_index):
        for name_index, name_len in self._count_words_in_name(sent):
            if name_index < note_index:
                note_index -= name_len
        return note_index
    
    @staticmethod
    def _merge_note_tail(seg):
        text = seg.text
        
        for note in seg.findall("note", NS):
            #print(note)
            if note.tail:
                if note.tail[0].isalnum():
                    space = ' '
                else:
                    space = ''
                text += space + note.tail
         
        return text   
    
    def update_ids_and_names(self, xml, file):
        self.update_tag_ids(xml, file)
        self.update_title(xml)

    def update_tag_ids(self, xml, file):
        "Add the '.ana' etxtension to all xml:id attributes in annotated corpus"
        name = os.path.splitext(os.path.basename(file))[0]
        for tag in xml.iter():
            if '{http://www.w3.org/XML/1998/namespace}id' in tag.attrib:
                if tag.tag == "{http://www.tei-c.org/ns/1.0}TEI":
                    tag.attrib['{http://www.w3.org/XML/1998/namespace}id'] =  tag.attrib['{http://www.w3.org/XML/1998/namespace}id'] + '.ana'
                else:
                    id_ext = tag.attrib['{http://www.w3.org/XML/1998/namespace}id'].split('.')[-1]
                    tag.attrib['{http://www.w3.org/XML/1998/namespace}id'] = name + '.ana.' + id_ext

    def update_title(self, xml):
        """Add .ana to title"""
        titles = xml.findall("//titleStmt/title", NS)
        for title in titles:
            title.text = title.text.replace('[ParlaMint SAMPLE]', '[ParlaMint.ana SAMPLE]')

def main():
    logging.info("Starting new parse...")
    
    ana_file_names = [x.split(".")[0] for x in glob("*.ana.xml")]  
    
    files = list()
    for file in glob('*.xml'):
        if file.split('.')[0] != "ParlaMint-NO":
                if "ana" not in file.split("."):
                    if file.split('.')[0] not in ana_file_names:
                        files.append(file)
    
    
    if args.input:
        DocAnnotater(args.input)
    else:   
        for doc in tqdm(files):
            logging.info(f"Now annotating {doc}")
            try:    
                DocAnnotater(doc)
            except Exception as e:
                logging.error(f"{doc} failed with {e}")
            

    logging.info("Program finished!\n")
    
if __name__ == "__main__":
    main()
