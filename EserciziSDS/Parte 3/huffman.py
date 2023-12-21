from collections import Counter


def huffman_first_step(x_prob_dict):
    while len(x_prob_dict) > 1:
        min_key_1 = min(x_prob_dict, key=lambda k: x_prob_dict[k])   # Trova il simbolo con minore probabilità
        min_prob_1 = x_prob_dict.pop(min_key_1)   # Elimina dal dizionario il simbolo e restituisce la sua probabilità
        min_key_2 = min(x_prob_dict, key=lambda k: x_prob_dict[k])   # Trova il nuovo simbolo con minore probabilità
        min_prob_2 = x_prob_dict.pop(min_key_2)   # Elimina dal dizionario il simbolo e restituisce la sua probabilità
        tot_prob = min_prob_1 + min_prob_2   # Somma le due probabilità
        new_key = (min_key_1, min_key_2)   # Crea una tupla dei due simboli come nuova chiave per il dizionario
        x_prob_dict[new_key] = tot_prob   # Aggiunge al dizionario la tupla con associata la probabilità totale
        print("Dizionario delle probabilità:", x_prob_dict)
    print('\n')
    return x_prob_dict


def huffman_second_step(x_tuple, codeword = '', c_dict = None):
    if c_dict is None:
        c_dict = {}   # Crea un dizionario per associare simboli e codeword (se non esiste già)
    if isinstance(x_tuple, tuple):   # Se x_tuple è una tupla, aggiorna le codeword per le sotto-tuple
        huffman_second_step(x_tuple[0], codeword + '0', c_dict)   # 0 per il "ramo" sinistro
        huffman_second_step(x_tuple[1], codeword + '1', c_dict)   # 1 per il "ramo" destro
    else:   # Se x_tuple è un simbolo, aggiunge simbolo e relativa codeword al dizionario
        c_dict[x_tuple] = codeword
    return c_dict   # Restituisce il dizionario che associa a ciascun simbolo una codeword


def huffman_algorithm(alphabet, prob_list):
    if len(alphabet) != len(prob_list):
        raise ValueError("L'alfabeto e la lista delle probabilità devono avere lo stesso numero di elementi.")
    prob_dict = dict(zip(alphabet, prob_list))
    tuple_prob_dict = huffman_first_step(prob_dict)   # Dizionario delle frequenze raggruppate 
    x_tuple = list(tuple_prob_dict.keys())[0]   # Tupla di lettere raggruppate dal primo passo di Huffman
    codewords_dict = huffman_second_step(x_tuple)   # Dizionario che associa a ciascuna lettera una codeword
    return codewords_dict


def huffman_encoding(str, codewords_dict):
    str = ''.join(x.lower() for x in str if x.isalpha())   # Ripulisce la stringa, rendendola di sol caratteri
    encoded_str = str
    for letter in codewords_dict:   # Sostituisce ogni lettera con la relativa codeword
        encoded_str = encoded_str.replace(letter, codewords_dict[letter])
    return encoded_str   # Restituisce la stringa codificata e il dizionario usato per la compressione


def huffman_decoding(encoded_str, codewords_dict):
    if not all(bit in '01' for bit in encoded_str):
        raise ValueError("La stringa deve contenere solo 0 e 1.")
    temp = ''   # Inizializza una stringa per il confronto delle porzioni di stringa con le codeword nel dizionario
    decoded_string = ''   # Variabile per salvare le porzioni decodificate di stringa
    for str_char in encoded_str:   # Controlla ogni carattere della stringa codificata
        temp += str_char   # Concatena il carattere corrente con i precedenti in temp
        if temp in codewords_dict.values():   # Se temp corrisponde ad una codeword nel dizonario
            decoded_char = next(key for key, value in codewords_dict.items() if value == temp)   # Decodifica la porzione di stringa
            decoded_string += decoded_char   # Concatena la porzione di stringa decodificata
            temp = ''   # Resetta la variabile temporanea per il comfronto con le codeword del dizionario
    return decoded_string   # Restituisce la stringa decodificata


if __name__ == "__main__":
    alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
    prob = [0.025, 0.025, 0.05, 0.1, 0.13, 0.17, 0.25, 0.25]
    h_dict = huffman_algorithm(alphabet, prob)
    print("Dizionario delle codeword ottenute tramite l'algoritmo di Huffman: ", h_dict, "\n")
    encoded_str = huffman_encoding('abcdefgh', h_dict)
    print("Stringa codificata:", encoded_str, "\n")
    decoded_str = huffman_decoding(encoded_str, h_dict)
    print("Stringa decodificata:", decoded_str)