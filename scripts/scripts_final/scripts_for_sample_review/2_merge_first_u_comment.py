"""
    merge note with speakernote

I believe that this kind of notes can be merged with speaker note:
https://github.com/tungland/ParlaMint/blob/1c385b6acce7a1459878c377a79dec4672af6d7d/Data/ParlaMint-NO/ParlaMint-NO_1999-03-02-lower.xml#L193-L198"""


"""
velg u/note
velg note type=speaker


if note.index == null
concat speaker_note + note

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

import functools

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug


def get_index(elem):
    return elem.getparent().index(elem)

@debug
def find_speaker_elem(elem):    
    target = elem.getparent().getprevious()
    if "speaker" in target.values():
        return target
    
def find_elems(xml):
    elems = xml.findall("//u/note", ns)
    
    # Filter elems    
    target_elems = [x for x in elems if get_index(x) == 0]

    # find speaker elems
    for elem in target_elems:
        speaker_note = find_speaker_elem(elem)
        if speaker_note is not None:
            speaker_note.text = " ".join([speaker_note.text, elem.text])
            elem.getparent().remove(elem)
            
            
def main():
    parser = et.XMLParser(remove_blank_text=True)
    
    for x in glob("*.xml"):
        if x.split(".")[0] != "ParlaMint-NO":
            xml = et.parse(x, parser)
            print(x)
            find_elems(xml)
            
            xml.write(x, pretty_print=True, encoding='utf-8')
        
if __name__ == "__main__":
    main()
    
