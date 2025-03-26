#!/bin/bash

read -e -p 'Input json file: ' jsonfile
if [ ! -f "$jsonfile" ] 
then
    echo -e "\nERROR: File (${jsonfile}) does not exist. Run again." 
    exit 1
fi

# make aname for the model
modelname="${jsonfile%.*}"

# Extract the value of "name" and store it in a variable
namevalue=$(jq -r '.name' "$jsonfile")

export jsonfile modelname namevalue
features=$(sbatch --parsable --export=jsonfile,modelname features.sh)
sbatch --export=jsonfile,modelname,namevalue --dependency=afterok:$features inference.sh
