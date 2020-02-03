# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 10:28:03 2020

@author: admin
"""

import numpy as np
from mftool import Mftool
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
#import matplotlib.dates
from functools import reduce
from tqdm import tqdm
import requests
import json

url_temp = "https://api.mfapi.in/mf/"


def fetch_history(scheme_code):
    """Fetch History for given scheme_code"""
    # make the url
    url = url_temp + scheme_code

    # get data from the url
    r = requests.get(url)
    val = json.loads(r.content)
    hist_data = val['data']

    # historic comments # TOOD: look at these later
    # #name = val['meta']
    # #name = name['scheme_name']
    # # q = mf.get_scheme_quote(codes[0]) # it's ok to use both string or integer as codes.

    dates = [x['date'] for x in hist_data]
    date_object = [
        datetime.strptime(date, '%d-%m-%Y').date() for date in dates
    ]

    date_object = pd.to_datetime(date_object, format='%Y-%m-%d')
    values = [float(x['nav']) for x in hist_data]

    scheme_df2 = pd.DataFrame({str(scheme_code): values}, index=date_object)
    #scheme_df  = pd.Series(values , index = date_object)

    # pickle the data
    scheme_df2.to_pickle('data/' + scheme_code)
    return scheme_df2


def screen_feat(Nav_hist):
    #Nav_hist = fetch_history(code)
    temp = Nav_hist.resample('d').mean()
    time_delta = ['1M', '3M', '6M', '12M', '36M', '60M']
    ##weig = np.array([12*5, 4*3, 2*1.5, 1, 0.333, 0.2])
    weig = np.array([12, 4, 2, 1, 0.333, 0.2])
    i = 0
    weeks = np.zeros([len(time_delta)])
    value = np.zeros([len(time_delta)])
    per_value = np.zeros([len(time_delta)])
    for iter in time_delta:
        tt = temp.last(iter)
        # print(iter)
        # print(tt.size)
        weeks[i] = tt.shape[0]
        value[i] = tt.mean().values
        # print(np.sum(tt.pct_change().values[1:]))
        # *np.float(weig[i])#/np.float(iter[0])
        per_value[i] = np.sum(tt.pct_change().values[1:])
        if np.isnan(per_value[i]):
            weeks[i] = weeks[i-1]
            value[i] = value[i-1]
            per_value[i] = per_value[i-1]
        i = i+1
    #reward = np.sum(per_value)
    return per_value


mf = Mftool()
schemes = mf.get_scheme_codes()
codes = list(schemes.keys())
schemes_df = pd.DataFrame(
    {'Name': list(schemes.values()), 'Code': list(schemes.keys())})
schemes_df.to_pickle('Schemes')
#schemes_df.set_index('Name', inplace=True)
rank_mat = np.zeros([len(codes), 7])

scheme_idx = len(codes)-1
code = codes[scheme_idx]
df = fetch_history(code)

for scheme_idx in tqdm(range(100)):
    code = codes[scheme_idx]
    df2 = fetch_history(code)
    ##df = pd.concat([df, df2], axis=1, sort=False)
    #feature = screen_feat(df2)
    #rank_mat[scheme_idx,0] = scheme_idx
    #rank_mat[scheme_idx,1:] = feature

#scheme_df2 = pd.DataFrame({ 'Name': list(schemes.values()), 'Code': codes ,'Feature':rank_mat[:,1:]})
# scheme_df2.to_excel("1.xls")
#df2 = pd.DataFrame({'Feature':rank_mat[:,1:]},index=codes )
# df2.to_pickle('Nav_Features')
