"""
13/06/2017

"""
# importing libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

SourceFile = 'signalexample.txt'

signal = np.genfromtxt(SourceFile)

def discre_signal(signal,elements,type):

    if (len(signal)%elements)==0:
        print('We will take elements = elements+1. Thank you for your comprehension! :)' )
        elements += 1
    h = len(signal) // elements
    aux = np.zeros((len(signal),))

    c_y = np.zeros(elements+1)  #valor dos nós
    c_x = np.zeros(elements+1)  #posicao dos nós

    disc_signal = np.zeros((len(signal)))
    error = np.zeros(len(signal))

    if type == 1:

        for i in range(elements+1):
            disc_signal[i * h:i * h + h] = np.average(signal[i * h:i * h + h])
            c_x[i] = i * h
            c_y[i] = disc_signal[i * h]

    elif type == 2:

        for i in range(elements):

            if i * h + h == len(signal):
                coefs = np.polyfit(np.linspace(i * h, i * h + h - 1, h - 1), signal[i * h:i * h + h - 1], 1)

                aux[i * h:i * h + h] = np.polyval(coefs, np.linspace(i * h, i * h + h, h))

                disc_signal[i * h:i * h + h] = aux[i * h:i * h + h].reshape(h)

                break

            coefs = np.polyfit(np.linspace(i * h, i * h + h, h), signal[i * h:i * h + h], 1)

            aux[i * h:i * h + h] = np.polyval(coefs, np.linspace(i * h, i * h + h, h))

            disc_signal[i * h:i * h + h] = aux[i * h:i * h + h].reshape(h)

    elif type == 3:

        for i in range(elements+1):
            c_x[i] = i * h
            c_y[i] = signal[i * h]

        cs = interpolate.CubicSpline(c_x, c_y)

        for i in range(elements):
            disc_signal[i * h:i * h + h] = cs(np.linspace(i * h, i * h + h, h)).reshape(h)

    error = ((disc_signal - signal) / signal)
    #error_rms = np.sqrt(np.mean(np.square(error)))

    return disc_signal,error

elements = 13

[test1,a] = discre_signal(signal,elements,1)
[test2,b] = discre_signal(signal,elements,2)
[test3,c] = discre_signal(signal,elements,3)

plt.figure(1)
plt.subplot(311)
plt.plot(test1,'.b')
plt.plot(signal,'r')
plt.subplot(312)
plt.plot(test2,'.b')
plt.plot(signal,'r')
plt.subplot(313)
plt.plot(test3,'.b')
plt.plot(signal,'r')
plt.show()
