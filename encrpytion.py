#!/usr/bin/env python
# coding: utf-8

# In[127]:


import glob
import os
import numpy as np
import pandas as pd
import pydicom


# In[154]:


class Simple_encryptor:
    def __init__(self, filename):
        self.reorder = pd.read_csv(filename+'_reorder.csv').to_numpy()
        self.mapping_string = pd.read_csv(filename+'_mapping_string.csv').to_numpy()
        self.mapping_file = pd.read_csv(filename+'_mapping_filename.csv').to_numpy()
        
        # convert the reorder contents to int
        for col in range(1,3):
            for row in range(self.reorder.shape[0]):
                self.reorder[row][col] = np.array([int(k) for k in self.reorder[row][col].split(',')])
    
        self.dicom_erase_field = ['ReferringPhysicianName', 
                                  'PerformingPhysicianName', 
                                  'NameOfPhysiciansReadingStudy', 
                                  'OperatorsName', 
                                  'PatientSex', 
                                  'PatientBirthDate', 
                                  'PatientAge']
        self.dicom_remove_field = ['InstitutionalDepartmentName',
                                   'MilitaryRank', 
                                   'StationName', 
                                   'BranchOfService', 
                                   'AdditionalPatientHistory']
        self.dicom_encrypt_field = ['AccessionNumber', 
                                    'PatientName',
                                    'InstitutionName', 
                                    'PatientID']
    
    def Encrypt_string(self, string, mapping = None):
        if mapping is None:
            mapping = self.mapping_string
        m = mapping
        
        string = str(string)
        string = np.array(list(string))[self.reorder[len(string)-1][1]]
        string = ''.join([m[np.where(m[:, 0] == s)[0][0]][1] if s in m[:, 0] else s for s in string])
        
        return string
    
    def Decrypt_string(self, string, mapping = None):
        if mapping is None:
            mapping = self.mapping_string
        m = mapping
        
        string = str(string)
        string = np.array(list(string))[self.reorder[len(string)-1][2]]
        string = ''.join([m[np.where(m[:, 1] == s)[0][0]][0] if s in m[:, 1] else s for s in string])
        
        return string
    
    def Encrypt_filename(self, filename, level = 1):
        '''
        @param: level: for a path, how many directories to be encrypted from the farest one
        '''
        m = self.mapping_file
        
        basenames = []
        for i in range(level):
            basenames.append(self.Encrypt_string(os.path.basename(filename).lower(), self.mapping_file))
            filename = os.path.dirname(filename)
        
        return os.path.join(*([filename] + basenames[::-1]))
    
    def Decrypt_filename(self, filename, level = 1):
        '''
        @param: level: for a path, how many directories to be encrypted from the farest one
        '''
        m = self.mapping_file
        
        basenames = []
        for i in range(level):
            basenames.append(self.Decrypt_string(os.path.basename(filename).lower(), self.mapping_file))
            filename = os.path.dirname(filename)
        
        return os.path.join(*([filename] + basenames[::-1]))
    
    def Encrypt_dicom(self, dcm):
        for field in self.dicom_erase_field:
            if field in dcm:
                setattr(dcm, field, ' ')
        
        for field in self.dicom_remove_field:
            if field in dcm:
                delattr(dcm, field)
        
        for field in self.dicom_encrypt_field:
            if field in dcm:
                # use lower only encryption, because usually the folder will be named with mrn and acc. This will avoid potential conflict in Windows
                string = str(getattr(dcm, field)).lower()
                setattr(dcm, field, self.Encrypt_string(string, self.mapping_file))
        
        return dcm
    
    def Get_folder_name(self, dcm):
        return '_'.join([dcm.PatientID, dcm.AccessionNumber])


# In[141]:


# generate two mapping charts: reorder and remapping (0-9, space and a-z. Everything is converted to lowercase)
# this is not a strong encryption, but should be enough for deidentification purpose


# In[121]:


if __name__ == '__main__':
    filename = 'aneurysm'
    np.random.seed(int.from_bytes(bytes(filename, 'utf-8'), 'little') % 2**32)
    
    # generate reorder chart
    records = []
    for i in range(255):
        forward = np.arange(i+1)
        np.random.shuffle(forward)
        backward = np.argsort(forward)
        
        fstr = ','.join([str(k) for k in forward])
        bstr = ','.join([str(k) for k in backward])
        
        records.append([i+1, fstr, bstr])
    pd.DataFrame(records, columns=['length', 'forward', 'backward']).to_csv(filename+'_reorder.csv', index=False)
    
    # generate character re-mapping chart, full
    src_chars = [chr(k) for k in [32, 45, 94, 95]+ list(range(48, 58)) + list(range(65,91)) + list(range(97,123))]
    dst_chars = np.copy(src_chars)
    np.random.shuffle(dst_chars)
    pd.DataFrame({'source': src_chars, 'target': dst_chars}).to_csv(filename+'_mapping_string.csv', index=False)
    
    src_chars = [chr(k) for k in [32, 45, 95]+ list(range(48, 58)) + list(range(97,123))]
    dst_chars = np.copy(src_chars)
    np.random.shuffle(dst_chars)
    pd.DataFrame({'source': src_chars, 'target': dst_chars}).to_csv(filename+'_mapping_filename.csv', index=False)


# In[151]:


if __name__ == '__main__':
    filename = 'aneurysm'
    f = Simple_encryptor(filename)
    
    s1 = f.Encrypt_string('MICKEY')
    s2 = f.Decrypt_string(s1)
    print (s1, s2)
    
    s1 = f.Encrypt_filename('/home/dwu/data/DZH_DATA/2018/Aneurysm/SAH-/1225515/9272310 - CT - NEURO - CTANGH-3D', 2)
    s2 = f.Decrypt_filename(s1, 2)
    print (s1)
    print (s2)
    
    dcm_files = glob.glob('/home/dwu/data/DZH_DATA/2018/Aneurysm/SAH-/1225515/*/*/*.dcm')
    img = pydicom.dcmread(dcm_files[0], force=True)
    img_enc = f.Encrypt_dicom(img)


# In[153]:


if __name__ == '__main__':
    import subprocess
    subprocess.check_call(['jupyter', 'nbconvert', '--to', 'script', 'encrpytion'])


# In[ ]:




