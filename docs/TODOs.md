# TODOs


Conversion
- [X] ~~Add speaker attriputes~~
- [X] ~~Uterrance segments~~
- ~~[X] Note tags~~
- ~~[X] Create 2017-2021 corpus~~

- [X] Create corpus component header template
- [ ] Dynamic metadata for component files
  - [x] ~~Date~~
  - [X] URI/filename
    - [X] Filename should be ´ParlaMint-NO_YYYY-MM-DD.xml´
- [X] XML:id for utterances and segments


Tags
- [ ] Kongen alt. other "speech" tags 
- [X] Div, head elements
- [ ] Sitat
- [X] Updating president
- [ ] For "høring" - manage chair, guest speakers


Corpus root
  - [ ] Create corpus root
  - [ ] List of speakers
  - [ ] List of orgs


### Metadata
- [ ] Create db to xml lxml script
#### People
- [ ] uri for people
  - [x] ~~Harvest list of all speakers from transcription~~
  - [X] Look in to xslt uri tools - python script
  - [x] ~~Give uri to all speaker headers - create python script~~
- [x] ~~List of speakers~~
- [X] List of organizations
- [ ] ~~How to get location, date of each document~~
- [ ] Presidentskap
- [ ] Regjeringsmedlemmer
  - [ ] Root
  - [ ] Speakere
- [ ] Match names
  - [ ] Make table of aliases
  - [ ] 


#### Orgs
- [ ] Create org table
- [ ] Create memberships table

Tests
- [ ] Compare text from unconverted and converted documents - is it preserved?

Text issues
- ~~[X] Segmenteringen oppfører seg rart i tilfeller med uthevet skrift - den deler inn i segmenter på kursiv. Dette er en konsekvens av fjerning av "navn" subfeltet~~

OBS
* ~~Noen ganger har presidentens personID et ekstra tall - må cle~~

Usikkert
* ~~Hvor mange typer møter er det i stortings refereatene?~~

