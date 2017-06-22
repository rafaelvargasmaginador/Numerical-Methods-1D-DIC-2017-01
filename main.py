
import numpy as np
import matplotlib.pyplot as plt
from framework import discre_signal, abq2img, correlate1D2 

nbscales = 7
# Sinal de entrada
SourceFile = 'signalexample.txt'
signal = np.genfromtxt(SourceFile)
# Gerando o signal deformado
numnodes=2**(8-1) + 1
abqoutput = np.zeros((numnodes,2))
abqoutput[:,0] = np.linspace(0,1,numnodes) #Simula tracao
#abqoutput[:,1] = np.linspace(0,-0.1,numnodes) #Simula tracao
abqoutput[:,1] = np.sin(np.linspace(0,2*np.pi,numnodes))*0.05
def_signal = abq2img(signal, abqoutput)
ROI = [0.1,0.7]

res,residual = correlate1D2(signal,def_signal,roi = ROI, nbscales=nbscales, guess=[0.03, -0.05])


nodes = np.linspace(ROI[0], ROI[1], numnodes)
plt.figure()
plt.plot(residual,'--om')
#plt.show()

plt.figure()
[garb_res, a] = discre_signal(def_signal, res+nodes, 1)
plt.grid('on')
plt.plot(garb_res,'.r')
plt.plot(def_signal,'--r')


[garb, a] = discre_signal(signal, nodes, 1)
#plt.figure()
plt.plot(garb,'.b')
plt.plot(signal,'--b')
#plt.show()

plt.figure()
plt.plot(nodes,np.sin(np.linspace(ROI[0]*2*np.pi,ROI[1]*2*np.pi,numnodes))*0.05,'--b')
plt.plot(nodes,res,'ob')
plt.show()

