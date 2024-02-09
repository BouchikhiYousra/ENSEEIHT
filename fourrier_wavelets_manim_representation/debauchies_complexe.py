import numpy as np
import math as m

### Filtre associée à la suite de daubechies complexe :
### OUTPUT :
### Suite des coefficients non nuls de h sous la forme d'array
def h_dbc():
    h0, h5 = (-3 -np.sqrt(15)*1j)/64, (-3 -np.sqrt(15)*1j)/64
    h1, h4 = (5 - np.sqrt(15)*1j)/64, (5 - np.sqrt(15)*1j)/64
    h2, h3 = (15 + np.sqrt(15)*1j)/32, (15 + np.sqrt(15)*1j)/32
    return np.array([h0,h1,h2,h3,h4,h5])


### Calcul des coefficients de projection sur Vj:
### INPUT :
### signal : le signal à projeter sur Vj (array)
### h : la suite (h) associée à la famille multirésolution sous forme de liste ou array([h0,h1] par ex)
### OUTPUT :
### coeffs : les coefficients de signal dans la nouvelle base Vj sous forme array
def projection_V(signal, h):
    
    ### On vérifie la dimension du signal :
    taille = len(signal)
    if taille < 2 :
        return ("La taille doit être un multiple de 2")
    if np.log2(taille) != int(np.log2(taille)) :
        return ("La taille doit être un multiple de 2")
    
    ### On calcule la projection :
    coeffs = []
    taille_filtre = len(h)
    for i in range(int(taille/2)):
        res = 0.
        for j in range(taille_filtre):
            if (0 <= j + 2*i <= taille - 1):
                res += h[j]*signal[j + 2*i]
        coeffs.append(res)
    
    return np.array(coeffs)


### Calcul des coefficients de projection sur Wj:
### INPUT :
### signal : le signal à projeter sur Wj (array)
### h : la suite (h) associée à la famille multirésolution sous forme de liste ou array([h0,h1] par ex)
### OUTPUT :
### coeffs : les coefficients de signal dans la nouvelle base Wj sous forme array
def projection_W(signal, h):
    
    ### On vérifie la dimension du signal :
    taille = len(signal)
    if taille < 2 :
        return ("La taille doit être un multiple de 2")
    if np.log2(taille) != int(np.log2(taille)) :
        return ("La taille doit être un multiple de 2")
    
    ### On calcule la projection :
    coeffs = []
    taille_filtre = len(h)
    for i in range(int(taille/2)):
        res = 0.
        for j in range(taille_filtre):
            if (0 <= 1 - j + 2*i <= taille - 1):
                res += ((-1)**(1-j)) * (h[j]) * (signal[1 - j + 2*i])
        coeffs.append(res)
    
    return np.array(coeffs)


### Compression du signal :
### INPUT :
### signal : le signal à compresser (array)
### h : la suite (h) associée à la famille multirésolution sous forme de liste ou array([h0,h1] par ex)
### L : Nombre de compression que l'on souhaite effectuée
### OUTPUT :
### coeffs_compr : liste d'arrays contenant [Vl, Wl, Wl+1, ..., Wj]
def wavelet_transform(signal,h,L):
    
    ### On vérifie la dimension du signal :
    taille = len(signal)
    if taille < 2 :
        return ("La taille doit être un multiple de 2")
    if np.log2(taille) != int(np.log2(taille)) :
        return ("La taille doit être un multiple de 2")
    
    ### On vérifie les tailles :
    if L == 0 or len(signal) < len(h):
        return [signal]
    else:
        V = projection_V(signal, h)
        W = projection_W(signal, h)
        return wavelet_transform(V, h, L - 1) + [W]


### Reconstruction du signal à partir à partir de sa décomposition dans les différentes bases :
### INPUT :
### dec : la décomposition du signal dans les espaces Vj, Wj (liste d'arrays)
### h : la suite (h) associée à la famille multirésolution sous forme de liste ou array([h0,h1] par ex)
### OUPUT :
### le signal reconstruit sous forme d'array
def inverse_wavelet_transform(dec, h):
    if len(dec) > 2:
        V = inverse_wavelet_transform(dec[:-1], h)
    else:
        V = dec[0]
    W = dec[-1]
    N = len(h)
    M = len(V)
    g = [(-1) ** n * np.conj(h[N - 1 - n]) for n in range(N)]
    V2 = np.zeros(2 * M, dtype=type(h[0]))
    W2 = np.zeros(2 * M, dtype=type(h[0]))
    for i in range(0, M):
        for j in range(N):
            index_in_rec = 2 * i + j
            V2[index_in_rec % (2 * M)] += V[i] * h[j]
            W2[index_in_rec % (2 * M)] += W[i] * g[j]
    return V2 + W2

### Conversion d'une liste en coefficient en un array plus grand (enfait de la taille du signal initial)
### INPUT :
### liste_ : liste des coefficients (voir wavelet_transform)
### OUTPUT :
### tuple contenant l'array et une liste contenant la taille des liste initiales
def liste_to_array(liste_):
    return np.array([i for a in liste_ for i in a]), list(map(len, liste_))


