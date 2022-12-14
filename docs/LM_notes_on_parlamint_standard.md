# LMs' notes on parlamint corpora structure

## Intro
Parlmint corpora encoding is a specialization of Parla-CLARIN, which is a customization of TEI. I.e. Parla-CLARIN is a flexible standard for describing parliamentary proceedings, while parlamint is a more rigid implementation.

Parlamint structure is described in docs in parlamints github repo.

This documents contains notes and comments on the parlamint standard.


## General
The document contains notes on langueage and dir structure, filenames. 

Important to note: the corpus consists of a plain text version and a linguistically annotated version

Note:
* No tab - should be space
* No-break space --> space
* Non-breaking hyphen --> hyphen
* Soft hyphen  --> to remove

Standard values Norsk
no, nb, nn

Time
yyyy-mm-dd

### Filenames
Root file: ParlaMint-NO.xml
Corpus component: root, undersdcore, date of transcription

## Metadata
### The corpus root file:
Conains a title statement
With the paralmentary term


## Utterances and Notes


### Notes

From article:  
>    The following columns quantifies the elements that appear in the corpus texts apart from speeches. Namely, the transcripts also contain session or agenda titles, names of speakers or chairs etc., which have been preserved in about half of the corpora and marked up as headings, the number of which is shown in the “Head” column. Furthermore, the transcripts contain many transcriber notes, i.e. remarks about time, voting, interruptions, applause, the fact that the speaker could not be understood etc. Such commentary was identified and marked up in the corpora in two ways. The default was to mark them up as notes, while some corpora also use more precise elements, the sum of which is shown in the “Incidents” column; these elements are “vocal” (non-lexical vocalised phenomena, e.g. exclamations from the auditorium), “kinesic” (non-vocalised communicative phenomena, e.g. applause) and “incident” (non-communicative phenomena, e.g. coughing).  



