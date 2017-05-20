# Rotina de teste para a funcao abq2img

from abq2img_1D import abq2img
import numpy as np


imgsignal =np.loadtxt('signalexample.txt')
abqoutput =np.loadtxt('abqoutputexample.txt')
#abqoutput[:,1] = np.linspace(0,0.5,11) #Simula tracao

newsig = abq2img(imgsignal,abqoutput)

import matplotlib.pyplot as plt
plt.plot(imgsignal,'r--')
plt.plot(newsig,'b--')
plt.show()
