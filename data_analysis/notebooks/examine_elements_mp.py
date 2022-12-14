import os, sys
from bs4 import BeautifulSoup as bs
import multiprocessing as mp


    
def file_loop(root):
    for root, _, file_lst in os.walk(root):
        for file in file_lst:
            yield file, os.path.join(root, file)

def dir_loop(root):
    for root, dir, _ in os.walk(root):
        if len(dir) > 0:
            for name in dir:
                yield name, os.path.join(root, name)
        
def parse_xml(c_name, destination, xml_collection, *tags):
    print(xml_collection)
    for name, doc in file_loop(xml_collection):
        print(doc)
        with open(doc) as f:
            soup = bs(f, "lxml-xml")
        for desc in soup.descendants:
            
            if desc.name in tags:
                with open(f"{destination}/{c_name}-{desc.name}.csv", "a") as f:
                    f.write(str(desc))
                    f.write("\n")
 
def main(input): 
    
    destination = input[0]
    
    if not os.path.exists(destination): 
        os.mkdir(destination)
    else:
        print("Dir exists")

    pool = mp.Pool()
            
    for name, path in dir_loop("data"):
        print(name)
        #for w in :
        #pool.apply_async(parse_xml, args=(name, w[0], destination, w[1], "merknad"))
        pool.apply_async(parse_xml, args=(name, destination, path, *input))
        print(path)

    pool.close()         
    pool.join()
     
 
                    
        
if __name__ == '__main__':
    main(sys.argv[1:])
    
    
    
    
   
