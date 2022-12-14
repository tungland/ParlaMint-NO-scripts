import os
import requests
import pandas as pd
import pandas_read_xml as pdx
import glob
import numpy as np
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from pandas_read_xml import fully_flatten, read_xml
from sqlalchemy import create_engine
from tqdm import tqdm


# Download mp info from data.storting


def parse_session_list(session_list_url):
    "Parses list of parliament sessions"
    r = requests.get(session_list_url)
    soup = bs(r.content, "lxml-xml")
    
    for session in soup.find_all('stortingsperiode'):
        yield session.find('id').text

def main():
    session_lst_url = "https://data.stortinget.no/eksport/stortingsperioder"
    session_lst = parse_session_list(session_lst_url)
    mp_url = "https://data.stortinget.no/eksport/representanter?stortingsperiodeid={}&vararepresentanter=true"
    
    engine = create_engine('postgresql://larsm:admin@localhost:5432/parlamint')
    
    #if not os.path.exists('mp_data_raw'):
    #        os.mkdir('mp_data_raw')

    count = 0   
    l = list()
    for x in tqdm(session_lst):
        #print(x)
        r = requests.get(mp_url.format(x))
        
       # with open("mp_data_raw/{}.xml".format(x), "w") as f:
        #    f.write(r.text)
        
        df = read_xml(r.text, ['representanter_oversikt', 'representanter_liste']).pipe(fully_flatten)
        df.columns = ['|'.join(x.split('|')[1:]) for x in df.columns]
        if 'doedsdato' not in df.columns:
            df['doedsdato'] = np.NAN
        df = df.loc[:, ['doedsdato', 'etternavn', 'foedselsdato', 'fornavn',
        'id', 'kjoenn', 'vara_representant', 
        'fylke|id', 'fylke|navn',
        'parti|id', 'parti|navn', 'parti|representert_parti']]
        
        df['periode'] = x
        l += [df]
        
        count += 1
        if count >= 7:
            break
    
    df = pd.concat(l).reset_index(drop=True)
    # # Merge mps with multiplpe terms
    # periods = df.groupby('id')['periode'].apply(list).reset_index(name='periode_liste').set_index('id')
    # df = df.drop_duplicates(subset='id').join(periods, on='id')
    # df.drop('periode', axis=1, inplace=True)
    
    #return df
    #df.to_sql("mps", engine, index=None)
    
    # Table 1: MPs personal info
    personal_info_table = df.drop(['vara_representant', 'parti|representert_parti', 'periode', 'parti|id', 'parti|navn', 'fylke|id', 'fylke|navn'], axis=1)
    personal_info_table.drop_duplicates().to_sql('mps', engine, if_exists='replace', index=False)
    
    
    # Table 2: period and substitute info
    period = df.loc[:, ['id', 'vara_representant', 'periode', 'parti|id', 'parti|navn', 'fylke|id', 'fylke|navn']]
    period.to_sql('mps_period', engine, if_exists='replace', index=False)

if __name__ == "__main__":
    main()