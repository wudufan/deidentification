#!/usr/bin/env python
# coding: utf-8

# In[1]:


# encrypt all the folder names and contents in dicom images


# In[30]:


import glob
import os
import encrpytion
import pydicom
import sys
from pathlib import Path


# In[38]:


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default='/home/dwu/data/DZH_DATA/2018/Aneurysm/Controls_SAH+/')
parser.add_argument('--output_dir', type=str, default='/home/dwu/data/Aneurysm/2018/Controls_SAH+/')
parser.add_argument('--keep_relative_path', type=int, default=0)
parser.add_argument('--overwrite', type=int, default=1)

if sys.argv[0] != 'Dicom_encryption.py':
    args = parser.parse_args(['--keep_relative_path', '0', 
                              '--overwrite', '0'])
else:
    args = parser.parse_args()

for k in args.__dict__:
    print (k, '=', args.__dict__[k])


# In[39]:


encrpytor = encrpytion.Simple_encryptor('aneurysm')


# In[40]:


if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)


# In[41]:


# encrpyt the dicoms and put into folder according to MRN_ACC
mrns = glob.glob(os.path.join(args.input_dir, '*'))
print (len(mrns))
for k, mrn in enumerate(mrns):
    print (k, end=',', flush=True)
    filenames = Path(mrn).rglob('*.dcm')
    for i, filename in enumerate(filenames):
        dcm = pydicom.dcmread(str(filename), force=True)
        dcm = encrpytor.Encrypt_dicom(dcm)
        
        if not args.keep_relative_path:
            dst_folder = os.path.join(args.output_dir, encrpytor.Get_folder_name(dcm))
        else:
            dst_folder = os.path.dirname(str(filename)).replace(args.input_dir, args.output_dir)
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)
        if i == 0 and os.path.exists(dst_folder) and not args.overwrite:
            break
        
        dcm.save_as(os.path.join(dst_folder, os.path.basename(str(filename))))


# In[ ]:




