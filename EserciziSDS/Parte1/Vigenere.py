import math
import collections

def get_repeated_trigrams_frequencies(ciphertext):   # Restituisce un dizionario con le frequenze dei trigrammi ripetuti
    n = 3
    trigrams_frequencies = {}      
    for i in range(len(ciphertext) - n + 1):
        trigram = ciphertext[i : i+n]   # Seleziona un trigramma
        trigrams_frequencies[trigram] = trigrams_frequencies.get(trigram, 0) + 1   # Aggiunge 1 alla frequenza
    repeated_trigrams_frequencies = {}   # Crea un dizionario vuoto per i trigrammi filtrati
    for trigram, freq in trigrams_frequencies.items():
        if freq >= 2:
            repeated_trigrams_frequencies[trigram] = freq
    return repeated_trigrams_frequencies


def equals_trigrams_positions(ciphertext):   # Restituisce un dizionario che associa a ciascun trigramma ripetuto le posizioni dove compare nel testo
    trigram_frequencies = get_repeated_trigrams_frequencies(ciphertext)
    trigram_positions = {}   # Dizionario per memorizzare le posizioni dei trigrammi ripetuti
    for trigram, freq in trigram_frequencies.items():
        positions = []
        position = -1   # Inizia la ricerca dalla prima posizione possibile
        for _ in range(freq):
            position = ciphertext.find(trigram, position + 1)
            positions.append(position)
        trigram_positions[trigram] = positions
    return trigram_positions


def get_trigram_distances(ciphertext):   # Restituisce un dizionario con le distanze tra le posizioni di ciascuna occorrenza di ciascun trigramma
    trigram_positions = equals_trigrams_positions(ciphertext)
    trigram_distances = {}   # Dizionario per le distanze dei trigrammi
    for trigram, positions in trigram_positions.items():   # Scorre il dizionario con le posizioni di ciascun trigramma
        distances = [positions[i] - positions[i - 1] for i in range(1, len(positions))]   # Salva in un array le distanze tra le posizioni di un trigramma
        trigram_distances[trigram] = distances   # Associa l'array delle distanze al proprio trigramma in un dizionario
    return trigram_distances


def get_trigram_gcd(trigram_distances):
    trigram_gcd = {}  # Dizionario per i MCD delle distanze dei trigrammi
    for trigram, distances in trigram_distances.items():   # Calcola il MCD delle distanze per il trigramma corrente
        gcd = distances[0]
        for distance in distances:
            gcd = math.gcd(gcd, distance)
        trigram_gcd[trigram] = gcd
    return trigram_gcd


def get_top_3_frequent_mcd(mcd_dict):   # Trova possibile lunghezza della chiave secondo il test di Kasiski   
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


def find_vigenere_key_length(ciphertext, min_key_length=3, max_key_length=20):
    best_key_length = None
    best_index_diff = float('inf')
    typical_english_ic = 0.067

    for key_length in range(min_key_length, max_key_length + 1):   # Varia la lunghezza della chiave dal valore minimo al massimo
        subtexts = ['' for _ in range(key_length)] ###########
        for i, char in enumerate(ciphertext):    ############
            subtexts[i % key_length] += char

        indices = [calculate_coincidence_index(subtext) for subtext in subtexts]
        average_ic = sum(indices) / key_length   # Calcola l'ic medio delle sottostringhe considerate        
        index_diff = abs(average_ic - typical_english_ic)   # Calcola la differenza tra l'indice medio e quello tipico dell'inglese
        if index_diff < best_index_diff:   # Ricerca l'ic con la differenza minima da quello della lingua inglese
            best_key_length = key_length   # Aggiorna la migliore lunghezza della chiave
            best_index_diff = index_diff   # Aggiorna la migliore differenza rispetto all'ic della lingua inglese
    return best_key_length














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
    
    #Test di Kasiski
    repeated_trigram_frequencies = get_repeated_trigrams_frequencies(c)   # Frequenze dei trigrammi ripetuti
    print("Dizionario delle frequenze dei trigrammi ripetuti: ", repeated_trigram_frequencies, "\n")

    trigram_pos = equals_trigrams_positions(c)   # Posizioni dei trigrammi ripetuti
    print("Dizionario delle posizioni dei trigrammi ripetuti: ", trigram_pos, "\n")

    trigram_distances = get_trigram_distances(c)   # Distranze tra le posizioni dei trigrammi ripetuti
    print("Dizionario delle distanze tra le posizioni dei trigrammi: ", trigram_distances, "\n")

    trigram_gcd = get_trigram_gcd(trigram_distances)  # Calcola i MCD delle distanze
    print("Dizionario dei MCD delle distanze dei trigrammi: ", trigram_gcd)

    top_3_frequent = get_top_3_frequent_mcd(trigram_gcd)   # Visualizzo i 3 MCD più frequenti
    print("I 3 MCD più frequenti sono:", top_3_frequent)

    # Indici di coincidenza
    key_length = find_vigenere_key_length(c)
    print("Lunghezza della chiave stimata:", key_length)
