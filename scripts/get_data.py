from lxml import etree
import requests
from bs4 import BeautifulSoup as bs
import os

"""Script for scraping Norwegian parliament API
    """



def parse_session_list(session_list_url):
    "Parses list of parliament sessions"
    r = requests.get(session_list_url)
    soup = bs(r.content, "lxml-xml")
    
    for session in soup.find_all('sesjon'):
        yield session.find('id').text
    
    
    
def parse_session(session_id, publications_link):
    "Parses list of publications per parliament session"
    
    r = requests.get(publications_link.format(session_id))
    soup = bs(r.content, "lxml-xml")
    
    for id in soup.find_all('id'):
        yield id.text


def parse_pub(pub_id, session_id, minutes_link, base_path='data/'):
    """Writes publication to local

    Args:
        pub_id (str): publication id
        session_id (str): session id, i.e. 1998-99 etc.
        minutes_link (str): base url for meeting minutes
        base_path (str, optional): folder to store data into. Defaults to 'data/'.
    """
    r = requests.get(minutes_link.format(pub_id), "lxml-xml")
    #soup = bs(r.content, "lxml-xml")
    root = etree.fromstring(r.content)
    et = etree.ElementTree(root)
    et.write(f'{base_path}{session_id}/{pub_id}.xml')
    
    
def main():
    sessions_link = "https://data.stortinget.no/eksport/sesjoner"
    publications_link = "https://data.stortinget.no/eksport/publikasjoner?publikasjontype=referat&sesjonid={}"
    minutes_link = "https://data.stortinget.no/eksport/publikasjon?publikasjonid={}"
    base_path = "data/"

    os.mkdir(base_path)
    for id in parse_session_list(sessions_link):
        os.mkdir(f"{base_path}{id}")
        for id2 in parse_session(id, publications_link):
            try:
                parse_pub(id2, id, minutes_link)
            except:
                with open("Corrupted_documents.txt", "a") as f:
                    f.write(str(minutes_link.format(id2) )+ ", ")
    
def provisional():
    minutes_base_uri = "https://data.stortinget.no/eksport/publikasjon?publikasjonid={}"   
    url = "https://data.stortinget.no/eksport/publikasjoner?publikasjontype=referat&sesjonid=2005-2006"
     
     
    os.mkdir("debugging_data")
    r = requests.get(url)
    soup = bs(r.content, "lxml-xml")
    
    for id in soup.find_all('id'):
        try:
            parse_pub(id.text, "debugging_data", minutes_base_uri, base_path='')
        except:
            print("Error ", id.text) 
         
    
    
if __name__ == '__main__':
    main()
    #provisional()
    