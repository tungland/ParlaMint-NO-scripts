import lxml.etree as et
from glob import glob
from tqdm import tqdm
import re
from tqdm.contrib.concurrent import process_map

tei = 'http://www.tei-c.org/ns/1.0'
ns = {'tei' : tei}

# periods = {
#     '1997' : '1997-01',
#     '1998' : '1997-01',
#     '1999' : '1997-01',
#     '2000' : '1997-01',
#     '2001' : '2001-05',
#     '2002' : '2001-05',
#     '2003' : '2001-05',
#     '2004' : '2001-05',
#     '2005' : '2005-09',
#     '2006' : '2005-09',
#     '2007' : '2005-09',
#     '2008' : '2005-09',
#     '2009' : '2005-09',
#     '2010' : '2009-14',
#     '2011' : '2009-14',
#     '2012' : '2009-14',
#     '2013' : '2013-17',
#     '2014' : '2013-17',
#     '2015' : '2013-17',
#     '2016' : '2013-17',
#     '2017' : '2013-17',
#     '2018' : '2017-21',
#     '2019' : '2017-21',
#     '2020' : '2017-21',
#     '2021' : '2017-21',
#     '2022' : '2021-25',
    
# }

periods = {
    '1997': '1997-2001',
    '1998': '1997-2001',
    '1999': '1997-2001',
    '2000': '1997-2001',
    '2001': '2001-2005',
    '2002': '2001-2005',
    '2003': '2001-2005',
    '2004': '2001-2005',
    '2005': '2005-2009',
    '2006': '2005-2009',
    '2007': '2005-2009',
    '2008': '2005-2009',
    '2009': '2005-2009',
    '2010': '2009-2014',
    '2011': '2009-2014',
    '2012': '2009-2014',
    '2013': '2013-2017',
    '2014': '2013-2017',
    '2015': '2013-2017',
    '2016': '2013-2017',
    '2017': '2013-2017',
    '2018': '2017-2021',
    '2019': '2017-2021',
    '2020': '2017-2021',
    '2021': '2017-2021',
    '2022': '2021-2025'
    }




def determine_year(year, month):
    "Determine the parliamentary year based on year and month"
    year = int(year)
    month = int(month)   
    
    if month > 8:
        year1 = year
        year2 = year + 1
    elif month <= 8:
        year1 = year -1
        year2 = year
        
    return str(year1), str(year2)    

def extract_name(xml):
   
    t = xml.xpath("/tei:TEI/tei:teiHeader/tei:date", namespaces=ns)
    
    name = t[0].text

    #p = r"ParlaMint-NO_([0-9]{4})-([0-9]{2})_([0-9]{6})_?(lower|upper)?_?"
    p = r"ParlaMint-NO_([0-9]{4}-[0-9]{2}-[0-9]{2})-?(lower|upper)?(?:_[0-9])?"
    
    m = re.match(p, name)
    if not m:
        raise ValueError


    #year1 = m.group(1)
    #year2 = m.group(2)
    date = m.group(1)
    year = date.split('-')[0]
    month = date.split('-')[1] 
    year1, year2 = determine_year(year, month)       
    
    house = ''
    if len(m.groups()) > 2:
        house = m.group(2)
    
    return year1, year2, date, house
    
def set_house(house=None, lang=None):
    if house == 'lower':
        if lang == 'eng':
            return 'Lower House'
        elif lang == 'no':
            return 'Odelstinget'
    elif house == 'upper':
        if lang == 'eng':
            return 'Upper House'
        elif lang == 'no':
            return 'Lagtinget'
    else:
        if lang=='eng':
            return 'the Norwegian Parliament'
        elif lang=='no':
            return 'Stortinget'

def expand_year(year_str):
    "Expand year from 2d to 4d"
    
    year = int(year_str)
    
    if year > 90:
        return '19' + year_str
    else:
        return '20' + year_str 

    
def rewrite_doc(doc):
    xml = et.parse(doc)
    year1, year2, date, house = extract_name(xml)

    period = periods[year1]

    # Change date
    d = xml.xpath("/tei:TEI/tei:teiHeader/tei:date", namespaces=ns)[0]
    d2 = xml.xpath("/tei:TEI/tei:teiHeader/tei:profileDesc/tei:settingDesc/tei:setting/tei:date", namespaces=ns)[0]
    #date = '-'.join([expand_year(date[:2]), date[2:4], date[4:]])
    
    
    # d.text = date
    d2.text = date
    d2.set('when', date)

    # delete 'date'
    d.getparent().remove(d)
    
    
    # Change title
    titles = xml.xpath("/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title", namespaces=ns)

    titles[0].text = f"Norsk parlamentarisk korpus ParlaMint-NO, {date} [ParlaMint SAMPLE]"
    titles[1].text = f"Norwegian parliamentary corpus ParlaMint-NO, {date} [ParlaMint SAMPLE]"
    titles[2].text = f"Referat fra møte i {set_house(house, lang='no')}, periode {period}, sesjon {year1}-{year2}"
    titles[3].text = f"Hansard from meeting in {set_house(house, lang='eng')}, Session {period}, Sitting {year1}-{year2}"
    
    
    # session and house
    meeting = xml.xpath("/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:meeting", namespaces=ns)[0]
    meeting.text = f"{year1}-{year2}"

    if int(year1) < 2009:
        if house == 'lower':
            meeting.set('ana', f"#parla.lower #parla.session")
        elif house == 'upper':
            meeting.set('ana', f"#parla.upper #parla.session")
        else:
            meeting.set('ana', f"#parla.joint #parla.session")

    xml.write(doc)

def set_date_title(path):

    docs = glob(path + '/*.xml')
    process_map(rewrite_doc, docs, chunksize=1, max_workers=36)


if __name__ == "__main__":
    set_date_title("/home/larsm/my_projects/stortingsdata/output")
    #set_date_title("/home/larsm/my_projects/stortingsdata/test")
    
