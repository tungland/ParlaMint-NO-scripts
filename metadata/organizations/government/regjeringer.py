import re, pandas as pd
from sqlalchemy import create_engine
from datetime import date
import numpy as np
import dateparser

def remove_special_characters(s : pd.Series):
    return (s.str.replace('æ', 'ae')
      .str.replace('ø', 'o')
      .str.replace('å', 'aa')
      )    


def govtid(string : str):
    p = r"(\w+)'s (first |second )?government"
    m = re.search(p, string)
    if not m:
        return None
    else:
        govt = m.group(1).lower()
        n = '1'
        if m.group(2):
            n = m.group(2)
        
            if n == 'second ':
                n = '2'
            else:
                n = '1'
        
       
            
        return "government." + govt + n    
        

def regjeringer():
    engine = create_engine('postgresql://larsm:admin@localhost:5432/parlamint')
    l = """Jonas Gahr Støres regjering
2021-
14. oktober 2021–
AP, SP
1
Erna Solbergs regjering
2013-2021
16. oktober 2013–14. oktober 2021
H, FRP;H, FRP,V;H, FRP, V, KRF;H, V, KRF
1
Jens Stoltenbergs andre regjering
2005-2013
17. oktober 2005–16. oktober 2013
AP, SP, SV
1
Kjell Magne Bondeviks andre regjering
2001-2005
19. oktober 2001–17. oktober 2005
KRF, H, V
1
Jens Stoltenbergs første regjering
2000-2001
17. mars 2000–19. oktober 2001
AP
0
Kjell Magne Bondeviks første regjering
1997-2000
17. oktober 1997–17. mars 2000
KRF, V, SP
1"""

    name = l.split("\n")[::5]
    years = l.split("\n")[1::5]
    dates = [x.split('–') for x in l.split("\n")[2::5]]
    start = [dateparser.parse(x[0]) for x in dates]
    end = end = [dateparser.parse(x[1]) if x[1] != '' else np.NAN for x in dates]
    
    parties = [x.split(';') for x in l.split("\n")[3::5]]
    coalition = [bool(int(x))  for x in l.split("\n")[4::5]]
    
    govts = pd.DataFrame([name, years, start, end, parties, coalition]).transpose()
    
    #return govts
    govts.columns = ['name_no', 'period_years', 'start_date', 'end_date', 'parties', 'coalition']
    
    # Create english version
    govts['name_en'] = (govts['name_no'].str.replace('andre', 'second')
                .str.replace('første', 'first')
                .str.replace('regjering', 'government')
                .str.replace(r"(s (?:first|second)? ?government)", r"'\1", regex=True)
                
                )
    
    # Split multicoalition erna solberg
    #govts.loc[1, 'parties'] = [x.split(' ,') for x in govts.parties[1]]
    #govts.loc[:, 'parties'] = [x.split(' ,') for sublist in govts.parties for x in sublist]
    
    # Add ids
    govts['id'] = govts.name_en.apply(govtid)
    govts['id'] = remove_special_characters(govts['id'])
    
    #govts.to_sql('governments', engine, if_exists='replace')
    govts.to_sql('governments', engine)
    #return govts
    
if __name__ == '__main__':
    regjeringer()