# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 12:19:16 2023

@author: Seba 
"""
import pandas as pd
import numpy as np
import matplotlib as plt

#%% DF's 
sell_docs = pd.read_excel('./Sell docs 2022.xlsx', sheet_name = None, decimal = ',')
lead_gen = pd.read_excel('./Lead Generation.xlsx', sheet_name = None, decimal = ',')
#%% Limpieza de df_lead_gen

#Saco una sheet que no sirven
del lead_gen['Pinterest']

def renombrar(diccionario, nombre_columna, nuevo_nombre): 
    '''Recorre el diccionario con los datasets y corige los nombres de las columnas'''
    for nombre_dataframe, dataframe in diccionario.items():
        if nombre_columna in dataframe.columns:
            dataframe.rename(columns={nombre_columna: nuevo_nombre}, inplace=True)
            
#%% #Renombrando 

renombrar(lead_gen, 'Reels AVG views', 'Avg Views') 
renombrar(lead_gen, 'Total IG Followers', 'Total Subs / Followers') 
renombrar(lead_gen, 'Total Followers', 'Total Subs / Followers') 
renombrar(lead_gen, 'Est Avg Views Per Reel', 'Avg Views')
renombrar(lead_gen, 'Target Niche \nGroup', 'Target Niche')
renombrar(lead_gen, 'Est Avg Views Per Video', 'Avg Views')

#%% Armando el Dataset con todos 
# Concatenar los dataframes desde el diccionario 
df_lead_gen = pd.concat(lead_gen.values(), ignore_index = True)

#Sacando los valores faltantes 
df_lead_gen = df_lead_gen.dropna(axis = 0, how = 'all')

#busco las columnas de mas 
df_lead_gen.columns

#Sacando las columnas que no interesan 
df_lead_gen = df_lead_gen.drop(['LinkedIn','Other platforms', 'Other platforms.1',
                                'Phone/ Whatsapp/ TM', 'Added By:', 'Phone / SMS', 'Notes',
                                'Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14', 'Date', 'Notes.1',
                                'Re-Scrape', 'Re-Scrape Value', 'Added to Email Failed Campaign',
                                'Re-scraped email', 'Unnamed: 11', 'Unnamed: 10', 'Re-scraped Email',
                                'Re-scraped IG', 'Whats/Tele', 'Wha/Tele', 'Phone / Whatsapp/TM',
                                'Facebook', 'IG / Twitter', 'Website (Contact Form)', 'Instagram',
                                'Twitter', 'Whatsapp / Telegram', 'Unnamed: 16',
                                'Unnamed: 17', 'Unnamed: 18','Unnamed: 19','Comment on YouTube',
                                'Lead '], axis = 1)

#Busco duplicados 
filas_duplicadas = df_lead_gen.duplicated()
df_lead_gen.drop_duplicates(keep = 'first', inplace = True)

#Valores faltantes 
Faltantes = df_lead_gen.isna().sum()
#URL                           9
#Username                     25
#Target Niche               1178
#Relevant Service           1398 sale
#Avg Views                   528 
#Total Subs / Followers     1542
#Email 1                    5758
#Email 2                   15262 
#IG                        10835 sale 
#TikTok                    18015 sale


df_lead_gen = df_lead_gen.drop(['TikTok', 'IG', 'Relevant Service'], axis = 1)

#Saco los valores faltantes de URL User 
df_lead_gen.dropna(['URL', 'Username'])

#%%
#Busco los que le faltan los 2 emails y los remuevo
sin_emails = df_lead_gen['Email 1'].isna() & df_lead_gen['Email 2'].isna()
sin_emails.sum()

df_lead_gen.drop(df_lead_gen[sin_emails].index, inplace = True)

#Guardado de archivo 
df_lead_gen.to_csv('./df_lead_gen.csv', index=False)

















