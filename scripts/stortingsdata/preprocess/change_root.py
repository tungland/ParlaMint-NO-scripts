import lxml, glob
from lxml.etree import parse, tostring,Element, ElementTree
from tqdm import tqdm

def change_root(folder, pre2016 = True):
    
    for file in tqdm(glob.glob(folder + "/*")):
        doc = parse(file)
        
        if pre2016:         
            new_root = Element('forhandling')
        else:
            new_root = Element('Forhandlinger')
        
        for e in doc.xpath('/*/*'):
            new_root.append(e)
        
        tree = ElementTree(new_root)    
        tree.write(file)
        
        
