import argparse
import json
import os
from collections import OrderedDict

# Set up argument parser
parser = argparse.ArgumentParser(description="add a cif restraint file to an AF3 .json file.")
parser.add_argument('json_file', help="Path to the input .json file")
parser.add_argument('cif_file', help="Path to the input .cif file")
parser.add_argument('output_file', help="Path to the input .cif file")

# Parse arguments
args = parser.parse_args()



# Open and load the JSON file
with open(args.json_file, 'r') as file:
    data = json.load(file, object_pairs_hook=OrderedDict)

# Open the cif file in read mode
with open(args.cif_file, 'r') as file:
    content = file.read()

#process the cif file to insert it into the json file (replace doublequotes with single quotes)
#note would normally need to escape backslashes, but this is handled by json.dump()
# Replace double quotes with single quotes
modified_content = content.replace('"', "'")



# Append a new string to the 'userCCD' value
if 'userCCD' in data:
    data['userCCD'] += '\n' + modified_content
else:
    # Create a new OrderedDict to maintain the desired order
    new_data = OrderedDict()
    for key, value in data.items():
        if key == 'modelSeeds':
            # Add 'userCCD' before 'modelSeeds'
            new_data['userCCD'] = modified_content  # Replace "default_value" with the desired initial value
        new_data[key] = value
    data = new_data


# Write the modified JSON back to the file
with open(args.output_file, 'w') as file:
    json.dump(data, file, indent=4)

print("The cif file has been added to the JSON file.")