### Conversion de de l'array contenant tous les coefficients en luste d'arrays conrrespondant à un espace :
### INPUT :
### array_ : le tableau contenant tous les coefficients
### liste_shape : liste avec les tailles des tableaux correspondant aux espaces
### OUTPUT :
### La liste des arrays
def array_to_liste(array_, liste_shape):
    res = []
    start = 0
    for shape in liste_shape:
        res.append(np.array(array_[start:start + shape]))
        start += shape
    return res


### Calcul du nombre de décomposition que l'on peut effectuer au maximum
### INPUT :
### h : la suite (h) associée à la famille multirésolution sous forme de liste ou array([h0,h1] par ex)
### n : puissance de 2 associée à la taille du signal
def max_level(h,n):
    return m.floor(np.log2(2**n/(len(h)-1)))


### Calcul de la fonction de phi_j_k :
### INPUT :
### h : la suite (h) associée à la famille multirésolution sous forme de liste ou array([h0,h1] par ex)
### n : Puissance de 2 correspondant à la taille du signal (ex : 10 pour un signal de taille 1024)
### j : indice de dilatation (-3 par exemple)
### k : indice de translation (1 par exemple pour phi_-3_1)
def phi_j_k(h, n, j, k):
    
    ### On vérifie que la valeur de k est correcte :
    if not (0 <= k <= 2**(-j) - 1) :
        return ("Erreur dans le choix de k")
    
    ### On calcule phi_j_k :
    zeros_ = np.zeros(2**n)
    wvt = wavelet_transform(zeros_,h,j+n)
    arr, coeff_slices = liste_to_array(wvt) 
    zeros_[k] = 1 
    coeffs_from_arr = array_to_liste(zeros_,coeff_slices)
    phi_j_k = inverse_wavelet_transform(coeffs_from_arr, h) 
    return phi_j_k


### Calcul de la fonction psi_j_k :
### INPUT :
### h : la suite (h) associée à la famille multirésolution sous forme de liste ou array([h0,h1] par ex)
### n : Puissance de 2 correspondant à la taille du signal (ex : 10 pour un signal de taille 1024)
### j : indice de dilatation (-4 par exemple)
### k : indice de translation (2 par exemple pour psi_-4_2)
def psi_j_k(h, n, j, k):
    
    ### On vérifie que la valeur de k est correcte :
    if not (0 <= k <= 2**(-j) - 1) :
        return ("Erreur dans le choix de k")
    
    ### On calcule psi_j_k :
    zeros_ = np.zeros(2**n)
    wvt = wavelet_transform(zeros_,h,j+n)
    arr, coeff_slices = liste_to_array(wvt) 
    zeros_[2**(-j) + k] = 1
    coeffs_from_arr = array_to_liste(zeros_,coeff_slices)
    psi_j_k = inverse_wavelet_transform(coeffs_from_arr, h) 
    return psi_j_k


### Calcul de toutes les fonctions phi et psi pour le dessin
### INPUT : 
### h : la suite (h) associée à la famille multirésolution sous forme de liste ou array([h0,h1] par ex)
### n : Puissance de 2 correspondant à la taille du signal (ex : 10 pour un signal de taille 1024)
### nb_details : nombre d'espaces de détails que l'on veut garder
def compute_functions(h,n,nb_details):
    
    ### On calcule j:
    L = max_level(h,n)
    j = L - n
    
    ### On calcule les phi :
    res = []
    for k in range(2**(-j)):
        res.append(phi_j_k(h,n,j,k))
    
    ### On calcule les psi pour les différents niveau de détails :
    for j_psi in range(abs(j),abs(j) + nb_details):
        for k in range(2**(j_psi)):
            res.append(psi_j_k(h,n,-j_psi,k))
            
    return res
    

### Calculer la projection complète sur tous les espaces.
### INPUT :
### signal : Le signal à décomposer
### h : la suite (h) associée à la famille multirésolution sous forme de liste ou array([h0,h1] par ex)
### nb_details : le nombre d'espaces de détails que l'on souhaite garder
### OUTPUT :
### liste d'array avec les projections succesives sur V puis sur les W
def projection_complete(signal,h,nb_details): 
    
    ### On vérifie la taille du signal :
    taille = len(signal)
    if taille < 2 :
        return ("La taille doit être un multiple de 2")
    if np.log2(taille) != int(np.log2(taille)) :
        return ("La taille doit être un multiple de 2")
    else :
        n = int(np.log2(taille))

    ### Calcul du niveau max de projection :
    L = max_level(h, n)
    
    ### Coefficients de projection du signal :
    ps = wavelet_transform(signal, h, L)
    ps = ps[:(nb_details+1)]
    ps = liste_to_array(ps)[0]
    
    ### Calcul des fonctions formant une base de l'espace de projection :
    fonctions = compute_functions(h,n,nb_details)
    
    ### Vérification de la compatibilité des dimensions :
    if len(fonctions) != len(ps) :
        return ("Erreur de dimension")
    else :
        for i in range(len(ps)):
            fonctions[i] = ps[i] * fonctions[i]
    
    return np.array(fonctions)