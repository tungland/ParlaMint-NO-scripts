"""Fix dependency error

UD-Syn dep 'Root' references itself as target. It should target its parent sentence
"""

import lxml.etree as et
from glob import glob

ns = {"tei" : "http://www.tei-c.org/ns/1.0"}


def process_sent(s):
    id = s.attrib['{http://www.w3.org/XML/1998/namespace}id']
    
    linkGrp = s.find("{http://www.tei-c.org/ns/1.0}linkGrp")
    links = linkGrp.findall("{http://www.tei-c.org/ns/1.0}link")
    
    for link in links:
        if link.attrib["ana"] == "ud-syn:root":
            old_attrib_link =  link.attrib["target"].split()[1]
            new_attrib = f"#{id} {old_attrib_link}" 
            link.attrib["target"] = new_attrib
            
def parse_doc(doc):
    parser = et.XMLParser(remove_blank_text=True)
    
    xml = et.parse(doc, parser)

    sents = xml.xpath("//tei:s", namespaces=ns)
    
    for s in sents:
        process_sent(s)  
        
    xml.write(doc, pretty_print=True, encoding='utf-8')

def main():
    #doc = "/home/larsm/my_projects/ParlaMint/Data/ParlaMint-NO/ParlaMint-NO_2008-04-08-lower.ana.xml"
    #doc = "/home/larsm/my_projects/ParlaMint/Data/ParlaMint-NO/ParlaMint-NO_2004-09-30.xml"
    #file_paths = "/home/larsm/my_projects/ParlaMint/Data/ParlaMint-NO/*.xml"
    file_paths = "*"

    
    for doc in glob(file_paths):
        parse_doc(doc)
        
if __name__ == "__main__":
    main()