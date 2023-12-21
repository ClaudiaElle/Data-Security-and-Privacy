import random
import time


def euclidean_extended(a, b):   # Utilizza l'algoritmo di Euclide esteso per calcolare l'MCD
    # tra a e b e per trovare i coefficienti
    x, y = 1, 0   # Coefficienti di a e b
    x1, y1 = 0, 1   # Variabili temporanee per i coefficienti di a e b
    while b != 0:   # Itera finché il resto non è zero
        q = a // b   # Quoziente intero
        a, b = b, a % b   # Calcola il resto, assegna b ad a e mette in b il resto
        x, x1 = x1, x - q * x1   # Aggiorna il coefficiente di a
        y, y1 = y1, y - q * y1   # Aggiorna il coefficiente di b      
    return a, x, y


def fast_exponentiation(a, e, n):   # Restituisce a^e mod(n)
    d = 1   # Accumulatore prodotti parziali
    binary_representation = []   # Array per memorizzare l'esponente in binario
    while e != 0:
        e, di = e // 2, e % 2   # Calcola la cifra binaria corrente di e, aggiorna e
        binary_representation.append(di)   # Aggiunge il risultato di e % 2 all'array
    for di in reversed(binary_representation):
        d = (d ** 2) % n
        if di == 1:
            d = (d * a) % n
    return d


