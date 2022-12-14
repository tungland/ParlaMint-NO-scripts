#!/bin/bash


data_source='sample_data_source'


dest1='sample_data'

source_dir1='sample_data/pre2016'
source_dir2='sample_data/post2016'
DESTINATION_FOLDER='sample_output'

# mkdir dest1
#mkdir source_dir1
#mkdri source_dir2

cp -r $data_source $dest1


mkdir $DESTINATION_FOLDER

echo "Preprocess pre 2016"
python scripts/preprocess.py $source_dir1 True
saxonb-xslt -s:$source_dir1 -xsl:scripts/pre2016.xsl -o:$DESTINATION_FOLDER

echo "Preprocess post 2016"
python scripts/preprocess.py $source_dir2 False
saxonb-xslt -s:$source_dir2 -xsl:scripts/post2016.xsl -o:$DESTINATION_FOLDER

echo "Postprocess"
python scripts/postprocess.py $DESTINATION_FOLDER

# rm -r source_dir1
# rm -r source_dir2

rm -r $dest1