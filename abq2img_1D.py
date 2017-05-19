# Funcao para deformar um signal 1D com base em um modelo de viga 1D do Abaqus
# 
# Caiua

# O funcionamento e baseado na deformacao de trechos do sinal de entrada 
#  conforme a deformacao calculada com o modelo de elementos finitos

# Parametros de entrada:
#  imgsignal: sinal de entrada (nao deformado)
#  abqoutput: saida do elementos finitos 
#             (Array de coordenada dos nos por deslocamento)
# Saida:
#  newsignal: sinal deformado segundo o modelo de elementos finitos  


import numpy as np

def abq2img(imgsignal,abqoutput):
    nodes = abqoutput[:,0]                               # Coordenadas dos nos
    u = abqoutput[:,1]                                   # Deslocamento nos
    pixelsperelem = int(len(imgsignal)/(len(nodes)-1))   # Pixels por elemento do sinal de entrada
    newsignal = np.zeros(imgsignal.shape)                # Sinal deformado (iniciali.)   
    positionnew=0                                        # Varialvel de posicao no sinal de saida
    for i in range(0,len(nodes)-1):
        strain = (u[i+1] - u[i])/(nodes[i+1]-nodes[i])
        scalefactor = (1+strain)
        newpixelsperelement = int(pixelsperelem*scalefactor)
        position = i*pixelsperelem                               # Varialvel de posicao no sinal de entrada
        # Interpolacao do sinal
        x = np.linspace(0,1,pixelsperelem)
        y = imgsignal[position:position+pixelsperelem]
        xnew = np.linspace(0,1,newpixelsperelement)
        ynew = np.interp(xnew, x, y)
        h = len(xnew)
        newsignal[positionnew:positionnew+newpixelsperelement] =  ynew
        positionnew +=h
    return newsignal

