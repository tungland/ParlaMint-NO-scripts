"""Add files to meta

Adds the filenames of .xml and .ana.xml to their corresponding metadata-file
"""

from venv import create
import lxml.etree as et
from os.path import basename, join
from glob import glob

xi = "http://www.w3.org/2001/XInclude"
tei = "http://www.tei-c.org/ns/1.0"
ns = {
    'xi' : xi,
    'tei' : tei
    }


class fileAdder:
    def __init__(self, path) -> None:
        # Add header files
        header = join(path, 'ParlaMint-NO.xml')
        annotated_header = join(path, 'ParlaMint-NO.ana.xml')
        
        
        # Parse files
        ftexts = [x for x in glob(join(
            path,
            "*[!.ana].xml"
        ))
                       if x != header]
        
        fanas = [x for x in glob(join(
            path,
            "*.ana.xml"
        ))
                      if x != annotated_header]

        
        # Create data dict
        self.data = {
            header : ftexts,     
            annotated_header : fanas
        }
        
        # strip whitespace to make lxml prettyprint function correctly
        self.parser = et.XMLParser(remove_blank_text=True)
        
    def create_element(self, part_name):
        "Create xml element from doc_name"
        
        el = et.Element("{http://www.w3.org/2001/XInclude}include", nsmap=ns)
        el.set('href', basename(part_name))
        
        return el
        
    def add_elements(self, header):
        "Adds elements to doc. Strips old."
        
        
        xml = et.parse(header, self.parser)
        root = xml.getroot()
        
        print(xml)
        
        # Remove old
        et.strip_elements(root, "{http://www.w3.org/2001/XInclude}include")       
        
        #
        for part in self.data[header]:         
            new_element = self.create_element(part)
            root.append(new_element)
    
        xml.write(header, pretty_print=True, encoding='utf-8')
    
    def run(self):  
        "Add elements to each header"     
        for header in self.data.keys():
            print(header)
            self.add_elements(header)


def main():
    path = 'sample2'
    path = ""     
    
    adder = fileAdder(path)
    
    adder.run()
    
if __name__ == "__main__":
   main() 