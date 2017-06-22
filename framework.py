# -*- coding: utf-8 -*-
"""
# Framework de funções para a correlação

@author: aluno
"""
import numpy as np
from scipy import interpolate, optimize, interp

# Função erro
def error_func(nodes, g, nodes_values, ty):
    x_nodes = np.rint(len(g) * nodes)
    x_nodes = x_nodes.astype(int)
    # disc_signal = np.zeros((len(g)))
    Error = np.zeros(len(x_nodes) - 1)
    el_value = np.zeros(len(x_nodes) - 1)
    if ty == 1:
        for i in range(len(x_nodes) - 1):
            el_value[i] = np.average(g[x_nodes[i]:x_nodes[i + 1]])
            # disc_signal[nodes[i]:nodes[i+1]] = np.average(signal[nodes[i]:nodes[i+1]])
        Error = el_value - nodes_values
    return np.mean(np.abs(Error))


# Função erro
def error_func2(disp, nodes, f, g):
    print([nodes,disp])
    xf = np.rint(len(f) * nodes).astype(int)
    xg = xf + np.rint(len(g) * disp).astype(int)
    Error = np.zeros(len(xf) - 1)
    el_f = np.zeros(len(xf) - 1)
    el_g = np.zeros(len(xg) - 1)
    for i in range(len(xf) - 1):
        #el_f[i] = np.mean(np.abs(f[xf[i]:xf[i + 1]]
        #    -np.linspace(f[xf[i]],f[xf[i + 1]],len(f[xf[i]:xf[i + 1]])))/len(f[xf[i]:xf[i + 1]]))
        el_g[i] = np.mean(np.abs(g[xg[i]:xg[i + 1]]
            -np.linspace(g[xg[i]],g[xg[i + 1]],len(g[xg[i]:xg[i + 1]])))/len(g[xg[i]:xg[i + 1]]))
    return np.sum(np.square(el_g))

# Discretização do sinal
def discre_signal(signal, nodes, ty):
    x_nodes = np.rint(nodes * len(signal))
    x_nodes = x_nodes.astype(int)
    x_nodes[-1] += -1
    y_nodes = np.zeros(len(x_nodes))
    for i in range(len(x_nodes)):
        y_nodes[i] = signal[x_nodes[i]]
    h = np.diff(x_nodes)
    aux = np.zeros((len(signal),))
    disc_signal = np.zeros((len(signal)))
    element_value = np.zeros(len(x_nodes) - 1)

    if ty == 1:

        for i in range(len(x_nodes) - 1):
            element_value[i] = np.average(signal[x_nodes[i]:x_nodes[i + 1]])
            disc_signal[x_nodes[i]:x_nodes[i + 1]] = np.average(signal[x_nodes[i]:x_nodes[i + 1]])

    elif ty == 2:

        for i in range(len(x_nodes) - 1):
            coefs = np.polyfit(np.linspace(x_nodes[i], x_nodes[i + 1], h[i]), signal[x_nodes[i]:x_nodes[i + 1]], 1)

            aux[x_nodes[i]: x_nodes[i + 1]] = np.polyval(coefs, np.linspace(x_nodes[i], x_nodes[i + 1], h[i]))

            disc_signal[x_nodes[i]:x_nodes[i + 1]] = aux[x_nodes[i]:x_nodes[i + 1]].reshape(h[i])

    elif ty == 3:

        cs = interpolate.CubicSpline(x_nodes, y_nodes)

        for i in range(len(x_nodes) - 1):
            disc_signal[x_nodes[i]:x_nodes[i + 1]] = cs(np.linspace(x_nodes[i], x_nodes[i + 1], h[i])).reshape(h[i])

    disc_signal[0:x_nodes[0]] = np.nan
    disc_signal[x_nodes[-1]:len(signal)] = np.nan

    return disc_signal, element_value

# Deformar o sinal segundo um resultado de deslocamentos
def abq2img(imgsignal,abqoutput):
    nodes = abqoutput[:,0]                               # Coordenadas dos nos
    u = abqoutput[:,1]                                   # Deslocamento nos
    pixelsperelem = int(len(imgsignal)/(len(nodes)-1))   # Pixels por elemento do sinal de entrada
    newsignal = np.zeros(imgsignal.shape)                # Sinal deformado (iniciali.)   inal de saida
    start=0
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
        dh = newpixelsperelement
        end = start+dh
        if len(newsignal[start:]) > newpixelsperelement:
            end = start+dh
        else:
            dh=len(newsignal[start:])
            end = start+dh
        newsignal[start:end] =  ynew[:dh]
        start += dh 
    return newsignal



# Função de correlação
def correlate1D(refsignal, defsignal, roi= [0.1,0.9], nbscales = 5, guess = [0, 0.1]):
    residual = np.zeros([nbscales,1])
    for i in range(nbscales):
        print('Interação: ' + str(i))
        print('Chute: ' + str(guess))
        numnodes = 2**(i) + 1
        nodes = np.linspace(roi[0], roi[1], numnodes)
        [garbage, graylevelref] = discre_signal(refsignal, nodes, 1)
        result = optimize.fmin(error_func, guess, args=(defsignal, graylevelref, 1))
        [garbage, grayleveldef] = discre_signal(defsignal, result, 1)
        guess = None
        x = np.linspace(roi[0],roi[1],2**(i+1) + 1)
        guess = interp(x,nodes,result)
        residual[i] = np.mean(np.abs((grayleveldef-graylevelref)/graylevelref))
        print('Residuo: ' + str(residual[i]))
    return result,residual

# Função de correlação
def correlate1D2(signal, defsignal, roi= [0.1,0.9], nbscales = 5, guess = [0, 0.1]):
    residual = np.zeros([nbscales,1])
    for i in range(nbscales):
        print('Interação: ' + str(i))
        print('Chute: ' + str(guess))
        numnodes = 2**(i) + 1
        nodes = np.linspace(roi[0], roi[1], numnodes)
        print('Node == ' + str(nodes))
        result = optimize.fmin(error_func2, guess, args=(nodes, signal, defsignal))
        residual[i] = error_func2(result, nodes, signal, defsignal)
        guess = None
        x = np.linspace(roi[0],roi[1],2**(i+1) + 1)
        guess = interp(x,nodes,result)
        print('Residuo: ' + str(residual[i]))
    return result,residual
