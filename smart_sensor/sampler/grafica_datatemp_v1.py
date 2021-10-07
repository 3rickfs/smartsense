# -*- coding: utf-8 -*-
"""
Mostrar valores de temperatura obtenidos en gráficas

Created on Sun Mar 28 08:37:49 2021

@author: Erick Fiestas
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import csv

datafilepath = r'C:\Users\hjara\OneDrive\IA apps\xubuntu\ai_apps\projects\smart_sensor\sampler\csvfiles'

tempdata = []
dicc_tempe = {'caliente': 1, 'frio': 0}
estimacion = []

for folder in os.listdir(datafilepath):
    if folder == 'caliente' or folder == 'frio':
        npath = os.path.join(datafilepath,folder)
        for archivo_csv in os.listdir(npath):
            filepath = os.path.join(npath,archivo_csv)
            i = 0
            with open(filepath, 'r') as csvfile:
                csvReader = csv.reader(csvfile, delimiter=',')
                for row in csvReader:
                    if i>0: 
                        tempdata.append(float(row[0]))
                        estimacion.append(dicc_tempe[folder])
                    #if i>0: print(row[0])
                    i += 1
            
tempdata = np.array(tempdata)
estimacion = np.array(estimacion)

plt.figure(figsize = (10,6))
plt.scatter(estimacion, tempdata)
plt.xlabel('0-frio / 1-caliente') , plt.ylabel('Temperatura (°C)')

        
            
            
            
            
            
            