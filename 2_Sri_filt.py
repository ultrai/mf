# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 11:06:19 2020

@author: admin
"""
import os
os.chdir('E:\\Sri\\')
### NOTE Stop YEAR filter is 2020 Line 37
### NOTE Stop YEAR filter is 2020 Line 37
### NOTE Stop YEAR filter is 2020 Line 37
### NOTE Stop YEAR filter is 2020 Line 37
### NOTE Stop YEAR filter is 2020 Line 37
from glob import glob
from mftool import Mftool
from tqdm import tqdm
import pandas as pd
import numpy as np
lst = glob('Data\*')
mf = Mftool()
dr = 'Data_filtered//Nav_filtered_'
df = pd.read_pickle(lst[0])
temp = df.keys()[0]
df = df.rename({temp:'dummy'}, axis=1)
df3 = df
nan_list=[]
expired_list=[]
nochg_list=[]
ite = 0
for i in tqdm(iter(lst)):
    ite= ite+1
    df2 = pd.read_pickle(i)
    df2 = df2.resample('d').mean()
    #print(i)
    #print(df2.last('1d').values)
    if np.isnan(df2.last('1M').values).all():
        nan_list.append(i)
    elif len(df2.last('7d').dropna().values)<1:
        expired_list.append(i)
    elif df2.index[-1].year!=2020:
        expired_list.append(i)
    #elif (df2.last('180d').median()==df2.last('1d')).values.any():
    elif (df2.last('180d').dropna().std()<0.01).all():
         nochg_list.append(i)
    else:
        df = pd.concat([df, df2], axis=1, sort=False)
    if np.remainder(ite,1000)==0:
        df = df.drop('dummy',axis=1)
        df.to_pickle(dr +str(ite))
        df = df3

nan_list = pd.DataFrame({'NAN_codes': nan_list }) 
expired_list = pd.DataFrame({'Expired_codes': expired_list }) 
nochg_list = pd.DataFrame({'Nochg_codes': nochg_list }) 

df = df.drop('dummy',axis=1)
df.to_pickle(dr+str(ite))
nan_list.to_pickle('NAN_codes')
expired_list.to_pickle('Expired_codes')
nochg_list.to_pickle('Nochg_codes')

schemes = mf.get_scheme_codes()
schemes_list = pd.DataFrame({'Schemes': schemes }) 
schemes_list.to_pickle('schemes')

#from mftool import Mftool
#mf = Mftool()
#print(nan_list)
#print(df)
#mf.get_scheme_details("146862")    

        