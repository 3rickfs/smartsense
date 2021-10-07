# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 09:28:33 2021

@author: Erick Fiestas
"""
# In[1]:
# *Load necessary libraries*

import numpy as np
import matplotlib.pyplot as plt
import random


# In[2]:
# Variables

Ab = 1115.6
Bb = -31.9
Ar = -860.6
Br = 31.9

MaxB = 35.0
MinB = 27.0
MaxR = 35.0
MinR = 27.0

# In[2]:
# Generate our data
noise = np.array([random.randrange(-10,10) for i in range(100)])
data_x_b = np.linspace(MinB, MaxB, 100)
data_y_b = Bb * data_x_b + Ab + noise
noise = np.array([random.randrange(-10,10) for i in range(100)])
data_x_r = np.linspace(MinR, MaxR, 100) #[:, np.newaxis]
data_y_r = Br * data_x_r + Ar + noise

#Ploting synthetic data
plt.figure(figsize=(10,10))
plt.scatter(data_x_b,data_y_b)
plt.scatter(data_x_r,data_y_r)

plt.show()