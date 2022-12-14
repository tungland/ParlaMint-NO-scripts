import glob
import re
import os

# Renames the parliament reference files according to ParlaMint naming scheme


def get_date(name):
    """Processes filename

    :param name: filenam
    :type name: string
    :return: new file 
    :rtype: str
    """
    p1 = re.compile("^refs-(\d{2})(\d{2})(\d{2})-(\d{2})-(\d{2}).*\.xml$")
    p2 = re.compile("^s(\d{2})(\d{2})(\d{2})\.xml$")
    p3 = re.compile("^s(\d{2})(\d{2})(\d{2})k\.xml$")
    
    if re.match(p1, name):

        m = re.match(p1, name)
        
        year = (lambda m : m.group(3) if (int(m.group(4) )< 10) else m.group(2))(m)

        new_name = f"{''.join([m.group(1), m.group(2), m.group(3)])}_{year}{m.group(4)}{m.group(5)}"
        
    elif re.match(p2, name):
        m = re.match(p2, name)
        
        day = m.group(3)
        month = int(m.group(2))
        year = int(m.group(1))
        
        if (year < 50 and year > 0) or (year == 0 and month >= 10) :
            prefix = 20
        else:
            prefix = 19
        
        
        
        if month < 10:
            new_name = f"{prefix}{'{:02d}'.format(99 if year == 0 else year -1)}{'{:02d}'.format(year)}_{'{:02d}'.format(year)}{'{:02d}'.format(month)}{day}"
        else:
             new_name = f"{prefix}{'{:02d}'.format(year)}{'{:02d}'.format(00 if year == 99 else year + 1)}_{'{:02d}'.format(year)}{'{:02d}'.format(month)}{day}"
    
    elif re.match(p3, name):
        m = re.match(p3, name)
        
        day = m.group(3)
        month = int(m.group(2))
        year = int(m.group(1))
        
        # if (year < 50) or (year == 0 and month >= 10) :
        if (year < 50 and year > 0) or (year == 0 and month >= 10) :
            prefix = 20
        else:
            prefix = 19
        
        if month < 10:
            new_name = f"{prefix}{'{:02d}'.format(99 if year == 0 else year -1)}{'{:02d}'.format(year)}_{'{:02d}'.format(year)}{'{:02d}'.format(month)}{day}-2"
        else:
             new_name = f"{prefix}{'{:02d}'.format(year)}{'{:02d}'.format(00 if year == 99 else year + 1)}_{'{:02d}'.format(year)}{'{:02d}'.format(month)}{day}-2"
    
       
    else:
        return None
    #     raise ValueError
    
    return f"ParlaMint-NO_{new_name}.xml"


# def main():
#     #paths = glob.glob("../data/*/*")
#     paths = glob.glob("source*/*")
#     names = [x.split('/')[-1] for x in paths]
    
#     new_names ={}
#     for name in names:
#         new_name = get_date(name)
#         if new_name:    
#             new_names[name] = new_name
            
#     for path in paths:
#         name = path.split('/')[-1]
#         if name in new_names.keys():
        
#             os.rename(path, f"{'/'.join(path.split('/')[:-1])}/{new_names[name]}")
        
# if __name__ == "__main__":
#     main()

def create_doc_id(dirname : str):
    paths = glob.glob(dirname + '/*')
    names = [x.split('/')[-1] for x in paths]
    
    new_names ={}
    for name in names:
        new_name = get_date(name)
        if new_name:    
            new_names[name] = new_name
            
    for path in paths:
        name = path.split('/')[-1]
        if name in new_names.keys():
        
            os.rename(path, f"{'/'.join(path.split('/')[:-1])}/{new_names[name]}")
        


    
    
    