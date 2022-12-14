'''Remove empty and whitespace only tags from parlamint doc bodies'''
import lxml.etree as et
from glob import glob
from tqdm.contrib.concurrent import process_map


def recursively_empty(e):
   if e.text and not e.text.isspace():
       return False
   return all((recursively_empty(c) for c in e.iterchildren()))

def iterate_elem(doc):
    xml = et.parse(doc)

    
    try:
        tag = xml.xpath('/*/tei:text', namespaces={'tei' : 'http://www.tei-c.org/ns/1.0'})[0]
    except:
        raise ValueError("Failed on {}".format(doc))
    
    
    context = et.iterwalk(tag)
    
    for action, elem in context:
        parent = elem.getparent()
        if recursively_empty(elem):
            parent.remove(elem)
    
    #new_text = recursively_empty(tag)
    #print(xml.xpath('/*/tei:text', namespaces={'tei' : 'http://www.tei-c.org/ns/1.0'}))
    #print(context)
    
    try:
        xml.xpath('/*/tei:text', namespaces={'tei' : 'http://www.tei-c.org/ns/1.0'})[0] = context
    except:
        raise ValueError("Failed on {}".format(doc))
    
    xml.write(doc, pretty_print=True)
    
def main(path='../output'):
    docs = glob(path + '/*')
    
    process_map(iterate_elem, docs, chunksize=1, max_workers=4) # max_workers=36

if __name__ == "__main__":
    main()