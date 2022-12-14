import requests, pandas as pd
from bs4 import BeautifulSoup as bs
import pandas_read_xml as pdx

from sqlalchemy import create_engine
engine = create_engine('postgresql://larsm:admin@localhost:5432/parlamint')

def fetch_presidentskap(session):
    base_url = "https://data.stortinget.no/eksport/presidentskapet?stortingsperiodeid={}"
    r = requests.get(base_url.format(session))
    soup = bs(r.content, "xml")
    #print(soup)
    df = pdx.fully_flatten(pdx.read_xml(str(soup), ["presidentskapet_oversikt", "medlem_liste"]))
    df.columns = [x.split("|")[-1] for x in df.columns]
    df["periode"] = session
    return df

def per_gen():
    date1 = 1997
    date2 = 2001
    while date1 < 2022: 
        string = f"{date1}-{date2}"
        date1 += 4
        date2 += 4
        yield string

def loop():
    lst = list()    
    for x in per_gen():
        lst += [fetch_presidentskap(x)]
    return pd.concat(lst).reset_index(drop=True)

def main():
    df = loop()
    df.to_sql("presidentskap", engine, if_exists="replace")
    
if __name__=="__main__":
    main()