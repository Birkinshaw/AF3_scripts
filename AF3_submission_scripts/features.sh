#!/bin/bash
#SBATCH --job-name=AF3_features
#SBATCH --partition=regular   
#SBATCH --time=0-05:00:00             
#SBATCH --mem=64G
#SBATCH -c 10
#SBATCH -n 1
#SBATCH --export=ALL
#SBATCH -o AF3_logs/%x_%j.out
module load alphafold/3.0.0
alphafold3 -f -i ${jsonfile} -o ${modelname}


