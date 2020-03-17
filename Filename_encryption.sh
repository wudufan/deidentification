#!/bin/bash
#SBATCH --partition=defq
#SBATCH --job-name=filename_encryption
#SBATCH --nodelist=gpu-node005
#SBATCH --cpus-per-task=4

python3 Filename_encryption.py --input_dir "/home/dwu/data/DZH_DATA/check" --output_dir "/home/dwu/data/Aneurysm/check"
python3 Filename_encryption.py --input_dir "/home/dwu/data/DZH_DATA/label" --output_dir "/home/dwu/data/Aneurysm/label"
python3 Filename_encryption.py --input_dir "/home/dwu/data/DZH_DATA/Sample3D" --output_dir "/home/dwu/data/Aneurysm/Sample3D"