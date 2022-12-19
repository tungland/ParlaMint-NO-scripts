"""Format XML

Formats all xml in current folder according to lxml pretty print
"""
import lxml.etree as et
from stortingsdata.utils import apply_to_file
from glob import glob

def format_xml():
    parser = et.XMLParser(remove_blank_text=True)   
    
    files = glob("*.xml")
    
    for file in files:
        xml = et.parse(file, parser)
        xml.write(file, pretty_print=True, encoding='utf-8')
        
if __name__ == "__main__":
    format_xml()
    