"""Classify the language in u (utterances) in norwegian parliament

Only classifies english, bokmål and nynorsk. Only classifies strings with >10 tokens

"""

# TODO: Implement token split - don't assign language to utterances with less than 10 words. 


import glob
import lxml.etree as ET
from pytextcat import Classifier

from dhlab.nbtokenizer import Tokens

from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

def less_than_ten(text):
    "Check if text has less than 10 tokens"
    toks = Tokens(text)
    return toks.size <= 10

def process(doc : ET.ElementTree, c : Classifier = None):
    #c = Classifier(folder='/home/larsm/my_projects/stortingsdata/scripts/langdet/lm')   
    
    for u in doc.xpath('/tei:TEI/tei:text/tei:body/tei:div/tei:u', namespaces={'tei' : 'http://www.tei-c.org/ns/1.0'}):
        
        text = ' '.join(u.xpath('tei:seg/text()', namespaces={'tei' : 'http://www.tei-c.org/ns/1.0'}))
        
        # if less_than_ten(text):
        #     continue            
        # else:
        lang = c.classify(text)
        
        if lang not in ['nno', 'nob']:
            with open('lang.tsv', 'a') as f:
                f.write(lang + '\n')
        
        u.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = lang
    
    return doc    

def f(doc):
    c = Classifier(folder='lm')   
    xml = ET.parse(doc)
        
    new_xml = process(xml, c)
        
    new_xml.write(doc, pretty_print= True)   

def main():
    docs = glob.glob('output/*')
    # docs = glob.glob('sample_output/*')
    
    c = Classifier(folder='/home/larsm/my_projects/stortingsdata/scripts/langdet/lm')   
    
    
    
    for doc in tqdm(docs):
        xml = ET.parse(doc)
        
        new_xml = process(xml, c)
        
        new_xml.write(doc, pretty_print= True)
    
    #processed = 0
    
   #with multiprocessing.Pool(4) as pool:
    #    pool.map(f, docs)

    #process_map(f, docs, chunksize=1, max_workers=4) 
        
if __name__ == '__main__':
    main()