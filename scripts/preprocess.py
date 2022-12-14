import sys
from stortingsdata.preprocess.change_root import change_root
from stortingsdata.preprocess.doc_id import doc_id
from stortingsdata.preprocess.clean_text import clean_text

if __name__ == '__main__':
    
    f = '../new_output'
    f = sys.argv[1]
    
    arg = sys.argv[2]
    if arg == 'False':
        arg = False
    
    
    # Clean root element
    print("Cleaning root")
    change_root(f, arg)
    
    # Rename doc with id
    print("Clean root")
    doc_id(f)
    
    # Remove undesired symbols
    print("Cleaning text")
    clean_text(f)
    
    