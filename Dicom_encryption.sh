#!/bin/bash
#SBATCH --partition=defq
#SBATCH --job-name=dicom_encryption
#SBATCH --nodelist=gpu-node005
#SBATCH --cpus-per-task=4

# python3 Dicom_encryption.py --input_dir "/home/dwu/data/DZH_DATA/2018/Aneurysm/SAH-" --output_dir "/home/dwu/data/Aneurysm/2018/SAH-" &
# python3 Dicom_encryption.py --input_dir "/home/dwu/data/DZH_DATA/2018/Aneurysm/SAH+" --output_dir "/home/dwu/data/Aneurysm/2018/SAH+" &
# python3 Dicom_encryption.py --input_dir "/home/dwu/data/DZH_DATA/2018/Aneurysm/SAH+2" --output_dir "/home/dwu/data/Aneurysm/2018/SAH+2" &
# wait

# python3 Dicom_encryption.py --input_dir "/home/dwu/data/DZH_DATA/2018/Aneurysm/Controls_SAH+" --output_dir "/home/dwu/data/Aneurysm/2018/Controls_SAH+" &
# python3 Dicom_encryption.py --input_dir "/home/dwu/data/DZH_DATA/Aneurysms 9.19.19/SAH+" --output_dir "/home/dwu/data/Aneurysm/2019/SAH+" --keep_relative_path 1 &
# python3 Dicom_encryption.py --input_dir "/home/dwu/data/DZH_DATA/Aneurysms 9.19.19/SAH-" --output_dir "/home/dwu/data/Aneurysm/2019/SAH-" --keep_relative_path 1 &
# wait

# python3 Dicom_encryption.py --input_dir "/home/dwu/data/DZH_DATA/Aneurysms 9.19.19/Ann without image/Sah-/" --output_dir "/home/dwu/data/Aneurysm/2019/Ann without image/Sah-"
# python3 Dicom_encryption.py --input_dir "/home/dwu/data/DZH_DATA/Aneurysms 9.19.19/Ann without image/Sah+/" --output_dir "/home/dwu/data/Aneurysm/2019/Ann without image/Sah+"
