# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 13:46:40 2020

@author: admin
"""

import os
os.chdir('E:\\Sri\\')

from glob import glob
from mftool import Mftool
from tqdm import tqdm
import pandas as pd
import numpy as np
lst = glob('Data_filtered\\Nav*')
mf = Mftool()
ite_code = 0
Val = np.zeros([15000,7])
date_object = ["7d","30d","90d","180d","12M","36M","60M"]
wei = [53,12,4,2,1,0.333,0.2]
#df = pd.DataFrame({'dummy': rank_mat }, index = date_object) 
Cod = []
select = []
select_pct = []
New_scheme=[]    
for i in tqdm(iter(lst)):
    df = pd.read_pickle(i)
    #df = df.drop('dummy',axis=1)
    codes = df.keys()
    for code in iter(codes):
        #Val = Val_d
        if code=='118834':
            print('found')
            kok=df[code]
        if code=='100041':
            print('found')
            kok2=df[code]
        Nav = df[code]
        ite = 0
        for dat in iter(date_object):
            val = Nav.last(dat)
            val = val.dropna()
            if (dat=="180d") & (val.std()>1):
                #print(Nav)
                select_pct.append(np.sum(val.pct_change().values[1:]))
                #select.append(code)
                if ((np.sum(Nav.last("8d").dropna().pct_change().values[1:])<0.0) 
                    and (np.sum(val.pct_change().values[1:])>0.09 ) 
                    and (np.sum(Nav.last("360d").dropna().pct_change().values[1:])>0.18 )
                    and (np.sum(Nav.last("720d").dropna().pct_change().values[1:])>0.20 )):
                    #print(code)
                    iden = mf.get_scheme_details(code)
                    print(iden['scheme_name'])
                    select.append(iden['scheme_name'])
            if len(val)<1:#val[0]==0:
                print(code)
                New_scheme.append(code)
            else:
                Val[ite_code,ite] = wei[ite]*(val[-1]-val[0])/val[0]
            
            #print(Val[0,ite])
            if np.isnan(Val[ite_code,ite]):
                Val[ite_code,ite] = 0.0
            #if Val[ite_code,0] == 0.0:
            #    print(code)
            #    tt = code
           
            
            ite = ite+1
        #df2 = pd.DataFrame({code: rank_mat }, index = date_object)
        #df = pd.concat([df, df2], axis=1, sort=False)
        #Val_d = np.concatenate((Val_d,Val),axis=0)
        ite_code = ite_code+1
        Cod.append(code)        
#Cod = Cod[1:]
np.max(Val,axis=0)
df = pd.DataFrame({date_object[0]: Val[:len(Cod),0],
                   date_object[1]: Val[:len(Cod),1], 
                   date_object[2]: Val[:len(Cod),2],
                   date_object[3]: Val[:len(Cod),3], 
                   date_object[4]: Val[:len(Cod),4],
                   date_object[5]: Val[:len(Cod),5], 
                   date_object[6]: Val[:len(Cod),6]}, index = Cod) 
df.to_pickle('NAV_feat')
df.to_excel("1.xls")

df2 = pd.DataFrame({Cod[0]: Val[0,:]},index = date_object)
for i in tqdm(range(len(Cod)-1)):
    df = pd.DataFrame({Cod[i+1]: Val[i+1,:]},index = date_object)
    df2 = pd.concat([df2, df], axis=1, sort=False)
df2.to_pickle('NAV_feat_T')
#df2.to_excel("2.xls")
Index = np.mean(Val[:,1:5],axis=1)>0.15
#Index2 = ((Val[:,0]-Val[:,1])/Val[:,1])<0
#Criter = np.and(Index,Index2)
