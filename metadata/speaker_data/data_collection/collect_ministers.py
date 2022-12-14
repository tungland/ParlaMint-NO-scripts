import requests, pandas as pd
from sqlalchemy import create_engine

# TODO: add english label to ministers


def to_df(dct : dict) -> pd.DataFrame:
    """Wikidata query result json to dataframe

    :param dct: _description_
    :type dct: dict
    :return: _description_
    :rtype: pd.DataFrame
    """
    columns = dct['head']['vars']    
    lst = list()
    for t in dct['results']['bindings']:
        inner_lst = list()  
        for key in t.keys():  
            inner_lst += [t[key]['value']] 
        lst += [pd.DataFrame([inner_lst], columns=t.keys())]        
    return pd.concat(lst)


def qry(query : str) -> pd.DataFrame:
    """Query Wikidata

    :param query: WD query string
    :type query: str
    :return: Result
    :rtype: pd.DataFrame
    """
    url = 'https://query.wikidata.org/sparql' 
    r = requests.get(url, params = {'format': 'json', 'query': query})
    data = r.json()
    return to_df(data)
    
def query_gen() -> tuple:
    """
    Wikidata query generator 
    """
    dct = dict()
    dct["ministers"] = """
SELECT ?min ?minLabel ?person ?personLabel ?start ?end ?genderLabel ?født ?død ?partiLabel ?stid
WHERE 
{
  ?min wdt:P361 wd:Q1770849 .
       
       
  ?person wdt:P39 ?min .
  
    ?person p:P39 ?pos .
  ?pos ps:P39 ?min ;
       pq:P580 ?start.
      
  
  OPTIONAL {?pos pq:P582 ?end. }
  OPTIONAL {?person wdt:P21 ?gender . }
          OPTIONAL { ?person wdt:P569 ?født .}
  OPTIONAL { ?person wdt:P570 ?død .} 
    OPTIONAL {?person wdt:P3072 ?stid . }          
           
  
   FILTER (?start > "1997-05-23T10:20:13+05:30"^^xsd:dateTime)
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nb". }
}

ORDER BY ?start
"""
    dct["minister_parties"] = """
    SELECT DISTINCT ?stid ?person ?personLabel ?partiLabel  ?pstart ?pend 
WHERE
{
  ?min wdt:P361 wd:Q1770849 .
       
       
  ?person wdt:P39 ?min .
  
    ?person p:P39 ?pos .
  ?pos ps:P39 ?min ;
       pq:P580 ?start.
 
 
  ?person p:P102 ?p .
  ?p ps:P102 ?parti .
 OPTIONAL { ?p pq:P580 ?pstart . }
OPTIONAL {  ?p pq:P582 ?pend .}
  OPTIONAL {?person wdt:P3072 ?stid . }   
 
           
  
   FILTER (?start > "1997-05-23T10:20:13+05:30"^^xsd:dateTime)
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],nb". }
}

ORDER BY DESC(?pstart) """

    for key in dct.keys():
        yield key, dct[key]


def main():    
    engine = create_engine('postgresql://larsm:admin@localhost:5432/parlamint')
    
    for name, query in query_gen():
        df = qry(query)
        # lower all column names
        df.columns = [x.lower() for x in df.columns]
        df.to_sql(name, engine)
        
if __name__=="__main__":
    main()