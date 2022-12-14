"""
Every component file contains one sitting day, so it should also contain a corresponding meeting element. Furthermore there should be also specified term and session and probably title should be fixed too, because it is saying something different from meeting element:

https://github.com/tungland/ParlaMint/blob/1c385b6acce7a1459878c377a79dec4672af6d7d/Data/ParlaMint-NO/ParlaMint-NO_1999-03-02-lower.xml#L11-L13

<title type="sub" xml:lang="nob">Referat fra møte i Stortinget, periode 1997-2001, sesjon 1998-1999</title>
<title type="sub" xml:lang="en">Hansard from meeting in the Norwegian Parliament, Session 1997-2001, Sitting 1998-1999</title>
<meeting ana="#parla.lower #parla.session #ST.1998-1999" corresp="#OT">Session 1998-1999</meeting>

Can be encoded this way (if it makes sense in the Norwegian domain):

<title type="sub" xml:lang="nob">Referat fra møte i Stortinget, <!--Term--> 1997-2001, sesjon 1998-1999, <!--Sitting day 1999-03-02--></title>
<title type="sub" xml:lang="en">Hansard from meeting in the Norwegian Parliament, Term 1997-2001, Session 1998-1999, Sitting day 1999-03-02</title>
<meeting ana="#parla.lower #parla.term" corresp="#OT" n="1997-2001">Term 1997-2001</meeting>
<meeting ana="#parla.lower #parla.session #ST.1998-1999" corresp="#OT" n="1998-1999">Session 1998-1999</meeting>
<meeting ana="#parla.lower #parla.sitting" corresp="#OT" n="1999-03-02">Sitting day 1999-03-02</meeting>
"""
import lxml.etree as et
import re
from glob import glob
from copy import deepcopy as copy

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



def get_date(xml):
    date_string = xml.find("teiHeader/profileDesc/settingDesc/setting/date", ns).get("when")
    assert re.match("\d{4}-\d{2}-\d{2}", date_string), "Wrong date format"    
    return date_string

def get_session(xml):
    res = xml.findall("//meeting", ns)
    val = ""
    chamber = ""
    corresp = ""
    
    for r in res:
        tmp = r.get("ana").split()
        if tmp[1] == "#parla.session":
            val = tmp[2].split(".")[1]
            chamber = tmp[0]
            corresp = r.get("corresp")
    
    assert val != "", "No session"
    assert re.match(r"\d{4}-\d{4}", val), "Wrong format"
    
    val = copy(val)
    chamber = copy(chamber)
    corresp = copy(corresp)
    
    return val, chamber, corresp

def session_to_term(session):
    y1, y2 = [int(x) for x in session.split("-")]
    assert y1 in range(1997,2022), "Wrong period"
    print(y1)
    
    if y1 in range(1997, 2001):
        return "1997-2001"
    elif y1 in range(2001, 2005):
        return "2001-2005"
    elif y1 in range(2005, 2009):
        return "2005-2009"
    elif y1 in range(2009, 2013):
        return "2009-2013"
    elif y1 in range(2013, 2017):
        return "2013-2017"
    elif y1 in range(2017, 2021):
        return "2017-2021"
    elif y1 in range(2021, 2025):
        return "2021-2025"
    else:
        raise ValueError("Wrong session")

def edit_title(xml, term, session, date):
    titles = xml.findall("//title", ns)
    subtitles = [x for x in titles if x.get("type") == "sub"]
    
    template_nob_sub = f"Referat fra møte i Stortinget, Stortingsperiode {term}, sesjon {session}, møtedag {date}"
    template_en_sub = f"Hansard from meeting in the Norwegian Parliament, term {term}, Session {session}, Sitting day {date}"
    
    for title in subtitles:
        if title.get(xmllang) == "nob":
            title.text = template_nob_sub
        elif title.get(xmllang) == "en":
            title.text = template_en_sub
        else:
            raise ValueError(f"Wrong xmllang at {date}")
        
def edit_meetings(xml, term, session, date, chamber, corresp):
    title_stmt = xml.find("//titleStmt", ns)
    
    #Delete old meetings
    for elem in title_stmt:
        if elem.tag ==  "{http://www.tei-c.org/ns/1.0}meeting":
            title_stmt.remove(elem)
    
    for x, x_str in zip([term, session, date], ["term", "session", "sitting"]):
        meeting = et.Element("{http://www.tei-c.org/ns/1.0}meeting")
        if x_str == "sitting":
            meeting.set("ana", f"{chamber} #parla.{x_str}")
            meeting.text = f"{x_str.title()} day {x}"
        else:
            meeting.set("ana", f"{chamber} #parla.{x_str} #ST.{x}")
            meeting.text = f"{x_str.title()} {x}"
            
            
        meeting.set("corresp", corresp)
        #print(x)
        meeting.set("n", x)
        
        title_stmt.insert(4, meeting)
        
def parse_xml(xml):
    date = get_date(xml)
    session, chamber, corresp = get_session(xml)
    term = session_to_term(session)
    
    edit_title(xml, term, session, date)
    edit_meetings(xml, term, session, date, chamber, corresp)


def main():
    parser = et.XMLParser(remove_blank_text=True)
    
    for x in glob("*.xml"):
        if x.split(".")[0] != "ParlaMint-NO":
            xml = et.parse(x, parser)
            print(x)
            parse_xml(xml)
            
            xml.write(x, pretty_print=True, encoding='utf-8')
        
if __name__ == "__main__":
    main()
    
    
    
    
    
        
