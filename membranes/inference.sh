#!/bin/bash
#SBATCH --job-name=AF3_inference
#SBATCH --partition=gpuq   
#SBATCH --time=0-01:00:00            
#SBATCH --gres=gpu:A30:1   
#SBATCH --mem=64G
#SBATCH -c 8
#SBATCH -n 1
#SBATCH --export=ALL
#SBATCH -o AF3_logs/%x_%j.out

module load alphafold/3.0.0
alphafold3 -c -i ${modelname}/${namevalue}/${namevalue}_data.json -o ${modelname}-inference

