# README

## Conversion to ParlaMint
Install an XSLT processor, eg. this CLI tool for Saxon:  
`sudo apt install libsaxonb-java`



Download corpus  
`python scripts/get_data.py`

Move the files we want to temporary pre and post 2016 folders 
`cp data/*/s*.xml source_pre2016`  
`cp data/*/refs*.xml source_post2016`   
This also deduplicates 

Clean those files  
`python scripts/replace_e_paths.py`

Name files  
`python scripts/create_doc_id.py`

Pre 2016 requires the dtd to be present  
`cp docs/forhandl_xml.dtd source_pre2016/`

Create output dir  
`mkdir output`

Convert with saxon  
`saxonb-xslt -s:source_pre2016 -xsl:scripts/pre2016.xsl -o:output`  
`saxonb-xslt -s:source_post2016 -xsl:scripts/post2016.xsl -o:output`







