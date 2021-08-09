import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import sys
from math import *

style.use('dark_background')

n = int(input("n = "))

P1 = 0.5

x = np.linspace(-0.25, 0.25, n)
t = np.linspace(0, 60, n*100)


dx = x[1] - x[0]
dt = t[1] - t[0]

tau0 = 273.15-17
tau1 = 273.15+32

S = np.linspace(tau0 - (tau1-tau0)/10, tau1 + (tau1-tau0)/10, 20)

#alpha0 = 1.3323*(10**(-7))
#alpha0 = 0

alpha0 = 1.0829*(10**(-6))
alpha1 = 4.11140578*(10**(-6))

def init(x):
    psi = []
    alpha = []
    for i in range(int(len(x)*P1)):
        psi.append(tau0 + np.exp(x[i] + 0.1))
        alpha.append(alpha0)
    for i in range(len(x) - int((len(x)*P1))):
        psi.append(tau1 - np.exp(-x[i] - 0.1))
        alpha.append(alpha1)
    return(psi, alpha)

psi0 = init(x)[0]
alpha = init(x)[1]

def conduction(psi0, x, t):
    psi = []
    psi.append(psi0)
    for i in range(len(t)):
        psix = []
        psix.append(tau0)
        for v in range(1, len(x)-1):
            psixv = psi[i][v] + alpha[v]*((psi[i][v+1] - 2*psi[i][v] + psi[i][v-1])/(dx*dx))*dt
            psix.append(psixv)
        psix.append(tau1)
        psi.append(psix)
        if i%(n) == 0:
            print(int(i*(100/len(t))), " %")
    return(psi)

psi = conduction(psi0, x, t)

fig = plt.figure()

input("press a key to start the simualtion")

sys.path.append('/img')

T = []

plt.ion()

plt.plot(x, psi0, color = 'green')
plt.ylim([tau0 - (tau1-tau0)/5, tau1 + (tau1-tau0)/5])
plt.pause(2)

for i in range(len(t)):
    try:
        plt.clf()
        #plt.plot(x[int(len(x)*P1)], S, color = 'red')
        plt.scatter(x[int(len(x)*P1)], 273.15+10, color = 'green')
        plt.plot(x, psi[i*int((len(t)/150))])
        plt.ylim([tau0 - (tau1-tau0)/5, tau1 + (tau1-tau0)/5])
        plt.xlabel("distance en m")
        plt.ylabel(r"$\tau(x, t = {})$ en K".format(t[i*int(len(t)/150)]))
        plt.title("t = {}s, and T = {}°C".format(t[i*int((len(t)/150))], psi[i*int((len(t)/150))][int(len(x)*P1 + 1)] - 273.15))
        T.append(psi[i*int((len(t)/150))][int(len(x)*P1 + 1)] - 273.15)
        #plt.savefig("s{}.png".format(i))
        plt.pause(0.01)
    except IndexError:
        t_ = np.linspace(0, 60, len(T))
        plt.ylim([T[len(T) - 1] - 2, tau1 - 273.15 + 2])
        plt.plot(t_, T)
        plt.xlabel("temps en s")
        plt.ylabel("Temperature en °C")
        #plt.savefig("temps-t4.png")
        plt.pause(2)
