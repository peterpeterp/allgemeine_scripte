# -*- coding: utf-8 -*-
import os,sys,time
import pandas as pd

os.chdir('/Users/peterpfleiderer/Documents/Projects/Scripts/allgemeine_scripte')

table=pd.read_csv('SREX.csv',sep=';')

pkl_file = open('/Users/peterpfleiderer/Documents/Projects/Persistence/data/srex_dict.pkl', 'rb')
srex = pickle.load(pkl_file)	;	pkl_file.close()

srex={}
for name,i in zip(table.Code,range(len(table.Code))):
    if '*' not in name:
        tmp=list(table.loc[i])
        points=[]
        for pnt in tmp[4:]:
            if isinstance(pnt, float) == False:
                lonlat=pnt.split(' ')
                points.append(tuple([float(item) for item in lonlat if item not in ['']]))
        srex[name]={'points':points}

output = open('SREX.pkl', 'wb')
pickle.dump(srex, output)
output.close()
