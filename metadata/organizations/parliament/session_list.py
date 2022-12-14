from datetime import date
import pandas as pd
from sqlalchemy import create_engine

def add_year(d):
    return d.replace(year = d.year + 1)

def sessions():
    y1 = date(1998, 10, 1)
    y2 = date(1999, 9, 30)

    start = list()
    end = list()
    id = list()

    while y2.year < 2022:
        start += [y1]
        end += [y2]
        id +=[f"{y1.year}-{y2.year}"]
        
        y1 = add_year(y1)
        y2 = add_year(y2)
        
    return pd.DataFrame([id, start, end]).transpose().set_axis(['session_id', 'start_date', 'end_date'], axis=1)
    
    
def main():
    engine = create_engine('postgresql://larsm:admin@localhost:5432/parlamint')
    
    df = sessions()
    
    df.to_sql('sessions', engine)
    
if __name__ == '__main__':
    main()
    
    