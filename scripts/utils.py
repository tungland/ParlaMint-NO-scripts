import lxml.etree as et
import functools
from glob import glob

def pprint(elem):
    print(
        et.tostring(
                elem
            ).decode()
        )

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

    
def apply_to_component_files(func):
    parser = et.XMLParser(remove_blank_text=True)
    
    for x in glob("*.xml"):
        if x.split(".")[0] != "ParlaMint-NO":
            xml = et.parse(x, parser)
            print(x)
            func(xml)
            
            xml.write(x, pretty_print=True, encoding='utf-8')
