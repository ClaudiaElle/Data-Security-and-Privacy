import math
import collections
from collections import Counter
import string
import numpy as np

def get_repeated_ngrams_frequencies(ciphertext, n):   # Restituisce un dizionario con le frequenze degli n-grammi ripetuti
    ngrams_frequencies = {}      
    for i in range(len(ciphertext) - n + 1):
        ngram = ciphertext[i : i+n]   # Seleziona un n-gramma
        ngrams_frequencies[ngram] = ngrams_frequencies.get(ngram, 0) + 1   # Aggiunge 1 alla frequenza
    repeated_ngrams_frequencies = {}   # Crea un dizionario vuoto per gli n-grammi filtrati
    for trigram, freq in ngrams_frequencies.items():
        if freq > 1:   # Seleziona solo gli n-grammi ripetuti
            repeated_ngrams_frequencies[trigram] = freq
    return repeated_ngrams_frequencies


def equals_ngrams_positions(ciphertext, n):   # Restituisce un dizionario che associa a ciascun n-gramma ripetuto le posizioni dove compare nel testo
    ngram_frequencies = get_repeated_ngrams_frequencies(ciphertext, n)
    ngram_positions = {}   # Dizionario per memorizzare le posizioni degli n-grammi ripetuti
    for trigram, freq in ngram_frequencies.items():
        positions = []
        position = -1   # Inizia la ricerca dalla prima posizione possibile
        for _ in range(freq):
            position = ciphertext.find(trigram, position + 1)
            positions.append(position)
        ngram_positions[trigram] = positions
    return ngram_positions


def get_ngram_distances(ciphertext, n):   # Restituisce un dizionario con le distanze tra le posizioni di ciascuna occorrenza di ciascun trigramma
    ngram_positions = equals_ngrams_positions(ciphertext, n)
    ngram_distances = {}   # Dizionario per le distanze degli n-grammi
    for ngram, positions in ngram_positions.items():   # Scorre il dizionario con le posizioni di ciascun n-gramma
        distances = [positions[i] - positions[i - 1] for i in range(1, len(positions))]   # Salva in un array le distanze tra le posizioni di un n-gramma
        ngram_distances[ngram] = distances   # Associa l'array delle distanze al proprio n-gramma in un dizionario
    return ngram_distances


def get_trigram_gcd(trigram_distances):   # Calcola gli MCD tra le distanze
    trigram_gcd = {}   # Dizionario per i MCD delle distanze dei trigrammi
    for trigram, distances in trigram_distances.items():   # Calcola il MCD delle distanze per il trigramma corrente
        gcd = distances[0]
        for distance in distances:
            gcd = math.gcd(gcd, distance)
        trigram_gcd[trigram] = gcd
    return trigram_gcd


def get_top_3_frequent_mcd(trigram_distances):   # Trova possibile lunghezza della chiave secondo il test di Kasiski  
    mcd_dict = get_trigram_gcd(trigram_distances) 
    mcd_frequencies = collections.Counter(mcd_dict.values())   # Conta le frequenze degli MCD nel dizionario  
    top_3_frequent_mcd = [mcd for mcd, _ in mcd_frequencies.most_common(3)]   # Trova i 3 MCD più frequenti
    return top_3_frequent_mcd


def calculate_coincidence_index(text):   # Calcola l'indice di coincidenza per il testo
    total_chars = len(text)
    char_count = {}   # Dizionario che tiene traccia delle occorrenze di ogni carattere nel testo
    for char in text:
        char_count[char] = char_count.get(char, 0) + 1   # Incrementa il conteggio delle occorrenze del carattere se presente, altrimenti crea una nuova voce
    ic = 0
    for char, count in char_count.items():
        ic += (count / total_chars) * ((count - 1) / (total_chars - 1))   # Calcola l'indice di coincidenza
    return ic


