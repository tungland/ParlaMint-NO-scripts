import pandas as pd
import lxml.etree as et
import re
import sqlalchemy as sql
from itertools import chain
from lxml.builder import E
from glob import glob
from sqlalchemy import create_engine


def assign_gender(string):
    if string == 'kvinne':
        return 'F'
    elif string == 'mann':
        return 'M'
    else:
        # If gender is not provided        
        return 'U'
    
def is_vara(string):
    if string == 'true':
        return 'replacement'
    elif string == 'false':
        return 'member'
    else:
        raise ValueError
            

def FROM(*args):
    "from is reserved in python"
    return {"from":' '.join(args)}
 
def TO(*args):
    "to is reserved in python"
    return {"to":' '.join(args)}

def split_sub(string):
    if string == 'SUBSTITUTEMP':
        return 'Substitute MP'
    else:
        return string

def mp_affiliations(id : str, engine : sql.engine) -> et.Element:
    """MP parliament period generator
    
    :param id: MP id
    :type id: string
    :yield: Affiliation
    :rtype: Iterator[et.Element]
    """

    id = id.lstrip('#')
    
    for x in pd.read_sql_query("SELECT * FROM mps_period WHERE id=%s", engine, params=[id]).iterrows():
        #print(x[1])
        
        MP_AFFILIATION = E.affiliation
        PARTY_AFFILIATION = E.affiliation
        
        SUB = is_vara(x[1].vara_representant)
        PERIOD = x[1].periode
        PARTYID = x[1]['parti|id']
        PARTY = x[1]['parti|navn']
        FYLKEID = x[1]['fylke|id']
        FYLKE = x[1]['fylke|navn']
        
        m = re.match(r"(\d{4})-(\d{4})", PERIOD)
        FROM_YEAR = m.group(1)
        TO_YEAR = m.group(2)           
        
        mp_affiliation = MP_AFFILIATION(
            #"{} from {} for {} county for the {} period".format(split_sub(SUB.upper()), PARTY, FYLKE, PERIOD),
            FROM('{}-10-01'.format(FROM_YEAR)),
            TO('{}-09-30'.format(TO_YEAR)),
            role=SUB,
            ref='#ST'            
        )   
        
        yield mp_affiliation

def party_affiliation_element(party_id : str, from_=None, to_=None) -> et.Element:
    PARTY_AFFILIATION = E.affiliation

    xml = PARTY_AFFILIATION(
        role='member',
        ref="#party.{}".format(party_id.upper())
    )
    
    if from_:
        xml.attrib['from'] = "{}-10-01".format(from_)
    if to_:
        xml.attrib['to'] = "{}-09-30".format(to_)       

        
    return xml

def get_period(df : pd.DataFrame, party : str) -> tuple:
    """Extract the earliest and latest year for a given affiliation. 
    Assumes that MPs only changes party between parliamentary periods
    """    
    res = df.loc[df['parti|id'] == party, 'periode']    
    lst = []
    for period in res:
        # get years from string and append to list
        m = re.match(r"(\d{4})-(\d{4})", period)
        lst += [int(x) for x in m.group(1, 2)]  
        
    return min(lst), max(lst)

def party_affiliation(id, engine):
    """Generate party affiliation element 
    """
    id = id.lstrip('#')

    df = pd.read_sql_query("""SELECT "parti|navn", "parti|id", periode FROM mps_period WHERE id=%s""", engine, params=[id])
    
    # Handle MPs that have represented more than one party
    if df['parti|id'].nunique() > 1:
        for party in df['parti|id'].unique():
                       
            from_, to_ = get_period(df, party)         
            
            yield party_affiliation_element(party, from_=from_, to_=to_)
        
        
    else:
        try :
            yield party_affiliation_element(df['parti|id'].unique()[0])
        except Exception as e:
            print(df['parti|id'])
            print(id)
            raise e
            
def generate_mp_record(record : pd.Series, engine: sql.engine) -> et.Element:
    """Make an XML record for a single MP

    :param record: SQL record of an MP
    :type record: pd.Series
    :param engine: SQLalchemy engine
    :type engine: sql.engine
    :return: XML of MP
    :rtype: et.Element
    """
    mp = E.person
    persName = E.persName
    forename = E.forename
    surname = E.surname
    sex = E.sex
    birth = E.birth
    
    mp_xml = mp( 
        persName(
            forename(record.loc['fornavn']),
            surname(record.loc['etternavn'])
        ),
        sex(value=assign_gender(record.loc['kjoenn'])),
        birth(
            #record.loc['foedselsdato'], 
            when=(record.loc['foedselsdato'].split('T'))[0]
            )
        #id=record.loc['id']
    )

    # Set id
    mp_xml.set('{http://www.w3.org/XML/1998/namespace}id', 'person.' + record.loc['id'])


    # Append mp period affiliation    
    # for x in mp_affiliations(mp_xml.attrib['{http://www.w3.org/XML/1998/namespace}id'], engine):
    for x in mp_affiliations(record.loc['id'], engine):
        mp_xml.append(x)
    
    # Append mp period
    # for x in party_affiliation(mp_xml.attrib['{http://www.w3.org/XML/1998/namespace}id'], engine):
    for x in party_affiliation(record.loc['id'], engine):
        mp_xml.append(x)
        
    return mp_xml

def main():
    engine = create_engine('postgresql://larsm:admin@localhost:5432/parlamint') 
    
    # Generate speaker xml
    df = pd.read_sql('mps', engine)
    
    xml = et.Element('listPerson')

    for x in df.iterrows():
        xml.append(generate_mp_record(x[1], engine))
        
    xml = et.ElementTree(xml)
    
    xml.write('MP_speakers.xml', pretty_print=True)
    
if __name__ == "__main__":
    main()
        
        
# TODO:
# Add død
# Add minister posts