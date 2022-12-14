"""Generate table of old and new filenames"""

from glob import iglob
import pandas as pd
from os.path import basename, splitext
from stortingsdata.preprocess.doc_id import create_id
import re

# Exclude hearings and european committee
p = re.compile(r"^(s|o|l|refs)")

def get_old_filenames():
    path = "/home/larsm/my_projects/stortingsdata/data"
    for x in  iglob(path + "/*/*"):
        x = basename(x)
        if re.match(p, x):                
            yield x

def main():
    records = list()    
    for file in get_old_filenames():  
        dct = dict()
        id = create_id(file)
        dct["id"] = splitext(id)[0]
        dct["source"] = splitext(file)[0]
        records.append(dct)
        
    pd.DataFrame(records).to_csv("source_ids_table.csv", index=None)
    
if __name__ == "__main__":
    main()