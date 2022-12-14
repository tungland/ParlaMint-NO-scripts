"""
Add recommended note types

	

narrative
    Description in the third person of events taking place in the meeting, e.g. "Mr X. takes the Chair".
summary
    Summaries of speeches that are individually not interesting, e.g. "Question put and agreed to".
speaker
    Name, role and possible description of a person doing the speech
vote
    Outcome of a vote
location
    The location of the speaker, who was not on the podium
date
    Date of the session
president
    Chairman of a meeting
comment
    Comment of parliamentary reporter
time
    Date and time of the beginning and end of the debate
quorum
    The presence of the members of parliament
debate
    Comments on the conduct of debates
"""
from constants import NS
from utils import apply_to_component_files

def parse_xml(xml):

    res = xml.findall('//note', NS)
    target_notes = [x for x in res if ("type", "speaker") not in x.items()]
    
    for note in target_notes:
        note.attrib['type'] = "comment"
        

if __name__ == "__main__":
    apply_to_component_files(parse_xml)
