"""Clean Name and IDs from parlamint

Actions:
    * removes underscore and trailing numbers from some post 2016 pre-assigned IDs
    * adds '#person.'-prefix to post 2016 pre assigned IDs
    * removes 'name'-attribute from u-tags
"""

import lxml.etree as et
import re
from glob import glob
from tqdm.contrib.concurrent import process_map

def clean_name(doc):



    xml = et.parse(doc)

    # Pattern to remove extra underscore with numbers from some preassigned IDs
    p = r"([A-Za-zÆØÅæøå0-9]+)(?:_\d+)?"
    
    for u in xml.findall("//{http://www.tei-c.org/ns/1.0}u"):
        a = u.attrib['who']
        
        #if a != "":
        m = re.match(p, a)

        if m:

            # If matching pattern add prefix        
            u.attrib['who'] = '#person.' + m.group(1)        

        # Remove 'name' attribute
        u.attrib.pop('name', None)

    xml.write(doc)




def main(path='../output'):
    docs = glob(path + '/*')
    
    #for doc in docs:
    #    clean_name(doc)  
    process_map(clean_name, docs, chunksize=1)
    # process_map(clean_name, docs, chunksize=1, max_workers=36)
    
if __name__ == "__main__":
    main()