"Count all words and utterances and append to corpus header"

from glob import glob
import lxml.etree as et
from tqdm import tqdm
from os.path import basename, splitext
from tqdm.contrib.concurrent import process_map
import pandas as pd

ns = {"tei" : "http://www.tei-c.org/ns/1.0"}
parser = et.XMLParser(remove_blank_text=True)


def parse_file(file):
    xml = et.parse(file)
    
    measure_s = xml.xpath("/tei:TEI/tei:teiHeader/tei:fileDesc/tei:extent/tei:measure[1]", namespaces=ns)[0]
    
    measure_w = xml.xpath("/tei:TEI/tei:teiHeader/tei:fileDesc/tei:extent/tei:measure[3]", namespaces=ns)[0]
    
    s = int(measure_s.attrib["quantity"])
    w = int(measure_w.attrib["quantity"])
    
    with open("s_w.txt", "a") as f:
        f.write(f"{file}, {s}, {w}\n")
     
    #return s, w

def main():
    files = glob("*.xml")
    names = [(
        splitext(
            splitext(
                basename(
                    x
                )
            )[0]
        )[0], x) for x in files
    ]
    
    header = list()
    body = list()
    
    for name in names:
        if name[0] == "ParlaMint-NO":
          header.append(name[1])
        else:
            body.append(name[1]) 
    
    # s_tot = 0
    # w_tot = 0    
    # for file in tqdm(body):
    #     s, w = parse_file(file)
    #     s_tot += s
    #     w_tot += w
    process_map(parse_file, body, chunksize=1)
    
    df = pd.read_csv("s_w.txt")
    
    
    s_tot = df.iloc[:, 1].sum()
    w_tot = df.iloc[:, 2].sum()
    
        
    for file in tqdm(header):
        print(file)
        
        xml = et.parse(file, parser)
        
        s1 = xml.xpath("/tei:teiCorpus/tei:teiHeader/tei:fileDesc/tei:extent/tei:measure[1]", namespaces=ns)[0]
        #print(s1)
        s2 = xml.xpath("/tei:teiCorpus/tei:teiHeader/tei:fileDesc/tei:extent/tei:measure[2]", namespaces=ns)[0]
        
        w1 = xml.xpath("/tei:teiCorpus/tei:teiHeader/tei:fileDesc/tei:extent/tei:measure[3]", namespaces=ns)[0]
        w2 = xml.xpath("/tei:teiCorpus/tei:teiHeader/tei:fileDesc/tei:extent/tei:measure[4]", namespaces=ns)[0]
        
        s1.attrib["quantity"] = str(s_tot)
        s1.text = f"{s_tot} speeches"
        
        s2.attrib["quantity"] = str(s_tot)
        s2.text = f"{s_tot} taler"
        
        w1.attrib["quantity"] = str(w_tot)
        w1.text = f"{w_tot} words"
        
        w2.attrib["quantity"] = str(w_tot)
        w2.text = f"{w_tot} ord"
        
        xml.write(file, pretty_print=True, encoding='utf-8')
        
          
    
    
if __name__ == "__main__":
    main()
    
    