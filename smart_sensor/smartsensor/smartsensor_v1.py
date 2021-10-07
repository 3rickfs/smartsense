#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programm to train multilinear regretion model for the smart sensor


Created on Sat Feb  6 16:26:10 2021

@author: erickmfs
"""


# In[1]:
# *Load necessary libraries*

import numpy as np
import matplotlib.pyplot as plt
import random


# In[2]:
# Variables

Ab = 991.67
Bb = -28.33
Ar = -736.67
Br = 28.33

MaxB = 35.0
MinB = 26.0
MaxR = 35.0
MinR = 26.0

# In[3]:
# Generate our data
noise = np.array([random.randrange(-10,10) for i in range(100)])
data_x_b = np.linspace(MinB, MaxB, 100)
data_y_b = Bb * data_x_b + Ab + noise
noise = np.array([random.randrange(-10,10) for i in range(100)])
data_x_r = np.linspace(MinR, MaxR, 100) #[:, np.newaxis]
data_y_r = Br * data_x_r + Ar + noise

#Ploting synthetic data

plt.figure(figsize=(10,10))
#fig, axs = plt.subplots(2)
#fig.figure(figsize=(20,20))
#fig.suptitle('Data')
#axs[0].scatter(data_x_b,data_y_b)
#axs[1].scatter(data_x_r,data_y_r)

plt.scatter(data_x_b,data_y_b)
plt.scatter(data_x_r,data_y_r)

plt.show()

#Transverse
data_x_b = data_x_b[:, np.newaxis]
data_y_b = data_y_b[:, np.newaxis]
data_x_r = data_x_r[:, np.newaxis]
data_y_r = data_y_r[:, np.newaxis]

# In[4]:
# Add intercept data and normalize

model_order = 2
data_x_b = np.power(data_x_b, range(model_order))
max_x_b = np.max(data_x_b, axis=0)
print("Max value in data x for blue: " + str(max_x_b))
data_x_b /= max_x_b

data_x_r = np.power(data_x_r, range(model_order))
max_x_r = np.max(data_x_r, axis=0)
print("Max value in data x for red: " + str(max_x_r))
data_x_r /= max_x_r


# In[5]:
# Shuffle data and produce train and test sets

order = np.random.permutation(len(data_x_b))
portion = 20
test_x_b = data_x_b[order[:portion]]
test_y_b = data_y_b[order[:portion]]
test_x_r = data_x_r[order[:portion]]
test_y_r = data_y_r[order[:portion]]

train_x_b = data_x_b[order[portion:]]
train_y_b = data_y_b[order[portion:]]
train_x_r = data_x_r[order[portion:]]
train_y_r = data_y_r[order[portion:]]


# In[6]:
# Create gradient function

def get_gradient(w, x, y):
    y_estimate = x.dot(w).flatten()
    error = (y.flatten() - y_estimate)
    mse = (1.0/len(x))*np.sum(np.power(error, 2))
    gradient = -(1.0/len(x)) * error.dot(x)
    return gradient, mse



# In[7]:
# Perform gradient descent to learn model

tolerance = 1e-5
decay = 0.99
batch_size = 10
    
# Perform Stochastic Gradient Descent
for i in range(2):
    alpha = 0.5
    epochs = 1
    iterations = 0
    if i == 1: train_x = train_x_b; train_y = train_y_b; test_x = test_x_b; test_y = test_y_b; w = np.random.randn(model_order)
    if i == 0: train_x = train_x_r; train_y = train_y_r; test_x = test_x_r; test_y = test_y_r; w = np.random.randn(model_order)
    while True:
        order = np.random.permutation(len(train_x))
        train_x = train_x[order]
        train_y = train_y[order]
        b=0
        while b < len(train_x):
            tx = train_x[b : b+batch_size]
            ty = train_y[b : b+batch_size]
            gradient = get_gradient(w, tx, ty)[0]
            error = get_gradient(w, train_x, train_y)[1]
            w -= alpha * gradient
            iterations += 1
            b += batch_size
        
        # Keep track of our performance
        if epochs%100==0:
            new_error = get_gradient(w, train_x, train_y)[1]
            print("Epoch: %d - Error: %.4f" %(epochs/100, new_error))
        
            # Stopping Condition
            if abs(new_error - error) < tolerance:
                print("Converged.")
                break
            
        alpha = alpha * (decay ** int(epochs/1000))
        epochs += 1
    
    print("w =",w)
    print("Test Cost =", get_gradient(w, test_x, test_y)[1])
    print("Total iterations =", iterations)
    
    
    
    # In[8]:
    # Plot the model obtained
    
    y_model = np.polyval(w[::-1], np.linspace(0,1,100))
    plt.plot(np.linspace(0,1,100), y_model, c='g', label='Model')
    plt.scatter(train_x[:,1], train_y, c='b', label='Train Set')
    plt.scatter(test_x[:,1], test_y, c='r', label='Test Set')
    plt.grid()
    plt.legend(loc='best')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(0,1)
    plt.show()
    
    
    
