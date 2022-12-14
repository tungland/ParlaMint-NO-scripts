"""Merge memberships

Merge overlapping membership affilliations in persons. 

For now we do:
    * members of govt
But can later expand to:
    * members of parliament
    * replacements
    
    other? type head of government
"""

import lxml.etree as et
from glob import glob
from datetime import datetime
from datetimerange import DateTimeRange

# Define namespaces
ns = {"tei" : "http://www.tei-c.org/ns/1.0"}

# Define namespaces
ns = {"tei" : "http://www.tei-c.org/ns/1.0"}

class Membership:
    """Class representing a membership
    
    OBS: for reasons, a current membership is set as ending in the year 3000."""
    
    cutoff = datetime.strptime("2900-01-01", "%Y-%m-%d")
    
    def __init__(self, from_date, to_date = None):
        if isinstance(from_date, datetime):
            self.from_date = from_date
        else:
            self.from_date = datetime.strptime(from_date, "%Y-%m-%d")
        
        
        if to_date:
            if isinstance(to_date, datetime):
                self.to_date = to_date
            else:
                self.to_date = datetime.strptime(to_date, "%Y-%m-%d")
        else:
            self.to_date = datetime.strptime("3000-01-01", "%Y-%m-%d")
            
        # self.date_range = DateTimeRange(str(self.from_date).replace(" ", "T"), str(self.to_date).replace(" ", "T"))
        self.date_range = DateTimeRange(self.from_date, self.to_date)        
                
    def __str__(self):
        if self.to_date < self.cutoff:
            return f"""Membership from {datetime.strftime(self.from_date, "%Y-%m-%d")} to {datetime.strftime(self.to_date, "%Y-%m-%d")}"""
        else:
            return f"""Membership from {datetime.strftime(self.from_date, "%Y-%m-%d")}"""
        
        
    def to_xml(self):
        """Write to XML
        
        Element can be customized here"""
                
        el = et.Element("affiliation")
        from_date = datetime.strftime(self.from_date, "%Y-%m-%d")
        el.set("from", from_date)
        
        if self.to_date < self.cutoff:
            to_date = datetime.strftime(self.to_date, "%Y-%m-%d")
            el.set("to", to_date)

        el.set("role", "member")
        el.set("ref", "#government.NO")
        
        return el        
    
class Person:
    """Class representing a person entry"""
    def __init__(self, element : et.Element, memberships_raw : list[et.Element]) -> None:
        """
        :param element: ParlaMint person xml
        :type element: et.Element
        :param memberships_raw: List of memberships to merge
        :type memberships_raw: list[et.Element]
        """        
        
        self.affiliations = memberships_raw
        self.element = element
        self.id = element.attrib['{http://www.w3.org/XML/1998/namespace}id']
        
        # Parse affiliation xml
        lst = list()    
        for x in memberships_raw:
            from_ = x.attrib["from"]
            if "to" in x.attrib:
                to_ = x.attrib["to"]
            else:
                to_ = None            
            lst.append(Membership(from_, to_)) 
        
    
        # Simplify memberships
        memberships_ranges = [DateTimeRange(x.from_date, x.to_date) for x in lst]
        new_memberships_ranges = self.simplify_ranges(memberships_ranges)        
        
        # Add new memberships
        self.memberships = list()
        for range in new_memberships_ranges:
            new = Membership(range.start_datetime, range.end_datetime)
            self.memberships.append(new)
            
        # Edit element
        self.remove_affiliations()
        self.add_new_affiliations()        
                
    def __str__(self):
        return f"Person with ID {self.id} and {len(self.memberships)} memberships" 
    
    def remove_affiliations(self):
        for affilliation in self.affiliations:
            self.element.remove(affilliation)
            
    def add_new_affiliations(self):
        for membership in self.memberships:
            self.element.append(membership.to_xml())  
    
    @staticmethod
    def simplify_ranges(dtrs):
        if not dtrs:
            return []
        dtrs = sorted(dtrs, key=lambda dtr: dtr.start_datetime)
        simplified = []
        current = dtrs[0]
        for dtr in dtrs[1:]:
            if current.intersection(dtr).is_valid_timerange():
                current = current.encompass(dtr)
            else:
                simplified.append(current)
                current = dtr
        simplified.append(current)
        return simplified    

def parse_doc(doc):
    parser = et.XMLParser(remove_blank_text=True)

    xml = et.parse(doc, parser)
    persons = xml.xpath("//tei:person", namespaces=ns)

    person_list = list()
    overlapping_persons = list()

    for person in persons:
        memberships = person.xpath("./tei:affiliation[@role = 'member' and @ref='#government.NO']", namespaces=ns)
        if len(memberships) > 1:
            id = person.attrib['{http://www.w3.org/XML/1998/namespace}id']
            personobj = Person(person, memberships)
            person_list.append(personobj)
            
            overlapping_persons.append(person)
            
    xml.write(doc, pretty_print=True, encoding='utf-8')
            
def main():
    docs = ["/home/larsm/my_projects/ParlaMint/Data/ParlaMint-NO/ParlaMint-NO.xml",
            "/home/larsm/my_projects/ParlaMint/Data/ParlaMint-NO/ParlaMint-NO.ana.xml"]
    
    for doc in docs:
        parse_doc(doc)
    
if __name__ == "__main__":
    main()
    