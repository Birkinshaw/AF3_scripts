#!/bin/bash

read -e -p 'Input json file:' jsonfile
if [ ! -f "$jsonfile" ] 
then
    echo -e "\nERROR: File (${jsonfile}) does not exist. Run again." 
    exit 1
fi
modelname="${jsonfile%.*}"

export jsonfile modelname
features=$(sbatch --parsable --export=jsonfile,modelname features.sh)
sbatch --export=jsonfile,modelname --dependency=afterok:$features inference.sh
