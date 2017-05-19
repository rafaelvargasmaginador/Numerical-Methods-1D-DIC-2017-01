#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 19:26:52 2017

@author: vfsciuti
        
"""
# importing libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from detect_peaks import detect_peaks
### Functions


def auto_correlate(sinal, show = False):
    
     CSign = np.correlate(sinal,sinal, 'same') #multipliquei por -1 meramente para ver minimos
     
     
     SignPeaks = detect_peaks(CSign) #encontra os vales
     
     MinPeak = np.argmax(CSign[SignPeaks]) #encontra o menor vale entre os vales
     
     inip = int(SignPeaks[MinPeak] - (SignPeaks[MinPeak] - SignPeaks[MinPeak-1])/2)
     
     endp = int(SignPeaks[MinPeak] + (SignPeaks[MinPeak+1] - SignPeaks[MinPeak])/2)
     
     
     
     SignSample = CSign[inip:endp]
     
     XSample = np.arange(inip,endp)
     
     #estimate mean and standard deviation 
     
     aux = np.arange(SignSample.size)
     mean = np.sum(aux*SignSample)/np.sum(SignSample)
     sigma = np.sqrt(np.abs(np.sum((aux-mean)**2*SignSample)/np.sum(SignSample)))
     
     print(mean)
     
     print(sigma)
     
     def GaussFun(x,a,x0,sigma):
         return a*np.exp(-(x-x0)**2/(2.0*sigma**2))
     
        
     from scipy.optimize import curve_fit
     
     popt,pcov = curve_fit(GaussFun,XSample,SignSample,p0=[1,mean,sigma])
     
            
     plt.subplot(211)
     plt.plot(sinal,'-b', label = 'reference signal')
     plt.subplot(212)
     plt.plot(CSign,'-r', label = 'cross-correlated signal')
     plt.plot(SignPeaks, CSign[SignPeaks], '*k')
     plt.plot(XSample,SignSample,'g')
     plt.plot(XSample,GaussFun(XSample,popt[0], popt[1], popt[2]), 'm')
     
     plt.show()
     
    
### Main

SourceFile = 'signalexample.txt'

sinal = np.genfromtxt(SourceFile)

shift = np.min(sinal)

sinal -= shift

auto_correlate(sinal)

