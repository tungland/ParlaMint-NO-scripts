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
from constants import NS

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input")
args = parser.parse_args()

class DocAnnotater:
    def __init__(self, file) -> None:
        parser = et.XMLParser(remove_blank_text=True)
        xml = et.parse(file, parser)

        self.update_ids_and_names(xml, file)

        #self.nlp = spacy.load("annotation/model-best/")
        self.nlp = spacy.load("/home/larsm/my_projects/stortingsdata/scripts/annotation/spacy-models/model-best/")

        for seg in tqdm(xml.findall("//seg", NS)):
            self.process_seg(seg)

        destination = file.split('.')[0] + '.ana.xml'

        xml.write(destination, pretty_print=True, encoding='utf-8')

    def process_seg(self, seg):
        sents = nltk.tokenize.sent_tokenize(seg.text, language='norwegian')
        seg_id = seg.attrib['{http://www.w3.org/XML/1998/namespace}id']
        seg.text = ''

        sent_count = 1
        for sent in sents:
            sent_id = seg_id + '.' + str(sent_count)
            s_elem = et.SubElement(seg, 's')
            s_elem.set("{http://www.w3.org/XML/1998/namespace}id", sent_id)
            self.process_sent(sent, sent_id, s_elem)
            
            sent_count += 1

    def process_sent(self, sent, sent_id, s_elem):
        #nlp = spacy.load("/home/larsm/my_projects/stortingsdata/annotation/model-best/")

        tokens = self.nlp(sent)

        # Set word id dict
        self.word_ids = dict()

        w_count = 1
        for token in tokens:
            if not token.is_space:
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

        for t in tokens:
            link = et.SubElement(linkGrp, 'link')
            # lower and replace
            link.set("ana", f"ud-syn:{t.dep_.lower().replace(':', '_')}")
            link.set("target", f"#{self.word_ids[t.head.i]} #{self.word_ids[t.i]}")

    @staticmethod
    def check_for_note(elem):
        return elem.find("note") is not None
    
    def process_note(self, seg, s, tokens):
        notes = seg.findall("note", NS)
        
        note = notes[0]
        note_dct = dict()
        
        ind = len(tokens)
          
        
        
        for note in notes:
            seg.remove(note)
        
    
    
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

    # for x in glob("*.xml"):
    #     if x.split(".")[0] != "ParlaMint-NO":
    #         pass
    
    if args.input:
        DocAnnotater(args.input)
    else:   
        for doc in glob('*.xml'):
            if doc.split('.')[0] != "ParlaMint-NO":
                if "ana" not in doc.split("."):
                    DocAnnotater(doc)

if __name__ == "__main__":
    main()
