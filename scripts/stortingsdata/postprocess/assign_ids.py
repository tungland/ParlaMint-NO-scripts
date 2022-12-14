import pandas as pd
import glob
from lxml import etree
from sqlalchemy import create_engine
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

def get_id_dict(conn):
    df = pd.read_sql('name_id_pairs', con=conn)
    df.set_index('name', inplace=True)   
    return df['id'].to_dict()

def process_doc(path, dct):
    tree = etree.parse(path)
    namespaces = {'tei' : "http://www.tei-c.org/ns/1.0"}
    
    us = tree.xpath("//tei:u", namespaces=namespaces)
    for u in us:
              
        name = u.xpath("@name", namespaces=namespaces)

        who = None
        
        if u.xpath("who"):
            who = u.xpath("@who")

        if name[0] in dct and (who == [""] or who == ["person."] or not who):
         
            u.attrib["who"] = "#person." + dct[name[0]]       
        
        elif name[0] not in dct:
         
            with open("not in dct.txt", "a") as f:
                f.write(f"{path}, {name[0]}\n")
                
        else:        
            with open("else.txt", "a") as f:
                f.write(f"{path}, {name[0]}\n")
        
    return tree       
   
 
def assign_ids(folder):    
    
    engine = create_engine('postgresql://larsm:admin@localhost:5432/parlamint')

    id_dict = get_id_dict(engine)
    
    for file in tqdm(glob.glob(f"{folder}/*.xml")):
        name = file.split("/")[-1]
        
        try:
            xml = process_doc(file, id_dict)
            xml.write(file)
            
        except Exception as e:
            print(name)
            print(e)  
            
 