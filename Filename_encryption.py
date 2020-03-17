#!/usr/bin/env python
# coding: utf-8

# In[1]:


# encrypt the MRNs in the filenames of intermediate results (npy, png, etc)


# In[10]:


import glob
import os
import encrpytion
import shutil
import sys
from pathlib import Path


# In[11]:


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default='/home/dwu/data/DZH_DATA/check/')
parser.add_argument('--output_dir', type=str, default='/home/dwu/data/Aneurysm/check/')

if sys.argv[0] != 'Filename_encryption.py':
    args = parser.parse_args([])
else:
    args = parser.parse_args()

for k in args.__dict__:
    print (k, '=', args.__dict__[k])


# In[12]:


encrpytor = encrpytion.Simple_encryptor('aneurysm')


# In[13]:


if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)


# In[14]:


# split by '_' and encrypt the first part
filenames = glob.glob(os.path.join(args.input_dir, '*'))
print (len(filenames))
for i, filename in enumerate(filenames):
    print (i, end=',', flush=True)
    
    name = os.path.basename(filename)
    mrn = name.split('.')[0].split('_')[0]
    mrn_enc = encrpytor.Encrypt_filename(mrn)
    dstname = os.path.join(args.output_dir, name.replace(mrn, mrn_enc))
    
    shutil.copyfile(filename, dstname)


# In[ ]:




