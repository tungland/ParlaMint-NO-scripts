from pandas import read_sql_query, concat, DataFrame, read_sql, Series
from sqlalchemy import create_engine
import re
import pandas as pd

def presidentbytte(string):
    p = r"(.+) hadde her .*"
    m = re.match(p, string)
    if m:       
        return m.group(1)
    else:
        return string


def clean_text(s : Series) -> Series:
    s = s.apply(presidentbytte)
         
    s = (s.replace(r"[Ss]t?atsminister", '', regex=True)
        .replace(r"[Ss]tat?st?råd", '', regex=True)
        .replace(r"Utenriksminister", '', regex=True)
        .replace(r"Stortingspresident", '', regex=True)
        .replace(r"[Pp]resident(?:en)? ?") 
        .replace(r"(?:Første|Andre|Tredje|Fjerde|Femte) visepresident", '', regex=True)
        .replace(r"Stortingets (?:andre )?visepresident", '', regex=True)
        .replace(r"[Rr]epresentant(?:en)? ?")
        .replace(r"\(.+\)", '', regex=True)
        .replace(r"[\d\[\]\(\)«»]", '', regex=True)
        .replace(r"^e[rn] ", '', regex=True)
        .replace(r" [Sp]$", '', regex=True)
        .replace(r" [MS\.]$", '', regex=True)
        .replace(r"Votering", '', regex=True)
        .replace(r"-", "", regex=True)
        )
    return s
    
def clean_whitespace(s):
    s = (s.replace(r"\s+", " ", regex=True)
        .str.strip()
        .loc[s != ""]
    )
    return s
    
def match_names():
    engine = create_engine('postgresql://larsm:admin@localhost:5432/parlamint')  
    name_id = read_sql("name_id_pairs", engine, index_col='navn')
    names_raw = read_sql('all_speakers_raw', engine)
    
    names_raw['clean'] = (names_raw['name'].pipe(clean_text)
                      .pipe(clean_whitespace)
                      .str.lower()
                        )
    
    # Clean names for matching
    y = names_raw.reset_index()
    y['clean2'] = y.clean.str.replace(r"-", '', regex=True).str.lower()
    p = r"(\S+) (?:\S+ )*(\S+)"
    g = y['clean2'].str.extract(p)
    y['merged'] = g[0] + g[1]
    y['merged'] = y.merged.str.replace(r"\s", '', regex=True) 
    y.drop(['index', 'clean2'], axis=1, inplace=True)
    #y.set_index('merged', inplace=True)
    
    # Create cleaned field from name _ id pairs
    t = name_id.reset_index()
    t['clean'] = t.navn.str.replace(r"-", '', regex=True).str.lower()
    p = r"(\S+) (?:\S+ )*(\S+)"
    f = t['clean'].str.extract(p)
    t['merged'] = f[0] + f[1]
    t['merged'] = t.merged.str.replace(r"\s", '', regex=True) 
    t.drop('clean', axis=1, inplace=True)
    t.set_index('merged', inplace=True)
    
    df = pd.read_csv("aliases.csv").dropna(subset=['name'])
    j = df.join(name_id, on='Rett navn')
    l = j.loc[:, ['id', 'name']].set_index('name')
    
    u = pd.concat([t.id.to_frame(), l])
    
    
    
    # Merge tables
    pj = y.join(u, on='merged', lsuffix="_x", how="outer").reset_index(drop=True)

    
    
    
    # Print unmatched names    
    (pj.loc[(pj['id'].isna()) &  (pj['id_x'] == "")]
                     .drop_duplicates(subset='merged')
                     .to_csv('problems.csv')
                     )
    
    
    
    (pj.drop_duplicates(subset='merged')
        .to_csv('names.csv'))
    
if __name__ == '__main__':
    match_names()