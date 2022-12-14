"""Clean parlamint text

Remove Nonestandard characters

Remove associatet tags and UD dependants    
"""
# To remove
# U+00ad
"­"

# To replace
#U+00a0
" "
#U+2007
" "

import lxml.etree as et
from glob import glob 
from tqdm import tqdm

def replace_text(str):
    return str.replace("­", "").replace(" ", " ").replace(" ", " ")

def clean_text(xml):
    deleted_ids = list()
    
    for node in xml.iter():    
        if node.text:
            node.text = replace_text(node.text)
        if node.tag == "{http://www.tei-c.org/ns/1.0}w":
            if "lemma" in node.attrib:
                node.attrib["lemma"] = replace_text(node.attrib["lemma"])
                if node.attrib["lemma"] == "$ ":
                    "Delete nodes with"
                    
                    # # deleted_ids.append(node.attrib['{http://www.w3.org/XML/1998/namespace}id'])
                    # deleted_id = node.attrib['{http://www.w3.org/XML/1998/namespace}id']
                    parent = node.getparent()
                    grandparent = parent.getparent()
                    grandparent.remove(parent)
                    
                    # links = grandparent.findall("{http://www.tei-c.org/ns/1.0}linkGrp/{http://www.tei-c.org/ns/1.0}link")
                    
                    # for link in links:
                    #     if deleted_id in link.attrib["target"]:
                    #         print(deleted_id)
                    #         link.getparent().remove(link)
                            
                            


def main():
    #file_paths = "/home/larsm/my_projects/ParlaMint/Data/ParlaMint-NO/*.xml"
    file_paths = "*"


    parser = et.XMLParser(remove_blank_text=True)
    
    for doc in tqdm(glob(file_paths)):
        xml = et.parse(doc, parser)
        clean_text(xml)
        xml.write(doc, pretty_print=True, encoding='utf-8')

if __name__ == "__main__":
    main()