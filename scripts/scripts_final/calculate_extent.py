import lxml.etree as et
from glob import glob
import pandas as pd
from dhlab import nbtokenizer
from tqdm.contrib.concurrent import process_map
from tqdm import tqdm

tei = 'http://www.tei-c.org/ns/1.0'
ns = {'tei' : tei}

class tag_counter:
    def __init__(self, files, headers) -> None:
        self.files = files
        self.headers = headers
        
        
        # strip whitespace to make lxml prettyprint function correctly
        #self.parser = et.XMLParser(remove_blank_text=True)

    def count_speeches(self, xml):
        return xml.xpath("count(//tei:u)", namespaces=ns) 

    def count_words_text(self, xml):
        utts = xml.xpath("//tei:u", namespaces=ns)
        
        
        doc_word_count = 0
        for u in utts:
            u_text = ' '.join(u.itertext())
            word_count = nbtokenizer.Tokens(u_text).size
            doc_word_count += word_count
            
        return doc_word_count
        
        
    def count_words_ana(self, xml):
        return xml.xpath("count(//tei:w)", namespaces=ns) 
        #count_name = xml.xpath("count(//tei:s/tei:name/tei:w)", namespaces=ns) 
        #count2 = xml.xpath("count(//tei:s/tei:w)", namespaces=ns) 

    def process_doc(self, doc):
        parser = et.XMLParser(remove_blank_text=True)
        
        xml = et.parse(doc, parser)
        
        s = self.count_speeches(xml)    
        s = str(int(s))   
        
        if 'ana' in doc.split('.'):
            #print(doc)
            w_count= self.count_words_ana(xml)            
        else:
            #print(doc)
            w_count = self.count_words_text(xml)
            
        w_count = str(int(w_count))

        measure1 = xml.xpath("//tei:extent/tei:measure", namespaces=ns)[0]
        extent = measure1.getparent()
        
        for child in extent.getchildren():
            extent.remove(child)
        
        for lang in [('en', 'speeches'), ('nob', "taler")]:
            measure2 = et.Element("measure")
            measure2.set('quantity', s)
            measure2.set("unit", 'speeches')
            measure2.set("{http://www.w3.org/XML/1998/namespace}lang", lang[0])
            measure2.text = "{} {}".format(s, lang[1])  
            extent.append(measure2)
        
        for lang in [('en', 'words'), ('nob', "ord")]:
            measure2 = et.Element("measure")
            measure2.set('quantity', w_count)
            measure2.set("unit", "words")
            measure2.set("{http://www.w3.org/XML/1998/namespace}lang", lang[0])
            measure2.text = "{} {}".format(w_count, lang[1])           
            extent.append(measure2)
        
        xml.write(doc, pretty_print=True, encoding='utf-8')
        
        return int(s), int(w_count)
     
    def add_tot(self, s, w_count):
        parser = et.XMLParser(remove_blank_text=True)
        
        s = str(int(s))
        w_count = str(int(w_count))        
        
        for header in self.headers:
            xml = et.parse(header, parser)
            measure1 = xml.xpath("//tei:extent/tei:measure", namespaces=ns)[0]
            extent = measure1.getparent()
            
            for child in extent.getchildren():
                extent.remove(child)
            
            for lang in [('en', 'speeches'), ('nob', "taler")]:
                measure2 = et.Element("measure")
                measure2.set('quantity', s)
                measure2.set("unit", 'speeches')
                measure2.set("{http://www.w3.org/XML/1998/namespace}lang", lang[0])
                measure2.text = "{} taler".format(s)  
                extent.append(measure2)
            
            for lang in [('en', 'words'), ('nob', "ord")]:
                measure2 = et.Element("measure")
                measure2.set('quantity', w_count)
                measure2.set("unit", "words")
                measure2.set("{http://www.w3.org/XML/1998/namespace}lang", lang[0])
                measure2.text = "{} {}".format(w_count, lang[1])           
                extent.append(measure2) 
                
            xml.write(header, pretty_print=True, encoding='utf-8')

    def process_doc_wrapper(self, doc):
        s, w = self.process_doc(doc)
        self.s_tot += s
        self.w_tot += w    
            
    def run(self):
        self.s_tot = 0
        self.w_tot = 0        
        # for doc in tqdm(self.files):
        #     s, w = self.process_doc(doc)
        #     s_tot += s
        #     w_tot += w
        process_map(self.process_doc, self.files, chunksize=1)
            
        self.add_tot(self.s_tot, self.w_tot)

def main():
    files = glob('*.xml')
    
    headers = list()
    for file in files:
        if file.split(".")[0] == "ParlaMint-NO":
            files.remove(file)
            headers.append(file)
            print(file)
    
    c = tag_counter(files, headers)
    
    c.run()    
    
if __name__ == "__main__":
    # Wait with this one
    
    main()
