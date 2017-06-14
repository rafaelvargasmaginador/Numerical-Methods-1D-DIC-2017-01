"""
13/06/2017

"""
# importing libraries
import numpy as np
import matplotlib.pyplot as plt
from abq2img_1D import abq2img
from scipy import interpolate, optimize

SourceFile = 'signalexample.txt'



signal = np.genfromtxt(SourceFile)
signal = signal**2

#plots = 'true'

numnodes = 11
abqoutput = np.zeros((numnodes,2))
abqoutput[:,0] = np.linspace(0,1,numnodes) #Simula tracao
abqoutput[:,1] = np.linspace(0,-0.1,numnodes) #Simula tracao

def_signal = abq2img(signal, abqoutput)
#def_signal = np.loadtxt('abqoutputexample2.txt')
nan_n = max(np.sum(np.isnan(signal)), np.sum(np.isnan(def_signal)))
last_node = 1 - (nan_n / float(len(signal)))


def discre_signal(signal, nodes, type):
    x_nodes = np.rint(nodes * len(signal))
    x_nodes[-1] += -1
    y_nodes = np.zeros(len(x_nodes))
    for i in range(len(x_nodes)):
        y_nodes[i] = signal[x_nodes[i]]
    h = np.diff(x_nodes)
    aux = np.zeros((len(signal),))
    disc_signal = np.zeros((len(signal)))
    error = np.zeros(len(signal))
    element_value = np.zeros(len(x_nodes) - 1)

    if type == 1:

        for i in range(len(x_nodes) - 1):
            element_value[i] = np.average(signal[x_nodes[i]:x_nodes[i + 1]])
            disc_signal[x_nodes[i]:x_nodes[i + 1]] = np.average(signal[x_nodes[i]:x_nodes[i + 1]])

    elif type == 2:

        for i in range(len(x_nodes) - 1):
            coefs = np.polyfit(np.linspace(x_nodes[i], x_nodes[i + 1], h[i]), signal[x_nodes[i]:x_nodes[i + 1]], 1)

            aux[x_nodes[i]: x_nodes[i + 1]] = np.polyval(coefs, np.linspace(x_nodes[i], x_nodes[i + 1], h[i]))

            disc_signal[x_nodes[i]:x_nodes[i + 1]] = aux[x_nodes[i]:x_nodes[i + 1]].reshape(h[i])

    elif type == 3:

        cs = interpolate.CubicSpline(x_nodes, y_nodes)

        for i in range(len(x_nodes) - 1):
            disc_signal[x_nodes[i]:x_nodes[i + 1]] = cs(np.linspace(x_nodes[i], x_nodes[i + 1], h[i])).reshape(h[i])

    error = ((disc_signal - signal) / signal)
    # error_rms = np.sqrt(np.mean(np.square(error)))
    disc_signal[0:x_nodes[0]] = np.nan
    disc_signal[x_nodes[-1]:len(signal)] = np.nan

    return disc_signal, element_value


#nodes = np.linspace(0, last_node, 6)
nodes = np.linspace(0, 1, numnodes)

#nodes = np.array([0.01, 0.05, 0.17, 0.50, 0.60, 0.64, last_node - 0.01])

[test1, a] = discre_signal(signal, nodes, 1)
[test2, b] = discre_signal(signal, nodes, 2)
[test3, c] = discre_signal(signal, nodes, 3)

if plots == 'true':
    plt.figure(1)
    plt.subplot(311)
    plt.plot(test1, '.b')
    plt.plot(signal, 'r')
    plt.subplot(312)
    plt.plot(test2, '.b')
    plt.plot(signal, 'r')
    plt.subplot(313)
    plt.plot(test3, '.b')
    plt.plot(signal, 'r')
    plt.show()

    plt.figure(2)
    plt.plot(signal, 'r')
    plt.plot(def_signal, 'b')
    plt.show()


def error_fun(nodes, g, nodes_values, type):
    x_nodes = len(g) * nodes
    # disc_signal = np.zeros((len(g)))
    Error = np.zeros(len(x_nodes) - 1)
    el_value = np.zeros(len(x_nodes) - 1)

    if type == 1:
        for i in range(len(x_nodes) - 1):
            el_value[i] = np.average(g[x_nodes[i]:x_nodes[i + 1]])
            # disc_signal[nodes[i]:nodes[i+1]] = np.average(signal[nodes[i]:nodes[i+1]])
        Error = el_value - nodes_values
    return np.sqrt(np.mean(np.square(Error[not(np.isnan(Error)).all])))


uguess = np.linspace(0,-0.05,numnodes)
u = np.linspace(0,-0.1,numnodes)
'''
Test = error_fun(nodes+uguess, def_signal, a, 1)
print(Test)
Test = error_fun(nodes, def_signal, a, 1)
print(Test)
'''
#Newton-Raphson
aux_nodes = np.copy(nodes)

res = optimize.fmin(error_fun, nodes+uguess, args=(def_signal, a, 1))
print(res)
print(res - (nodes+u))
