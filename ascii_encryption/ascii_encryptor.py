#!/usr/bin/env python
# coding: utf-8

# In[56]:


import glob
import os
import numpy as np
import pandas as pd
import pydicom
import re

# simple encryptor, convert 0-9, a-z, A-Z to their corresponding ascii hex.
# A bias between 00 to FF is added to each char and then mod 256. The bias changes at different positions
# A encrypted string begins and ends with M and end with N.
# v1: the bias is added as np.arange(len(string)) - (key * len(string)) % 256, the problem is each character are quite close. Please use v2.
# If the enclosed string begins with K (embeded key), then the next two letters are the key of the encryption;
# If the enclosed string begins with L (hidden key), then the next two letters are just the length of string.
#
# v2: different bias: the bias is np.arange(len(string) * (key - 1)) % 256
# If the enclosed string begins with J (embeded key), then the next two letters are the key of the encryption;
# If the enclosed string begins with H (hidden key), then the next two letters are just the length of string.
class ascii_encryptor:
    def __init__(self, key = 0):
        self.key = key
        
        self.dicom_erase_field = ['ReferringPhysicianName', 
                                  'PerformingPhysicianName', 
                                  'NameOfPhysiciansReadingStudy', 
                                  'OperatorsName', 
                                  'PatientSex', 
                                  'OtherPatientNames',
                                  'PatientTelephoneNumbers',
                                  'PatientAddress',
                                  'PatientBirthDate', 
                                  'PatientAge']
        self.dicom_remove_field = ['InstitutionalDepartmentName',
                                   'MilitaryRank', 
                                   'StationName', 
                                   'BranchOfService', 
                                   'AdditionalPatientHistory']
        self.dicom_encrypt_field = ['AccessionNumber', 
                                    'StudyID',
                                    'PatientName',
                                    #'InstitutionName', 
                                    'PatientID']
    
    def is_embed_key(self, mode):
        return (mode == 'K' or mode == 'J')
    
    def key_version(self, mode):
        if mode == 'K' or mode == 'L':
            return 'v1'
        elif mode == 'J' or mode == 'H':
            return 'v2'
        else:
            raise ValueError('mode must be one of K,L,J,H')
    
    def encode_string(self, string, mode = 'J'):
        key = self.key % 256
        
        if self.key_version(mode) == 'v1':
            bias = np.arange(len(string)) - (key * len(string)) % 256
        else:
            bias = (np.arange(len(string)) * key) % 256
            
        encrypt_array = ['0x{:02x}'.format((ord(string[i]) + bias[i]) % 256)[2:].upper() for i in range(len(string))]
        if self.is_embed_key(mode):
            # embedded key
            encrypt_array = ['M', mode, '0x{:02x}'.format(key)[2:].upper()] + encrypt_array + ['N']
        else:
            # hidden key
            encrypt_array = ['M', mode, '0x{:02x}'.format(len(encrypt_array) % 256)[2:].upper()] + encrypt_array + ['N']
        
        return ''.join(encrypt_array)
    
    def __decode_single_string(self, string):
        mode = string[0]
        if self.is_embed_key(mode):
            key = int(string[1:3], 16)
        else:
            key = self.key
        
        string = string[3:]
        if self.key_version(mode) == 'v1':
            bias = np.arange(len(string) // 2) - (key * len(string) // 2) % 256
        else:
            bias = (np.arange(len(string) // 2) * key) % 256
            
        dec_array = [chr((int(string[i:i+2], 16) - bias[i//2])%256) for i in range(0, len(string), 2)]
        
        return ''.join(dec_array)
    
    def decode_string(self, string):
        tokens = re.findall('M[KLJH][0-9A-F]*N', string)
        dec_tokens = [self.__decode_single_string(t[1:-1]) for t in tokens]
        for t,d in zip(tokens, dec_tokens):
            string = string.replace(t,d)
        
        return string
    
    def encrypt_dicom(self, dcm, mode = 'J'):
        for field in self.dicom_erase_field:
            if field in dcm:
                setattr(dcm, field, ' ')
        
        for field in self.dicom_remove_field:
            if field in dcm:
                delattr(dcm, field)
        
        for field in self.dicom_encrypt_field:
            if field in dcm:
                string = str(getattr(dcm, field))
                setattr(dcm, field, self.encode_string(string, mode))
        
        return dcm

