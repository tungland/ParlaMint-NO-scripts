"""
     insert note inside paragraph

https://github.com/tungland/ParlaMint/blob/1c385b6acce7a1459878c377a79dec4672af6d7d/Data/ParlaMint-NO/ParlaMint-NO_1999-03-02-lower.xml#L118-L120

<seg xml:id="ParlaMint-NO_1999-03-02-lower.segd164e45">Statsråd Anne Enger Lahnstein la fram 2 kgl. proposisjonar</seg>
<note>(sjå under Referat)</note>
<seg xml:id="ParlaMint-NO_1999-03-02-lower.segd164e45s1">.</seg>

Source:

<a type="minnrykk">
<uth type="sperret">Statsråd Anne Enger Lahnstein</uth>
la fram 2 kgl. proposisjonar (sjå under Referat).
</a>

Expected encoding:

<seg xml:id="ParlaMint-NO_1999-03-02-lower.segd164e45">Statsråd Anne Enger Lahnstein la fram 2 kgl. proposisjonar<note type="comment">(sjå under Referat)</not
"""

import lxml.etree as et
from glob import glob

xi = "http://www.w3.org/2001/XInclude"
tei = "http://www.tei-c.org/ns/1.0"
xml_namespace = "http://www.w3.org/XML/1998/namespace"
xmllang = "{http://www.w3.org/XML/1998/namespace}lang"
xmlid = "{http://www.w3.org/XML/1998/namespace}id"

ns = {
    'xi' : xi,
    'tei' : tei,
    "" : tei
    }

def merge_note(note, ana=False):
    target_seg = note.getprevious()
    tail_seg = note.getnext()
    parent = note.getparent()

    #if not ana:
    
    # if tail seg
    if tail_seg is not None:
        note.tail = tail_seg.text
    target_seg.append(note)    
        
    # else:
    #     target_seg.append(note)
    #     for child in tail_seg:
    #         target_seg.append(child)
    
    if tail_seg is not None:    
        parent.remove(tail_seg)

 
def parse_doc(xml):
    target_notes = xml.findall("//u/note", ns)

    for note in target_notes:
           merge_note(note)     
        
def main():
    parser = et.XMLParser(remove_blank_text=True)
    
    for x in glob("*.xml"):
        if x.split(".")[0] != "ParlaMint-NO":
            xml = et.parse(x, parser)
            print(x)
            parse_doc(xml)
            
            xml.write(x, pretty_print=True, encoding='utf-8')
        
if __name__ == "__main__":
    main()
    
    