def find_odd_num(n, r = 0):   # Restituisce un numero dispari m e la potenza r tale che 2^r * m = n
    if n % 2 != 0:   # Se n è dispari restituisce n e r
        return n, r
    n, r = find_odd_num(n // 2, r + 1)   # Ripete il procedimento su n//2, incrementando r
    return n, r


def miller_rabin_test(x, n):   # Restituisce vero se n è composto, utilizza x per effettuare il test
    if x >= n or x <= 0:
        raise ValueError("Il vaore di x deve essre compreso tra 0 e n, estremi esclusi.") 
    if n != 2 and n % 2 == 0:   # Se n è pari allora è composto
        return True
    m, r = find_odd_num(n-1)
    x = fast_exponentiation(x, m, n)   # Calcola x0
    if x == 1 or x == n-1:   # Se x0 è 1 o n-1, allora n non è composto
        return False
    while r > 0:
        x = fast_exponentiation(x, 2, n)   # Calcola gli xi ad ogni passo
        if x == n-1:   # Se xi è n-1, allora il numero non è composto
            return False   
        r -= 1 
    return True   # Se non viene violata alcuna condizione, n è composto


def generate_prime_number(min_num , max_num, max_err):   # Genera casualmente un numero primo
    err = 0.25   # Inizializza la probabilità di errore
    n = random.randrange(min_num, max_num)   # Genera casualmente un numero intero
    x = random.randrange(2, n-1)   # Genera casualmente la x per il test di Miller-Rabin
    while miller_rabin_test(x, n):   # Ripete la generazione finché non trova un numero primo
        n = random.randrange(min_num, max_num)
        x = random.randrange(1, n-1)
    while err > max_err:   # Ripte il test di Miller-Rabin su n finché err non è al di sotto di max_err
        x = random.randrange(1, n-1)   # Genera un nuovo x per il test di Miller-Rabin
        if miller_rabin_test(x, n):   # Se n risulta composto, genera un nuovo n e ripete i test
            generate_prime_number(min_num, max_num, max_err)
        err *= 0.25   # Aggiorna la probabilità di errore ad ogni iterazione  
    return n


def generate_prime_factors(min_num, max_num):   # Genera due diversi numeri primi nell'intervallo specificato
    if min_num > max_num:
        raise ValueError("Inserire un intervallo appropriato.")
    p = generate_prime_number(min_num, max_num, 0.001)
    q = generate_prime_number(min_num, max_num, 0.001)
    while p == q:   # p e q devono essere primi distinti
        q = generate_prime_number(min_num, max_num, 0.001)   # Genero nuovamente q finché non è diverso da p
    return p, q


def generate_keys(min_num, max_num):   # Genera il modulo, la chiave pubblica e privata per RSA
    p, q = generate_prime_factors(min_num, max_num)   # Genera due numeri primi nel range specificato
    n = p * q   # Trova il modulo n come prodotto dei due numeri primi p e q
    phi_n = (p-1) * (q-1)
    e = random.randrange(1, phi_n)   # Genera casualmente un valore per l'esponente pubblico "e"
    mcd, d, y = euclidean_extended(e, phi_n)   # Controlla che e sia coprimo con phi_n
    d = d % phi_n
    while mcd != 1:   # Itera finché non trova e coprimo con phi_n
        e = random.randrange(1, phi_n)
        mcd, d, y = euclidean_extended(e, phi_n)   # d contiene l'esponente privato che dovrebbe essere grande
        d = d % phi_n
    if d < e:
        e, d = d, e   # Se d è più piccolo di e, scambio tra loro i valori, per avere d grande
    return n, e, d, p, q


def RSA_cipher(message, key, n):   # Cifra o decifra message tramite il cifrario RSA
    message = fast_exponentiation(message, key, n)
    return message


def decrypt_RSA_with_CRT(message, key, p, q, inv_p, inv_q):   # Cifra o decifra tramite il cifrario RSA ottimizzato
    # con il teorema cinese del resto
    sp = fast_exponentiation(message, key%(p-1), p)
    sq = fast_exponentiation(message, key%(q-1), q)
    #mcd, inv_p, inv_q = euclidean_extended(p, q)   # Ricava l'inverso di p modulo q e quello di q modulo p
    s = ((q * inv_q * sp) + (p * inv_p * sq)) % (p * q)   # Messaggio risultante
    return s



if __name__ == '__main__':
    # Euclide esteso
    mcd, x, y = euclidean_extended(60, 17)   
    print("MCD tra 60 e 17:", mcd, "con coefficienti di Bezout x =", x, " y =", y, "\n")
    # Esponenziazione veloce
    print("Esponenziazione veloce di 3 ^ 11 mod 10:", fast_exponentiation(3, 11, 10), "\n")
    # Test di compostezza di Miller-Rabin
    print("Test di compostezza di Miller-Rabin per 881: ", miller_rabin_test(4, 881), "\n")
    # Generazione numeri primi
    print("Numero primo: ", generate_prime_number(4, 100, 0.000001), "\n")

    # RSA
    n, e, d, p, q = generate_keys(10**100 + 1, 10**101)
    mcd, inv_p, inv_q = euclidean_extended(p, q)   # Ricava l'inverso di p modulo q e quello di q modulo p
    inv_p = inv_p % q
    inv_q = inv_q % p
    print("e iniziale:",e)

    time_RSA = [0.0] * 100   # Tempi RSA standard
    time_RSA_CRT = [0.0] * 100   # Tempi RSA con CRT
    for i in range(100):
        message = random.randrange(2, 10**100)   # Generazione casuale messaggio
        print("Esecuzione numero: " + str(i + 1))
        ciphertext = RSA_cipher(message, e, n)   # Cifratura
        t_start = time.time()

        plaintext = RSA_cipher(ciphertext, d, n)   # Decifratura con RSA
        t_finish = time.time()
        print("Tempo di esecuzione RSA:", t_finish - t_start)
        time_RSA[i] = t_finish - t_start   # Salva il tempo di esecuzione RSA

        t_start = time.time()
        plaintext_CRT = decrypt_RSA_with_CRT(ciphertext, d, p, q, inv_p, inv_q)   # Decifratura con RSA ottimizzato con CRT
        t_finish = time.time()
        print("Tempo di esecuzione RSA con CRT:", t_finish - t_start, "\n")
        time_RSA_CRT[i] = t_finish - t_start   # Salva il tempo di esecuzione RSA con CRT

        assert (plaintext == plaintext_CRT and plaintext == message)   # Controlla che il messaggio originale e quelli decifrati corrispondano
        

    time_RSA_tot = sum(time_RSA)  # Somma dei tempi di esecuzione
    time_CRT_tot = sum(time_RSA_CRT)
    print("Tempo totale RSA senza CRT: " + str(time_RSA_tot) + " secondi.")
    print("Tempo totale RSA con CRT: " + str(time_CRT_tot) + " secondi.")