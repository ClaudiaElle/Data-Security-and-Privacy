from public_key_cryptography import *
import numpy as np


def miller_rabin_algorithm(x, n, m, r):
    x0 = fast_exponentiation(x, m, n)   # Calcola x0
    if x0 == 1 or x0 == n-1:   # Se x0 è 1 o n-1, restituisco 0 (devo scegliere un altro x)
        return 0
    while r > 0:
        x = fast_exponentiation(x0, 2, n)   # Calcola gli xi ad ogni passo
        if x == n-1:   # Se xi è congruo a -1 mod n, restituisco 0 (devo scegliere un altro x)
            return 0
        if x == 1:  # Se xi=1 ho trovato quello che cercavo
            return euclidean_extended(x0+1, n)[0]  # Calcolo MCD(x0 + 1, n)
        x0 = x  # Aggiorno la x al passo precedente
        r -= 1   
    return 0  


def decryptionexp(n, d, e):
    m, r = find_odd_num(e*d-1)   # Trova m dispari ed r tali che ed-1 = 2^r * m
    i = 0   # Contatore iterazioni
    while(1):   # Ciclo finché non fattorizzo n
        i += 1   # Incrementa il numero di iterazioni
        x = random.randrange(n-1)   # Seleziono un x casuale
        euclide = euclidean_extended(x, n)
        if euclide[0] != 1:   # Se MCD tra x e n è diverso da 1 ho trovato la fattorizzazione
            p = euclide[1]
            q = n // p
            return i, p, q   # Restituisce il numero di iterazioni e i fattori p e q
        mcd = miller_rabin_algorithm(x, n, m, r)        
        if mcd != 0:   # Se l'mcd è un fattore di n
            p = mcd
            q = n // mcd
            return i, p, q   # Restituisce il numero di iterazioni e i fattori p e q



if __name__ == '__main__':
    exe_time = [0.0] * 100   # Tempo di esecuzione 
    iterations = [0] * 100   # Iterazioni
    for i in range(100):
        num, e, d, p, q = generate_keys(10**100 + 1, 10**101)  # Genera il modulo, gli esponenti e i fattori per RSA
        start = time.time()
        it, p1, q1 = decryptionexp(num, e, d)   # Attacco: restituisce numero di iterazioni e fattori p e q
        finish = time.time()
        iterations[i] = it
        exe_time[i] = finish - start   # Tempo impiegato per l'attacco
        assert (p == p1 or p == q1) and (q == q1 or q == p1)   # Controlla che i fattori trovati corrispondano a quelli originali
    print("Numero medio iterazioni per esecuzione: " + str(sum(iterations) / 100))
    print("Tempo medio per esecuzione: " + str(sum(exe_time) / 100) + " secondi")
    var = np.var(exe_time)   # Varianza dei tempi di esecuzione
    print("Varianza tempi di esecuzione: " + str(var) + " secondi al quadrato")
    print("Deviazione standard: " + str(var ** 0.5) + " secondi")

