import re, glob, lxml.etree as et
from tqdm import tqdm

def process_doc(doc):
    # # p1 to ''
    # p1 = r"\xad"
    # # p2 to ' '
    # p2 = r"\t|\xa0|\u2000|\u200a"  
    # # p3 to '-'
    # p3 = r'\u2011'
    
    # Characters to remove
    dct = {
        '' : r"\xad",
        ' ' : r"\t|\xa0|\u2000|\u200a|\u00A0|\u00a0|&#160;",
        '-' : r'\u2011'
    }
    
    for el in doc.iter():
        if isinstance(el.text, str):
            
            for key in dct.keys():
                if re.search(dct[key], el.text):
                    string = re.sub(dct[key], key, el.text)
                    el.text = string
            
            # if re.search(p1, el.text):
            #     string = re.sub(p1, '', el.text)
            #     el.text = string
            # if re.search(p2, el.text):        
            #     string = re.sub(p2, ' ', el.text)
            #     el.text = string
            # if re.search(p3, el.text):        
            #     string = re.sub(p3, ' ', el.text)
            #     el.text = string
               
    return doc


def clean_text(folder):
    """    
    TAB (U+0009)  /all tab -> (U+0020)
    NO-BREAK SPACE (U+00A0) -> (U+0020)
    (U+2000 - U+200A) -> (U+0020)
    NON-BREAKING HYPHEN (U+2011) -> ('-', U+002D)
    SOFT HYPHEN (U+00AD) -> ''
    
    p = r"\xad" # soft hyphen
    p = r"\u2011" # non-braking hyphen
    p = r"\t" #tab
    p = r"\xa0" # no-break space
    p = r'\u2000' # em -quad (space)
    p = r"\u200a" # hair space 
    """
 
    for file in tqdm(glob.glob(folder + '/*')):
        doc = et.parse(file)
        doc = process_doc(doc)
        doc.write(file)
       
    
        
        
    



