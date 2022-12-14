import glob, os
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import pandas as pd
import multiprocessing as mp

"""
Counts the elements from a xml collection. Outputs count of elements from each document

"""

def count_elements(xml_list, name):
    """Counts the elements in a list of XML files

    Args:
        xml_list (list): List of xml files to parse
        name (str): Destination path
    """
    dct = {}
    
    
    for doc in xml_list: 
        with open(doc) as f:
            soup = bs(f, "lxml-xml")   
        for desc in soup.descendants:
            if desc.name in dct.keys():
                dct[desc.name] += 1
            else:
                dct[desc.name] = 1
    
    df = pd.DataFrame.from_dict(dct, orient="index")
    df.to_csv("{}.csv".format(name))


def main_count_elements():
    """Multiprocess count_elements
    """
    base_path = "elements_data"
    os.mkdir(base_path)
    
    session_paths = glob.glob("data/*")
    sessions = [s.split("/")[1] for s in session_paths]
    
    path_dct = {}
    for s in session_paths:
        path_dct[s.split("/")[1]] = glob.glob(s + "/*")
    
    pool = mp.Pool()
    
    for s in sessions:
        pool.apply_async(count_elements, args = (path_dct[s], f"{base_path}/{s}"))
       
    pool.close()
    pool.join()    
        
if __name__ == '__main__':
    main_count_elements()