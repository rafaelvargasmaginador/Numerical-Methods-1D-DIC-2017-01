#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 19:11:57 2017

@author: vfsciuti
        
"""
# importing libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


### Functions

### Main

SourceFile = 'signalexample.txt'

signal = np.genfromtxt(SourceFile)

#shift = np.min(signal)
#
#signal -= shift

discret_tool = 'linear'

elements = 10

h = len(signal) // elements

print(h)

mean_signal = np.zeros((len(signal),1))

linear_signal = np.zeros((len(signal),1))

spline_signal = np.zeros((len(signal),1))

aux = np.zeros((len(signal),))

c_y = np.zeros(elements) #valor central dos elementos
c_x = np.zeros(elements) #posicao central dos elementos


#if discret_tool == 'mean':
    
for i in range(elements):
    mean_signal[i*h:i*h+h] = np.average(signal[i*h:i*h+h])
    c_x[i] = i*h+h/2
    c_y[i] = mean_signal[i*h]
        
#if discret_tool == 'linear':
    
for i in range(elements):
    
    
    if  i*h+h == len(signal):
        
        
        coefs = np.polyfit(np.linspace(i*h,i*h+h-1,h-1), signal[i*h:i*h+h-1],1)
    
    
        aux[i*h:i*h+h] = np.polyval(coefs, np.linspace(i*h,i*h+h,h))
        
        delta = c_y[i] - aux[i*h+int(h/2)] 
        
        aux += delta
        
        print(delta)
        
        linear_signal[i*h:i*h+h] = aux[i*h:i*h+h].reshape(h,1)
    
        
        break
    
    coefs = np.polyfit(np.linspace(i*h,i*h+h,h), signal[i*h:i*h+h],1)
    
    
    aux[i*h:i*h+h] = np.polyval(coefs, np.linspace(i*h,i*h+h,h))
    
    delta = c_y[i] - aux[i*h+int(h/2)] 
    
    aux += delta
    
    linear_signal[i*h:i*h+h] = aux[i*h:i*h+h].reshape(h,1)
    
#        
#    linear_signal[i*h:i*h+h] = np.linspace(signal[i*h], signal[i*h+h], h).reshape(h,1)

cs = interpolate.CubicSpline(c_x, c_y)

for i in range(elements):
    
            
    spline_signal[i*h:i*h+h] = cs(np.linspace(i*h,i*h+h,h)).reshape(h,1)


E_mean = np.average(abs((mean_signal-signal)/signal))

E_linear = np.average(abs((linear_signal - signal)/signal))

E_spline = np.average(abs((spline_signal - signal)/signal))

plt.subplot(211)
plt.plot(signal,'-b', label = 'reference signal')
plt.plot(mean_signal,'-r', label = 'average signal')
plt.plot(linear_signal,'-g', label = 'linear signal')
plt.plot(spline_signal,'-m', label = 'spline signal')
plt.plot(c_x,c_y,'*k')
plt.subplot(212)
plt.plot(elements, E_mean,'*r', label = 'average signal error')
plt.plot(elements, E_linear,'*g', label = 'linear signal error')
plt.plot(elements, E_spline,'*m', label = 'spline signal error')