def get_subtexts(ciphertext, key_length):   # Restituisce un array di sottostringhe divise in base alla lettera della chiave usata per la cifratura
    subtexts = ['' for _ in range(key_length)]   # Inizializza un array di stringhe vuote di lunghezza della chiave
    for i, char in enumerate(ciphertext): 
            subtexts[i % key_length] += char   # Aggiunge il carattere corrente alla sottostringa appropriata
    return subtexts


def find_vigenere_key_length(ciphertext, min_key_length=3, max_key_length=20):
    best_key_length = None
    best_rmse = float('inf')   # Inizializza con un valore infinito
    typical_english_ic = 0.067
    for key_length in range(min_key_length, max_key_length + 1):   # Varia la lunghezza della chiave dal valore minimo al massimo
        subtexts = get_subtexts(ciphertext, key_length)
        indexes = [calculate_coincidence_index(subtext) for subtext in subtexts]        
        rmse = math.sqrt(sum((ic - typical_english_ic) ** 2 for ic in indexes) / key_length)  # Calcola lo scarto quadratico medio
        if rmse < best_rmse:   # Ricerca l'ic con la differenza minima da quello della lingua inglese
            best_key_length = key_length   # Aggiorna la migliore lunghezza della chiave
            best_rmse = rmse   # Aggiorna la migliore differenza rispetto all'ic della lingua inglese
            indexes_best_k_lenght = indexes   # Salva gli indici di coincidenza per il valore scelto di m
    return best_key_length, indexes_best_k_lenght


def find_vigenere_key(ciphertext, key_length):
    eng_frequencies = np.array([0.082, 0.015, 0.028, 0.043, 0.13, 0.022, 0.02, 0.061, 0.07, 0.0015, 0.0077, 0.04, 0.024, 0.067, 0.075, 0.019,
         0.00095, 0.06, 0.063, 0.091, 0.028, 0.0098, 0.028, 0.0015, 0.02, 0.00074])   # Vettore frequenze lingua inglese
    subtexts = get_subtexts(ciphertext, key_length)   # Restituisce un vettore di stringhe, raggruppate in base alla lettera della chiave usata per cifrarle
    alphabet = string.ascii_lowercase   # Insieme di tutte le lettere dell'alfabeto in ordine
    key = ""
    for subtext in subtexts:
        letters_frequencies = Counter(subtext)   # Dizionari delle frequenze delle lettere nella sottostringa
        vector_frequencies = [letters_frequencies.get(letter, 0) for letter in alphabet]   # Crea un vettore delle frequenze di tutte le lettere dell'alfabeto
        tot_letters = sum(vector_frequencies)   # Totale lettere nella sottostringa
        vector_frequencies = np.array([freq/tot_letters for freq in vector_frequencies])   # Vettore con frequenze relative
        scalar_prod = 0
        key_letter = ""
        for shift in range(26):
            scalar_prod_temp = np.dot(eng_frequencies, np.roll(vector_frequencies, -1 * shift))   # Prodotto scalare e shift di vector_frequences
            if scalar_prod_temp > scalar_prod:   #  Ricerca lo shift che massimizza il prodotto scalare
                scalar_prod = scalar_prod_temp
                key_letter = chr(shift + 97)   # Trasforma lo shift nella lettera corrispondente (della chiave)
        print("Lettera della chiave trovata: ", key_letter, " con prodotto scalare", scalar_prod)
        key += key_letter
    return key    


def decrypt_vigenere(ciphertext, k):
    ciphertext = [ord(char) for char in ciphertext]
    k = [ord(char) for char in k]
    decripted_message = ""
    for i in range(len(ciphertext)):
        decripted_message += chr(((ciphertext[i] - k[i % len(k)]) % 26) + 97)
    return decripted_message
 


