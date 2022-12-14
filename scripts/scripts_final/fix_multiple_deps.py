import lxml.etree as et
from glob import glob

ns = {"tei" : "http://www.tei-c.org/ns/1.0"}
parser = et.XMLParser(remove_blank_text=True)

def rewrite_tag(link1, *links):
    "Make link2 a dependant of link 1"
    root = link1.attrib["target"].split()[1]
    
    for link in links:
        link.attrib["ana"] = "ud-syn:parataxis"
        self_ = link.attrib["target"].split()[1]
        link.attrib["target"] = " ".join([root, self_]) 
        
def find_links(xml, doc):
    tot = 0

    if len(xml.findall("//{http://www.tei-c.org/ns/1.0}linkGrp")) != 0:
        for linkGrp in xml.findall("//{http://www.tei-c.org/ns/1.0}linkGrp"):
            links = linkGrp.findall("{http://www.tei-c.org/ns/1.0}link")
            
            count = 0
            links_to_change = list()
            
            for link in links:
                if link.attrib["ana"] == "ud-syn:root":
                    count += 1
                    links_to_change.append(link)
                    
            rewrite_tag(links_to_change[0], *links_to_change[1:])
                        
            if count > 1:
                tot += 1
            
            
            
        print(tot / len(xml.findall("//{http://www.tei-c.org/ns/1.0}linkGrp")))
        xml.write(doc, pretty_print=True, encoding='utf-8')        
    

def main():
    paths = "/home/larsm/my_projects/ParlaMint/Data/ParlaMint-NO/*.xml"
    
    for doc in glob(paths):
        if "ana" in doc.split("."):
            xml = et.parse(doc, parser)
            find_links(xml, doc)
            
if __name__ == "__main__":
    main()
            
            
            