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

# shift = np.min(signal)
#
#signal -= shift

discret_tool = 'linear'

elements = np.array([5, 10, 15, 20, 25, 30])

error_mean = np.zeros(len(elements))
error_linear = np.zeros(len(elements))
error_spline = np.zeros(len(elements))

#elements = 10

for j in range(len(elements)):

    h = len(signal) // elements[j]

    #print(h)

    mean_signal = np.zeros((len(signal), 1))

    linear_signal = np.zeros((len(signal), 1))

    spline_signal = np.zeros((len(signal), 1))

    aux = np.zeros((len(signal),))

    c_y = np.zeros(elements[j])  #valor central dos elementos
    c_x = np.zeros(elements[j])  #posicao central dos elementos


#if discret_tool == 'mean':

    for i in range(elements[j]):
        mean_signal[i * h:i * h + h] = np.average(signal[i * h:i * h + h])
        c_x[i] = i * h + h / 2
        c_y[i] = mean_signal[i * h]

#if discret_tool == 'linear':

    for i in range(elements[j]):


        if i * h + h == len(signal):
            coefs = np.polyfit(np.linspace(i * h, i * h + h - 1, h - 1), signal[i * h:i * h + h - 1], 1)

            aux[i * h:i * h + h] = np.polyval(coefs, np.linspace(i * h, i * h + h, h))

            delta = c_y[i] - aux[i * h + int(h / 2)]

            aux += delta

            #print(delta)

            linear_signal[i * h:i * h + h] = aux[i * h:i * h + h].reshape(h, 1)

            break

        coefs = np.polyfit(np.linspace(i * h, i * h + h, h), signal[i * h:i * h + h], 1)

        aux[i * h:i * h + h] = np.polyval(coefs, np.linspace(i * h, i * h + h, h))

        delta = c_y[i] - aux[i * h + int(h / 2)]

        aux += delta

        linear_signal[i * h:i * h + h] = aux[i * h:i * h + h].reshape(h, 1)

#        
#    linear_signal[i*h:i*h+h] = np.linspace(signal[i*h], signal[i*h+h], h).reshape(h,1)

    cs = interpolate.CubicSpline(c_x, c_y)

    for i in range(elements[j]):
        spline_signal[i * h:i * h + h] = cs(np.linspace(i * h, i * h + h, h)).reshape(h, 1)

    E_mean = np.zeros(len(signal))
    E_linear = np.zeros(len(signal))
    E_spline = np.zeros(len(signal))

    for i in range(len(signal)):

        E_mean[i] = ((mean_signal[i] - signal[i])/signal[i])
#E_mean = np.average(abs((mean_signal-signal)/signal))

        E_linear[i] = ((linear_signal[i] - signal[i])/signal[i])
#E_linear = np.average(abs((linear_signal - signal)/signal))

        E_spline[i] = ((spline_signal[i] - signal[i])/signal[i])
#E_spline = np.average(abs((spline_signal - signal)/signal))


    error_mean[j] = np.sqrt(np.mean(np.square(E_mean)))
    error_linear[j] = np.sqrt(np.mean(np.square(E_linear)))
    error_spline[j] = np.sqrt(np.mean(np.square(E_spline)))


"""""
plt.figure()
#plt.close('all')
plt.subplot(211)
plt.plot(signal, '-b', label='reference signal')
plt.plot(mean_signal, '-r', label='average signal')
plt.plot(linear_signal, '-g', label='linear signal')
plt.plot(spline_signal, '-m', label='spline signal')
plt.plot(c_x, c_y, '*k')
plt.subplot(212)
#plt.plot(elements, E_mean, '*r', label='average signal error')
#plt.plot(elements, E_linear, '*g', label='linear signal error')
#plt.plot(elements, E_spline, '*m', label='spline signal error')
plt.plot(E_mean, 'r', label='average signal error')
plt.plot(E_linear, 'g', label='linear signal error')
plt.plot(E_spline, 'm', label='spline signal error')
#plt.subplot(313)
plt.show()
"""""

# análise de convergência

plt.plot(error_mean, 'r', label='average signal error')
plt.plot(error_linear, 'g', label='linear signal error')
plt.plot(error_spline, 'm', label='spline signal error')
plt.show()
