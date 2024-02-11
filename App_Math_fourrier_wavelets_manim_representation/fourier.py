import numpy as np

def Cn(f,n_fourier,n_riemann):
    # Calcul du n ième coefficient de Fourier de la fonction paramétrique f
    T = 2 * np.pi
    approx = 0
    largeur_rectangle = T / (n_riemann + 1)
    for i in range(n_riemann):
        indice = int(i/n_riemann * len(f))
        t = i / n_riemann * T
        approx += largeur_rectangle * f[indice] * (np.cos(2*np.pi/T*n_fourier*t) + 1j*np.sin(2*np.pi/T*n_fourier*t))
    return approx

def Cns(f,n_fourier_max,n_riemann):
    # Calcul des coefficients de Fourrier
    cns = []
    cns.append(Cn(f,0,n_riemann))
    for i in range(1,2*n_fourier_max+1):
        n_fourier = (-1)**(i-1)*((i+1)//2) # alternance de signe
        cns.append(Cn(f, n_fourier, n_riemann))
    return np.array(cns)