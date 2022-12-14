# Notes on the Norwegian parlament data



## bicameralism
During the period, norway switches from a bi-cameral to a unicameral parliament. 

In the 98 - 2016 the code of the minutes is the date preceeded by one of the letters h, s, o, l. 
1. h - høring - hearing
2. o - odelstinget (lower house)
3. l - lagtinget (upper house)
4. s - samlet - gathered

From 2009-10 only h and s are used, end of bicameralism

## Schema 

From 2016-17 the XML schema used by the norwegian parliament changes. Described in [](forhandl_xml.dtd) and [](forhandlinger.dtd)

### Tags that indicate utterances
* Presinnlegg
* Hovedinnlegg
* Replikk
* Kongen ?
* Andre???

### Quotes
- [ ] Blokksitat
- [ ] Sitat
### Actions, sounds
- [ ] Investigate "Hangling" tag

## Corrupted docs

Some docs are corrupt. See [Corrupted documents](Corrupted_documents.txt)

## kongen
Kongen taler til stortinget en gang i året. 

Fra 1999 til 2004 markeres denne med taggen "kongen". Fra 2016 - 2021 har man tagen "Kongen". I mellom disse så virker det å være et fall i nøyaktigheten på markup, og kongens tale er kunn markert med "a"-tagger.

F.eks. se:

* [2005](../data/2005-2006/s051011.xml)
* [2012](../data/2012-2013/s121002.xml)
* [2014](../data/2014-2015/s141002.xml)

## Change of meeting chair
The chair/president of the meeting is noted in the meeting head, but a change in chair is noted in free text. 