if __name__ == '__main__':
    c = "ZYIVIUPYKFJZLKRRIFVJMTGBLTSAVYEPXFWYIJTU"\
        "KSSXHKRJOKLKEYEBTVQGRCAYQVHYXXAVMYXGXNIZVRYRWZOBJ"\
        "YMYKXOHTUETHLOHTULOQYEYLGYYLKDVTKSGDUNRUWMTGXENYZ"\
        "RMZOSPUJMZCZHRGZVGVUUAJYMSFKCBSZRMTGIALLPRCANLOVPJ"\
        "MTGOKWSXINEFRZTVIJFEKVXUSTEFOUIZLKSRTJIZLGTQOJGUZK"\
        "RVTXECEETBHIIGGNTUOJFGVXIRXNSAPJSBSVLUARIOKIEZINIZ"\
        "CRWISSPRRCMTKHUGNVOTICIGCRWGFYUEJVZKROFUKUMJJONQGW"\
        "PGAONGNVTXSMRNSNLOGNEAGSPKHNIZZFFXIGKGNISAKNHRQEIC"\
        "LKDTGZRTSZHVTXFAXJEPXVEYMTGYEIIGPOSGOTWAVXOHTUMTKY"\
        "TUKIIISXDVTXGUYRDBTCCISTTNOEGUQVLRZVMTJURZGKMURLOEV"\
        "FMTXYOSBZICAOTUOEEIIXTNOEJOROTRFFRKERLGNVVKAGSGUVWI"\
        "EVEGUNEYEXETOFRCLKRRNZWBMKWBLKLKGOTLCFYRHHESACPUJJI"\
        "FZFVZMUNFGEHUQOSFOFRYETDJULPJIBEAZLERPEFNJVXUFRAPQY"\
        "IYXKPCKUFGGQFEUDXNIIOETVVNERFQOJTOVOTRJYERJGMHYVHCL"\
        "GTUGULKLUPRJKSLMTDNJFSXEZTUKVHMIUFGNVQUHKLZGIOKHKXV"\
        "ZKLXSAGUCYMILNEPULPJAGLXULXORZOEKRPOXE".lower() 

    # Ripetizioni nel testo  
    for n in range(2, 6):
        repeated_ngram_frequencies = get_repeated_ngrams_frequencies(c, n)   # Frequenze degli n-grammi ripetuti
        print("Dizionario delle frequenze dei ", n, "-grammi ripetuti: ", repeated_ngram_frequencies, "\n")   
        ngram_distances = get_ngram_distances(c, n)   # Distranze tra le posizioni degli n-grammi ripetuti
        print("Dizionario delle distanze tra le posizioni dei ", n, "-grammi: ", ngram_distances, "\n")

    # Test di Kasiski    
    repeated_trigram_frequencies = get_repeated_ngrams_frequencies(c, 3)   # Frequenze degli n-grammi ripetuti
    print("Dizionario delle frequenze dei ", n, "-grammi ripetuti: ", repeated_ngram_frequencies, "\n")    

    trigram_distances = get_ngram_distances(c, 3)   # Distranze tra le posizioni dei trigrammi ripetuti
    print("Dizionario delle distanze tra le posizioni dei trigrammi: ", trigram_distances, "\n")

    top_3_frequent = get_top_3_frequent_mcd(trigram_distances)   # Visualizzo i 3 MCD più frequenti: possibili lunghezze k
    print("I 3 MCD più frequenti sono: ", top_3_frequent, "\n")

    # Indici di coincidenza
    key_length, indexes = find_vigenere_key_length(c)   # Trova la lunghezza della chiave e i relativi indici di coincidenza
    print("Lunghezza della chiave stimata tramite indici di coincidenza:", key_length, "\n")
    print("Valori degli indici di coincidenza per la lunghezza della chiave trovata: ", indexes, "\n")
    print("Valore medio indici di coincidenza: ", sum(indexes) / key_length, "\n")

    k = find_vigenere_key(c, key_length)   # Trova la chiave con il metodo degli indici di coincidenza
    print("\nChiave trovata: ", k, "\n")
    
    message = decrypt_vigenere(c, k)   # Decifra il messaggio con la chiave trovata
    print("Messaggio decifrato: ", message)
