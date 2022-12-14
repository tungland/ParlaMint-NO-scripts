#!/bin/bash

source_dir1="pre2016"
source_dir2="post2016"

DESTINATION_FOLDER="output"


# Pre 2016 Schema
mkdir $DESTINATION_FOLDER

mkdir $source_dir1

# Collected parlament
cp data/*/s*.xml $source_dir1
# Upper house
cp data/*/l*.xml $source_dir1
# lower house
cp data/*/o*.xml $source_dir1

echo "Preprocessing pre 2016"
python scripts/preprocess.py $source_dir1 True

saxonb-xslt -s:$source_dir1 -xsl:scripts/pre2016.xsl -o:$DESTINATION_FOLDER


# Post 2016 schema
mkdir $source_dir2

cp data/*/refs*.xml $source_dir2

echo "Preprocessing post 2016"
python scripts/preprocess.py $source_dir2 False

saxonb-xslt -s:$source_dir2 -xsl:scripts/post2016.xsl -o:$DESTINATION_FOLDER

# Post

python scripts/postprocess.py $DESTINATION_FOLDER

# Delete tmp files
rm -r $source_dir1 $source_dir2




