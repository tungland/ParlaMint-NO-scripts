#!/bin/bash
# Downloads speaker data 



BASE_PATH="speaker_data"

# Download MP data
python $BASE_PATH/storting_mp_data/get_all_mp_data.py

# Download minister data
python $BASE_PATH/wikidata-regjering/collect_ministers.py

# Download president data
python $BASE_PATH/presidentskap/presidentskap.py

# Get all names from parlament data
python $BASE_PATH/speaker_names_from_output/get_all_speakers.py


# Create name_id_list
# python $BASE_PATH/name_id.py TODO: broken