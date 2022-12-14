from stortingsdata.postprocess.assign_ids import assign_ids
from stortingsdata.postprocess.handle_notes import handle_notes
from stortingsdata.postprocess.clean_ids import main as clean_ids
from stortingsdata.postprocess.delete_empties import main as delete_empties
from stortingsdata.postprocess.set_date_title import set_date_title as set_date_title

import sys

if __name__ == '__main__':
    
    f = sys.argv[1]
    
    #arg = sys.argv[2]
    
    # Assign speaker IDs
    print('Assigning ids')
    assign_ids(f)
    
    # Handle in text notes
    print('handling notes')
    handle_notes(f)
    
    # Clean ids
    clean_ids(f)
    
    # remove empty tags from body
    delete_empties(f)

    # fix dates and titles
    set_date_title(f)