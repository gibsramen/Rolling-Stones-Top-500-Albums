#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 14:26:20 2017

@author: gibraanrahman
"""

import discogs_client as dc
import pandas as pd
import re
import time

ds = dc.Client('my_user_agent/1.0', user_token='sXNIMzBirlRelkfFxITBKIIMjFYQTSQgNgVeFMio')
d = pd.read_csv('albumlist2.csv', encoding='latin10')

# 240 requests/min
# need to go piecewise
def getGenresAndStyles(num):
    print(num+1)
    search_query = d['Album'][num] + ' ' + d['Artist'][num]
    results = ds.search(search_query, type = 'master')
    try:
        master = results[0]
    except IndexError:
        genres_list.append(['?'])
        styles_list.append(['?'])
        error_list.append(d['Album'][num])
        print(d['Album'][num])
        return
    id = master.id
    genres = ds.master(id).genres
    styles = ds.master(id).styles
    genres_list.append(genres)
    styles_list.append(styles)

# if >1 genres/styles
# turn into list of strings
def parseList(u_list):
    n_list = []
    for y in range(0, len(u_list)):
        content = re.sub(r"(\[\')|(\'\])|(\')", "", str(u_list[y]))
        n_list.append(content) 
    return n_list

genres_list = []
styles_list = []
error_list = []

for i in range(0, 500):
    getGenresAndStyles(i)
    if (i+1) % 75 == 0:
        time.sleep(60)
    else:
        continue

g_df = pd.DataFrame(parseList(genres_list))
s_df = pd.DataFrame(parseList(styles_list))

g_df.to_csv('genres.csv')
s_df.to_csv('styles.csv')






