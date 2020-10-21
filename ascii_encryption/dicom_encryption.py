import glob
import os
import ascii_encryptor
import pydicom
import sys
from pathlib import Path
from multiprocessing import Pool
from functools import partial

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default='/home/dwu/data/Aneurysm/testing_cohort/20200815-aneurysm-without_SAH/selected_dicoms/')
parser.add_argument('--output_dir', type=str, default='/home/dwu/data/Aneurysm/testing_cohort/20200815-aneurysm-without_SAH/encrypted_dicoms/')
parser.add_argument('--key', type=int, default=0)
parser.add_argument('--sub_layers', type=int)

args = parser.parse_args()
for k in args.__dict__:
    print (k, '=', args.__dict__[k])
    
encryptor = ascii_encryptor.ascii_encryptor(args.key)
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

def encrypt_dcm_file(filename, output_dir, encryptor):
    try:
        dcm = pydicom.dcmread(filename)
    except Exception:
        dcm = pydicom.dcmread(filename, force=True)
    
    enc_dcm = encryptor.encrypt_dicom(dcm)
    if any(s in enc_dcm.InstitutionName.lower() for s in ['mass', 'mgh']):
        institution = 'MGH'
    elif any(s in enc_dcm.InstitutionName.lower() for s in ['brig', 'bwh']):
        institution = 'BWH'
    else:
        institution = enc_dcm.InstitutionName.upper().replace('/', ' ')
    
    dst_folder = os.path.join(output_dir, '_'.join([institution, enc_dcm.PatientID, enc_dcm.AccessionNumber]))
    if not os.path.exists(dst_folder):
        try:
            os.makedirs(dst_folder)
        except Exception:
            pass
    
    enc_dcm.save_as(os.path.join(dst_folder, os.path.basename(filename)))

glob_path = args.input_dir
for i in range(args.sub_layers):
    glob_path = os.path.join(glob_path, '*')
series_list = glob.glob(glob_path)

for i, series_dir in enumerate(series_list):
    if (i+1) % 10 == 0:
        print (i, end=',', flush=True)
    
    dcm_files = glob.glob(os.path.join(series_dir, '*.dcm'))
    p = Pool(16)
    p.map(partial(encrypt_dcm_file, output_dir = args.output_dir, encryptor = encryptor), dcm_files)
    p.close()