import re
import glob
from lxml import etree
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

def process_seg(file_path):
    tree = etree.parse(file_path)
    namespaces = {'tei' : "http://www.tei-c.org/ns/1.0"}
    
    #p = r"\([^\(\)]*(?:i salen|klubb[ea]r)[^\(\)]*\)"
    
    p = r'\([^\(\)]+\):? ?'
    
    segs = tree.xpath("//tei:seg", namespaces=namespaces)
    
    for s in segs: 
        # Return segs matching pattern
        t = re.search(p, s.xpath("string()"))
        
        # If match 
        if t:
            
            ms = re.finditer(p, s.xpath("string()"))  
            split = re.split(p, s.xpath("string()"))
            
            count = 0
            
            # Replace original tag text with first text        
            s.text = split[0].rstrip()
            new_seg = s
            a = s.attrib['{http://www.w3.org/XML/1998/namespace}id']
            
            for m in ms:
                # Create note element
                note = etree.Element('note')
                note.text = m.group(0).rstrip()
                new_seg.addnext(note)
                
                count += 1
                
                # Create new segment
                new_seg = etree.Element('seg')
                # Generate new id for new seg tag. Add s + count 
                new_seg.attrib['{http://www.w3.org/XML/1998/namespace}id'] = a + 's' + str(count)
                new_seg.text = split[count].rstrip()
                note.addnext(new_seg)

    return tree        

def main_loop(file):
    tree = process_seg(file)       
    tree.write(file)

def handle_notes(folder):
    docs = glob.glob(folder + "/*.xml")
    
   # process_map(main_loop, docs, chunksize=1, max_workers=36)
    process_map(main_loop, docs, chunksize=1)
    
                       