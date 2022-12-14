"""Rename parliment hansards to ParliaMint

The name format is as follows:

ParlaMint-NO_YYYY-MM-DD.xml

ParlaMint-NO_YYYY-MM-DD-odelsting.xml

ParlaMint-NO_YYYY-MM-DD-1.xml

"""

import glob
import os
import sys
from re import compile, match, search, Pattern

def date_to_period(date:str) -> str:
    """Create parlament period from date. The parliamentary year runs from October to September.

    :param date: date yymmdd
    :type date: str
    :raises ValueError: wrong input
    :raises ValueError: wrong input
    :return: Parlamentary period yyyy-yy
    :rtype: str
    """
    p = r"(\d{2})(\d{2})(\d{2})$"
    m = match(p, date)
    if not m:
        raise ValueError
    year = m.group(1)
    month = m.group(2)
    year_int = int(year)
    month_int = int(month)
    
    if month_int > 12:
        raise ValueError    
    elif month_int >= 10:
        if year_int == 99:
            year_1 = '99'
            year_2 = '00'
        else:
            year_1 = year
            year_2 = "{:02d}".format(year_int + 1)
    else:
        if year_int == 0:
            year_1 = '99'
            year_2 = '00'
        else:
            year_1 = "{:02d}".format(year_int - 1)
            year_2 = year
    
    # Create year prefix (19 or 20)       
    if year_int > 90 or (year_int == 0 and month_int < 10):
        prefix = '19'
    else:
        prefix = '20'
        
    return "{}{}-{}".format(prefix, year_1, year_2)
    


def pre2016(m:Pattern) -> str:
    day = m.group(3)
    month = m.group(2)
    year = m.group(1)
    return year + month + day

def post2016(m:Pattern) -> str:
    year = (lambda m : m.group(3) if (int(m.group(4) )< 10) else m.group(2))(m)
    month = m.group(4)
    day = m.group(5)     
    return year + month + day

def lower_or_upper(filename:str) -> str:   
    if match(r'o', filename):
        return '-lower'
    elif match(r"l", filename):
        return '-upper'
    else:
        return ''

def get_date(filename):
    pdct = {
        'pre2016' : compile("^[slo](\d{2})(\d{2})(\d{2})k?\.xml$"),
        'post2016' : compile("^refs-(\d{2})(\d{2})(\d{2})-(\d{2})-(\d{2}).*\.xml$")
    }
    
    # look for matches
    m = dict()
    for key in pdct.keys():
        m[key] = match(pdct[key], filename)   
                
    if m['pre2016']:
        file_date = pre2016(m['pre2016'])
    elif m['post2016']:
        file_date = post2016(m['post2016'])
    else:
        raise ValueError('Wrong input: {}'.format(filename)) 
        #file_date = None
    
    date = [file_date[i:i+2] for i in range(0, len(file_date), 2)]
    date = '-'.join(date)
        
    return date

def date_two_to_four(year_str):
    "2 digit year to 4 digit"
    
    year = int(year_str)
    if year > 90:
        return '19'
    else:
        return '20'
    
 
def create_id(filename):
    # look for k    
    k = ''
    if search(r'k\.xml$', filename):
        k = '-2'
        
    date = get_date(filename)
    if date:
        #prefix = date_to_period(date)
        house = lower_or_upper(filename)
    
        return f"ParlaMint-NO_{date_two_to_four(date[:2])}{date}{house}{k}.xml"
            

def doc_id(dirname):
    # Parse folder
    paths = glob.glob(dirname + '/*')
    names = [x.split('/')[-1] for x in paths]
    
    # Create new names
    new_names ={}
    for name in names:
        new_name = create_id(name)
        if new_name:    
            new_names[name] = new_name
            
    #for key in new_names:
    #    print(key, new_names[key])
    
    # Rename files    
    for path in paths:
        name = path.split('/')[-1]
        if name in new_names.keys():        
            os.rename(path, f"{'/'.join(path.split('/')[:-1])}/{new_names[name]}")        


    
    
if __name__ == '__main__':
    doc_id(sys.argv[1])
