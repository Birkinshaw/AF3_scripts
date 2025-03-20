import os
import json

#create a dictionary to store the data from each feature run in
data_dict = {}
for dir in os.listdir():
    #check if dir is a directory from the feature run directory
    if os.path.isdir(dir):
        print('found', dir)
        #check if the directory contains a _data.json file
        for file in os.listdir(dir):
            file_path = os.path.join(dir, file)
            if os.path.isfile(file_path) and '_data.json' in file:
                #load the data into the dictionary
                with open(file_path, 'r') as f:
                    data_dict[dir] = json.load(f)

                print(file_path, 'loaded into data_dict as', dir)

# Get the keys
data_dict_keys = list(data_dict.keys())

# Construct a dictionary with keys as integers and values as alphabets (uppercase and lowercase)
alphabet_dict = {i: chr(65 + i) if i < 26 else chr(97 + (i - 26)) for i in range(52)}

#construct the new dictionary
new_data_dict = data_dict[data_dict_keys[0]]

#add the sequences from the subsequent feature runs and change their chain id
for i in range(len(data_dict_keys) - 1):
    #add the sequences from the other feature runs
    j = i + 1
    new_data_dict['sequences'].append(data_dict[data_dict_keys[j]]['sequences'][0])
    #use the alphabet_dict to change the chain id
    new_data_dict['sequences'][j]['protein']['id']  = alphabet_dict[j]

#save the new dictionary
with open('combined_data.json', 'w') as f:
    json.dump(new_data_dict, f, indent=4)

print('combined_data.json saved')