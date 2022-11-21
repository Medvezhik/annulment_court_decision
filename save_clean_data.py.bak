#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import re


# In[2]:


data1 = pd.read_csv('mosgorsud.csv')
data2 = pd.read_csv('mosgorsud01.csv')
def verdict_to_int(verdict_str):
    if 'Оставить' in verdict_str.split():
        return 0
    if (('Отменить' in verdict_str.split()) 
          or ('Изменить' in verdict_str.split())):
        return 1
def clear_text(text):
    return " ".join(re.sub(r'[^u"а-яА-Я"]', ' ', text.lower()).split())

def len_txt(text):
    len_t = len(str(text).split())
    return len_t

data = pd.concat([data1,data2])
data.drop_duplicates(inplace=True)
data['target'] = data['verdict_up'].apply(verdict_to_int)
data = data[data['target'].notna()]
data['clear_text'] = data['text'].apply(clear_text)
data = data[['clear_text','target']]
data.reset_index(drop=True, inplace=True)
data['len_txt'] = data['clear_text'].apply(len_txt)
data = data.query('len_txt < 15000')
data.reset_index(drop=True, inplace=True)
data.to_csv('data_clean.csv', index=False)

