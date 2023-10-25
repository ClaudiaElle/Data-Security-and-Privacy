import numpy as np
from math import gcd
import sympy


def generate_square_matrix(matrix_size):   # Restituisce una matrice random di interi, invertibile modulo 26
    matrix = np.random.randint(0, 10, size=(matrix_size, matrix_size))    
    while is_matrix_invertible(matrix) == False:   # Se la matrice trovata non è invertibile mod 26 ne cerca una nuova
        matrix = np.random.randint(0, 10, size=(matrix_size, matrix_size))
    print("Matrice chiave k selezionata: ", matrix)   # Stampa la matrice trovata
    return matrix   # Resttuisce la matrice quadrata invertibile mod26


def clean_text (text):
    text_letters = "".join(filter(str.isalpha, text)).lower()   # Rimuove ciò che non è testo e trasforma in minuscolo
    return text_letters


def prepare_message(plaintext, block_size):
    plaintext = clean_text(plaintext)
    p_blocks = []  # Lista per i blocchi di numeri ASCII
    current_block = []  # Blocco corrente
    for char in plaintext:
        ascii_num = ord(char) - 97  # Converte il carattere in numero ASCII
        current_block.append(ascii_num)  # Aggiunge il numero al blocco corrente
        if len(current_block) == block_size:
            p_blocks.append(np.array(current_block))  # Converte il blocco in un array Numpy e lo aggiunge a p_blocks
            current_block = []
    return p_blocks


def encrypt(plaintext, k):
    ciphertext = ""   # Inizializza la stringa cifrata
    for block in plaintext:
        encrypted_block = (np.dot(k, block)) % 26   # Moltiplica il blocco per la matrice chiave e applica l'aritmetica modulare
        for num in encrypted_block:  
            ciphertext += chr(num + 97)   # Converte il blocco cifrato in caratteri e aggiunge alla stringa cifrata
    return ciphertext


def is_matrix_invertible(matrix):
    invertible = True
    if matrix.shape[0] != matrix.shape[1]:   # Verifica se la matrice è quadrata, se non lo è solleva un errore
        raise ValueError("La matrice non è quadrata.")
    determinante = round(np.linalg.det(matrix)) % 26   # Determinante della matrice modulo 26    
    if gcd(determinante, 26) != 1:   # Verifica se la matrice è invertibile modulo 26
        print("La matrice non è invertibile modulo 26.")
        invertible = False   # Se la matrice non è invertibile stampa un messaggio e restituisce falso
    return invertible


def matrix_mod_inverse(matrix):
    if is_matrix_invertible(matrix):    
        inverse_matrix = sympy.Matrix(matrix).inv_mod(26)   # Matrice inversa oggetto di Sympy
        inverse_matrix = np.array(inverse_matrix.tolist()).astype(int)   # Trasforma l'oggetto Sympy in una matrice Numpy
    else:
        raise ValueError("La matrice non è invertibile modulo 26.")   # Se la matrice non è invertibile mod26 solleva un errore        
    return inverse_matrix
        

def decrypt(ciphertext, k):    
    inverse_matrix = matrix_mod_inverse(k)   # Calcola l'inversa modulo 26
    decripted_message = encrypt(ciphertext, inverse_matrix)   # Stessa procedura di encription ma con matrice inversa modulo 26
    return decripted_message


def attack(message, encripted_message, block_size):
    plaintext = prepare_message(message, block_size)   # Trasforma il messaggio in blocchi di valori ASCII
    ciphertext = prepare_message(encripted_message, block_size)   # Trasforma il messaggio cifrato in blocchi di valori ASCII
    message = clean_text(message)
    max_lenght = len(message) - len(message) % block_size
    k = None   # Inizializza la chiave a None
    p_index = 0   # Inizializza l'indice per i blocchi di p
    c_index = 0   # Inizializza l'indice per i blocchi di c
    while p_index < len(plaintext) - block_size + 1 and c_index < len(ciphertext) - block_size + 1:
        p1 = np.array(plaintext[p_index:p_index+block_size]).T   # Prende due blocchi consecutivi di plaintext in una matrice
        c1 = np.array(ciphertext[c_index:c_index+block_size], dtype=int).T   # Prende due blocchi consecutivi di ciphertext in una matrice
        try:
            p1 = matrix_mod_inverse(p1)   # Calcola l'inversa modulo 26 di p1
            k = (np.dot(c1, p1)) % 26  # Calcola la chiave k utilizzando c1 e l'inversa di p1
            decripted_message = decrypt(ciphertext, k)   # Tenta la decription con la chiave trovata            
            if decripted_message == message[ :max_lenght]:   # Verifica se la decriptazione funziona correttamente con k
                print("Messaggio decifrato durante l'attacco: ", decripted_message)
                return k   # Restituisci la chiave trovata se corretta
        except Exception as e:   # Se la chiave non è invertibile tenta con il prossimo blocco
            print(f"Errore: {e}. Continua con il prossimo blocco.")
        p_index += 1
        c_index += 1
    raise Exception("Chiave non trovata.")   # Se non trova k in nessuno dei tentativi solleva un errore



if __name__ == '__main__':
    message = "Once upon a midnight dreary, while I pondered, weak and weary,"\
    "Over many a quaint and curious volume of forgotten lore—"\
    "While I nodded, nearly napping, suddenly there came a tapping,"\
    "As of some one gently rapping, rapping at my chamber door."\
    "“’Tis some visitor,” I muttered, “tapping at my chamber door—"\
    "Only this and nothing more.”"
    k = generate_square_matrix(3)

    # Encription
    plaintext = prepare_message(message, len(k))
    encripted_message = encrypt(plaintext,k)
    print("Testo cifrato:", encripted_message)

    #Decription
    ciphertext = prepare_message(encripted_message, len(k))
    decripted_message = decrypt(ciphertext, k)
    print("Testo decifrato:", decripted_message)

    # Attack
    k_found = attack(message, encripted_message, len(k))
    print("Chiave trovata: ", k_found)

    

