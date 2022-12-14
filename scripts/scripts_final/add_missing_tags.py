"""Add required missing tags to parlamint

tags to add:

<namespace name="http://www.tei-c.org/ns/1.0"/>
Child of tagsDecl

measure under extent

meeting

eng => en

"""
from glob import glob
import os
from xml.dom.expatbuilder import Namespaces
import lxml.etree as et
import pandas as pd
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

parser = et.XMLParser(remove_blank_text=True)

ns = {
    'tei' : 'http://www.tei-c.org/ns/1.0'
}

# import source ids
df = pd.read_csv("/home/larsm/my_projects/stortingsdata/scripts/source_ids_table.csv")
source_id_dct = df.set_index("id").loc[:, "source"].to_dict()


### Tags to add

# tagsDesl
namespace = et.Element('{http://www.tei-c.org/ns/1.0}namespace')
namespace.set("name", "http://www.tei-c.org/ns/1.0")
tagUsage = et.SubElement(namespace, '{http://www.tei-c.org/ns/1.0}tagUsage')
tagUsage.set('gi', 'seg')
tagUsage.set('occurs', '1')

#measure
measure = et.Element('{http://www.tei-c.org/ns/1.0}measure')
measure.set('quantity', '1')
measure.set('unit', 'speeches')

elements_to_add = {
    namespace,
    measure
}
# Appinfo
appInfo = et.Element("{http://www.tei-c.org/ns/1.0}appInfo")
application = et.SubElement(appInfo, "{http://www.tei-c.org/ns/1.0}application")
application.set("version", "3.4.1")
application.set("ident", "Spacy")
desc = et.SubElement(application, "{http://www.tei-c.org/ns/1.0}desc")
desc.set("{https://www.w3.org/XML/1998/namespace}lang", "en")
desc.text = "Linguistic processing performed with Spacy jointly trained for Norwegian Bokmål and Norwegian Nynorsk"

ana_only_els = {
    # parent : # child
    'encodingDesc' : appInfo
}

# Setting desc
setting_name = et.Element("name")
setting_name.set("type", "org")
setting_name.text = "Stortinget"

# source ids 


### Code

def add_to_ana_only(xml):
    "Add ana only tags"
    
    for key, val in ana_only_els.items():
        parent = xml.xpath("{http://www.tei-c.org/ns/1.0}" + key, namespaces=ns)[0]
        
        # remove unwanted children
         
def add_meeting(xml, name):    
    meeting = xml.xpath("//tei:meeting", namespaces=ns)[0]
    title = xml.xpath("//tei:titleStmt/tei:title", namespaces=ns)[3]
    sitting = title.text.split()[-1]
    
    if 'lower' in name.split('-'):
        meeting.set("corresp", "#OT")
        meeting.set("ana", "#parla.lower #parla.session #ST.{}".format(sitting))
        
        
    elif 'upper' in name.split('-'):
        meeting.set("corresp", "#LT")
        meeting.set("ana", "#parla.upper #parla.session #ST.{}".format(sitting))
        
    else:
        meeting.set("corresp", "#ST")
        meeting.set("ana", "#parla.uni #parla.session #ST.{}".format(sitting))

    meeting.text = "Session {}".format(sitting)

def edit_u_tag(xml):
    u_tags = xml.xpath("//tei:u", namespaces=ns)
    
    for u in u_tags:
        # eng to en
        if u.attrib["{http://www.w3.org/XML/1998/namespace}lang"] == "eng":
            u.attrib["{http://www.w3.org/XML/1998/namespace}lang"] = 'en'
            print("Eng to en")
            
        # delete empty 'who' attrib
        if "who" in u.attrib:
            if u.attrib["who"] == "":
                u.attrib.pop("who")

def add_setting_name(xml):
    "Add settingDesc org name 'Stortinget'"
    setting = xml.xpath("//tei:settingDesc/tei:setting", namespaces=ns)[0]

    for child in setting.getchildren():
        if 'type' in child.attrib:
            if child.attrib['type'] == "org":
                 setting.remove(child)
                 
    setting.insert(0, setting_name)
    
def edit_source(xml, name):
    """Edit source field
    
    1. Add source URL"""
    
    idno = xml.xpath("/tei:TEI/tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:idno", namespaces=ns)[0]
    id = source_id_dct[name]
    id_text = "https://data.stortinget.no/eksport/publikasjon?publikasjonid={}".format(id)   
    idno.text = id_text
    

    
def clean_date_field(xml):
    "Edit bibl/date"
    source_date = xml.xpath("//tei:settingDesc/tei:setting/tei:date", namespaces=ns)[0]
    date_string = source_date.attrib["when"]
    YY, mm, dd = date_string.split("-")
    date_string_processed = f"{dd}.{mm}.{YY[-2:]}"  
    
    target_date_element = xml.xpath("//tei:sourceDesc/tei:bibl/tei:date", namespaces=ns)[0] 
    
    target_date_element.attrib["when"] = date_string
    
    # edit source text
    source_date.text = date_string_processed   
    target_date_element.text = date_string_processed
    
def process_doc(file):
    """Doc loop"""
    
    name = os.path.basename(
        file
    ).split('.')[0]
    
    xml = et.parse(file, parser)
    
    # Add "namespace"
    tagsDecl = xml.xpath("//tei:tagsDecl", namespaces=ns)[0]
    #print(tagsDecl_replace.tag)
    
    for child in list(tagsDecl):
        tagsDecl.remove(child)    
    tagsDecl.append(namespace)  
    
    # Update extent
    extent = xml.xpath("//tei:extent", namespaces=ns)[0]
    
    for child in list(extent):
        extent.remove(child)    
    extent.append(measure)
    
    # if "ana" in file.split('.'):
    #     add_to_ana_only(xml)
    
    
    # Body only 
    if name != "ParlaMint-NO":
        add_meeting(xml, name)
        add_setting_name(xml)
        clean_date_field(xml)
        edit_source(xml, name)
        
    # u tags
    edit_u_tag(xml)
    
    xml.write(file, pretty_print=True, encoding='utf-8')

def main():
    #path = "/home/larsm/my_projects/ParlaMint/Data/ParlaMint-NO"    
    #os.chdir(path)
    files = glob("*.xml")
    
    print("Starting...")
    #for file in tqdm(files):
    #    process_doc(file)
    process_map(process_doc, files)
        
    print("Finished!")
        
if __name__ == "__main__":
    main()
        
        
    
    