import pandas as pd
import lxml.etree as et

from tqdm import tqdm

from glob import glob
from sqlalchemy import create_engine
from tqdm.contrib.concurrent import process_map

def parse_doc(file):
    tree = et.parse(file)
    engine = create_engine('postgresql://larsm:admin@localhost:5432/parlamint')
    us = tree.xpath("//tei:u", namespaces={"tei":"http://www.tei-c.org/ns/1.0"})
    lst = list()
    for u in us:
       lst += [(u.attrib["{http://www.w3.org/XML/1998/namespace}id"], u.attrib['name'], u.attrib["who"])]

    df = (pd.DataFrame(lst, columns=['seg', 'name', 'id']))
    df.to_sql('from_corpus', engine, if_exists='append', index=None)
    engine.dispose()

def main():
    files = glob("output/*")
    
    #process_map(parse_doc, files, chunksize=1, max_workers=36)
    process_map(parse_doc, files, chunksize=1, max_workers=4)
    
if __name__ == "__main__":
    main()
   