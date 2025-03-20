# Script to combine _data.json files from multiple feature runs.

The combine_features.py will find any file called "_data.json" in a subdirectory of this directory 
and combine them into one _data.json file called combined_data.json which you can pass to inference.

eg.
have directory called with:

combine_features.py
chainA/chainA_data.json
chainB/chainB_data.json

run script:

python combine_features.py

creates
combine_features.py
chainA/chainA_data.json
chainB/chainB_data.json
combined_data.json

pass combined_data.json to inference:

alphafold3 -c -i combined_data.json -o combined-inference