# ParlaMint-NO

Norske ParlaMint data.

Dette korpuset inneholder den norske delen av [ParlaMint prosjektet](https://www.clarin.eu/parlamint). ParlaMint er et EU-støttet prosjekt støttet av [CLARIN ERIC](https://www.clarin.eu/), et europeisk konsortium for forskningsinfrastruktur for språkressurser. 

Inneholder referater fra følgene møter:
* Møter i Stortinget oktober 1998 - september 2022.
* Lagtinget og Odelstinget oktober 1998 - juni 2009

Tekstdata er hentet fra Stortingets API, og konvertert til ParlaMint med XSLT og Python. Metadata for Stortingsrepresentanter og Ministere er hentet fra Stortingets API og Wikidata. 

## ParlaMint
ParlaMint er et prosjekt støttet av CLARIN ERIC. Prosjektet handler om å lage sammenlignbare og uniformt annoterte korpus fra parlamentarisk møtereferater.
Prosjektside: https://www.clarin.eu/parlamint
Github: https://github.com/clarin-eric/ParlaMint/

## Format og struktur
Korpuset består av xml-filer i ParlaMint format. ParlaMint er et XML-skjema, en spesialisering av Parla-CLARIN. Parla-CLARIN er et TEI-format laget for å beskrive parlamentariske referater. 
ParlaMint-skjemaet er beskrevet i detalj i prosjektets [GitHub-repositorie](https://clarin-eric.github.io/ParlaMint/). Det mer generelle Parla-CLARIN er beskrevet [her](https://clarin-eric.github.io/parla-clarin/).

Korpuset består av to deler. Den ene ("TEI") består av Stortingsreferater med informasjone om talere. Den andre ("TEI.ana") inneholder de samme tekstene med lingvistiske data annotert på ord og setningsnivå. 

Hver del av korpuset har en rot-fil (`ParlaMint-NO.xml`, `ParlaMint-NO.ana.xml`) og består forøvrig av delfiler. Delfilene er sortert i mapper etter kalenderår (OBS: mappestrukturen følger ikke parlamentarisk år). Hvert delfilnavn består av stammen "ParlaMint-NO_" og møtets dato. Møter i Lagtinget har også "-upper" i navnet. Møter i Odelstinget har "-lower" som kode. Noen dager har mer en ett møte. Da har møter etter det første et løpenummer, eg. "-*N*". Det er ingen dager med mer enn to møter i samme kammer. Hver TEI-fil (`.xml`-utvidelse ) har en tilsvarende TEI.ana-fil med utvidelse `.ana.xml` basert på det samme innholdet.

Hver delfil har et hode-element (`teiHeader`) som inneholder metadata om innholdet og et element `text` med filens innhold.

Rot-filene inneholder metadata for hver del av korpuset, inkludert:
* Antall ord og setninger.
* Metadata for talere.
* Metadata for organisasjoner.
* Taksonomier.

### Metadata
Korpuset består av xml-filer markert i ParlaMint-skjema. 

To deler (`TEI`, `TEI.ana`). 

Hver del består av:
* Rotfil
* 3267 delfiler

Korpuset inneholder
* 398781 taler
* 97541932 ord

## Ressurser
ParlaMint prosjektet tilbyr scripts og programmer for å jobbe med med ParlaMint-data. Dette inkluderer oppgaver som:
* Hente ut all tekst.
* Konvertere til `.conllu` 

## Kommentarer
Lagting og Odelsting: Norge har siden 1814 formelt hatt et en-kammersystem, men i praksis var det mellom 1814 og 2009 en variant av et to-kammersystem. I denne perioden delte Stortinget seg selv i to avdelinger, Odelstinget og Lagtinget, som henholdsvis hadde funksjoner som underhus og overhus. Ordningen med Lagting og Odelsting ble brukt for siste gang i 2009. 

I ParlaMint-NO vil det si at det i perioden 1998-2009 finnes tre typer referater:
* Fra Odelstinget, markert med "-lower" i filtittel.
* Fra Lagtinget, markert med "-upper" i filtittel.
* Fra begge avdelinger, uten noen markering.

Fra 2009 finnes ikke disse skillene.


## Lisens
*språkbank lisens*


## Lenker:
Stortingets API:
https://data.stortinget.no/  
ParlaMint II prosjektside:
https://www.clarin.eu/parlamint  
ParlaMint - Github:
https://github.com/clarin-eric/ParlaMint/  
Clarin ERIC:
https://www.clarin.eu/  
Github repo med scripts for å lage dette korpuset.
https://github.com/tungland/ParlaMint-NO-scripts


