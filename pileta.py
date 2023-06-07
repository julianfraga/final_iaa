# -*- coding: utf-8 -*-
"""
Created on Mon May 29 14:02:12 2023

@author: Usuario
"""

import pandas as pd
import os
os.chdir(r'D:/Documentos/UNSAM/Materias/IAA/final_iaa')
archivo = 'selldocs.tsv'

df = pd.read_csv(archivo, decimal = ',', sep='\t')
df.head()
columnas = list(df.columns)
columnas_lower = [columna.lower().replace(' ','_') for columna in columnas]
columnas_lower[-1] = 'total_rate'
columnas_lower[8] = 'avg_views'
rename_dic = {columnas[i]:columnas_lower[i] for i in range(len(columnas))}

df.rename(columns = rename_dic, inplace=True)
vistas = list(df['avg_views'].unique())

def corregir_numero(valor):
    if type(valor)!=str:
        return valor
    if '.' in valor:
        partes = valor.split('.')
        if len(partes) == 2 and partes[1].isdigit():
            return int(partes[0] + partes[1])
        elif len(partes) == 3 and partes[2].isdigit():
            return int(partes[0] + partes[1]+partes[2])
    return valor

df['likes'] = pd.to_numeric(df['likes'].apply(corregir_numero), errors ='coerce')
df['views'] = pd.to_numeric(df['views'].apply(corregir_numero), errors ='coerce')
df['comments'] = pd.to_numeric(df['comments'].apply(corregir_numero), errors ='coerce')
df['times_shared'] = pd.to_numeric(df['times_shared'].apply(corregir_numero), errors ='coerce')

#%%
import numpy as np
def formato(string):
       
    if type(string) != str:
        banderin = False

    elif 'Integration' in string:
        banderin = False


    elif '>1K' in string:
        banderin = False


    elif '?' in string:
        banderin = False
        
    elif 'Organic' in string:
        banderin = False
    else:
        banderin = True
      
    if banderin:
        string_split = string.split(sep = '-')
   
        if len(string_split) != 2:
            banderin = False
    
        string_format = []
        for i, item in enumerate(string_split):
            string_format.append(item.strip(' kK'))
            
            #excepciones
            if '800' in string_format[i]:
                string_format[i] = '0.8'
            if string_format[i] == '':
                string_format[i] = '0'
            if not string_split[i]:
                banderin = False
                
    if banderin == False:
        string_format = [-1, -1]
        
    return (string_format) 

def formatear_categorias(df, vistas):
    diccionario_categorias = {}
    for categoria in vistas:
        if type(categoria) != str:
            continue
        
        elif 'Integration' in categoria:
            continue
    
    
        elif '>1K' in categoria:
            continue
    
    
        elif '?' in categoria:
            continue
            
        elif 'Organic' in categoria:
            continue
        elif formato(categoria):
            if '-800' in categoria:
                categoria_format = 400
                
            else:
                
                categoria_format = 1000*np.mean([float(formato(categoria)[0]), float(formato(categoria)[1])])

            diccionario_categorias[categoria] = categoria_format
            
            
    return(diccionario_categorias)
        
#

# for index, fila in df.iterrows():
#     vistas = fila.avg_views


df['avg_views_num'] = 0
# df.rename(columns = {'#ad_#sponsored_or_any_type_of_sponsored_hashtag':'#ad'}, inplace=True)
for index, fila in df.iterrows():
    diccionario = formatear_categorias(df['avg_views'], vistas)
    categoria = df.at[index,'avg_views']
    if categoria in diccionario.keys():
        df.at[index,'avg_views_num']=diccionario[categoria]
    if df.at[index,'#ad'] in ['Yes', 'yes']:
        df.at[index,'#ad'] = True
    else:
        df.at[index,'#ad'] = False
    if np.isnan(df.at[index,'comments']):
        df.at[index,'comments'] = 0
    if np.isnan(df.at[index,'views']):
        df.at[index,'views'] = 0
    if np.isnan(df.at[index,'times_shared']):
        df.at[index,'times_shared'] = 0
    if np.isnan(df.at[index,'likes']):
        df.at[index,'likes'] = 0
        
df = df[df['avg_views_num']>=0]
#%%

features = ['platform','avg_views_num','#ad','#studypool']
views_ad = df['views']
likes_ad = df['likes']
shares_ad = df['times_shared']
comments_ad = df['comments']
df['engagement'] = (likes_ad+shares_ad+comments_ad)/views_ad
target = df['engagement']
features = df[features]
#%%
from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler

features_train, features_test, target_train, target_test = tts(features, target, test_size=0.33)
regresor = LogisticRegression()
regresor.fit(features_train, target_train)
predicciones_train = regresor.predict(features_test)