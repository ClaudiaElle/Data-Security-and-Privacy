from collections import Counter
import matplotlib.pyplot as plt
import math


def clean_text (text):
    text_letters = "".join(filter(str.isalpha, text)).lower()   # Rimuove ciò che non è testo e trasforma in minuscolo
    return text_letters


def frequency_histogram(text):
    cleaned_text=clean_text(text)
    counter = Counter(cleaned_text)   # Crea un dizionario con le frequenze di ciascuna lettera
    letters, frequencies = zip(*sorted(counter.items()))   # Estrae le lettere e le relative occorrenze e ordina in ordine alfabetico    
    plt.bar(letters, frequencies)   # Creazione istogramma
    plt.xlabel('Letters')   # Aggiunge le etichette all'istogramma
    plt.ylabel('Frequencies')
    plt.title('Frequency Histogram')    
    plt.show()   # Mostra l'istogramma


def mgram_distribution(text, m):
    cleaned_text = clean_text(text)
    mgram_distribution = Counter(cleaned_text[i:i + m] for i in range(0, len(cleaned_text) - m + 1, m))   # Crea un dizionario con le frequenze di ciascun m-gramma
    total_mgrams = sum(mgram_distribution.values())
    relative_frequencies = {mgram: freq / total_mgrams for mgram, freq in mgram_distribution.items()}  # Crea un dizionario con m-grammi come chiavi e frequenze relative come valori
    blocks, _ = zip(*sorted(mgram_distribution.items()))  # Estrae gli m-grammi e li ordina in ordine alfabetico
    num_to_show = min(50, len(blocks))   # Mostra solo le prime 50 frequenze
    relative_frequencies_list = [relative_frequencies[mgram] for mgram in blocks[:num_to_show]]    # Estrae le frequenze relative in base alle chiavi dal dizionario
    plt.bar(blocks[:num_to_show], relative_frequencies_list)  # Utilizza le frequenze relative
    plt.xlabel('Blocks')
    plt.ylabel('Relative Frequencies')   # Modifica l'etichetta
    plt.title(f'{m}-Grams Relative Frequency Histogram')   # Modifica il titolo
    plt.xticks(rotation='vertical')   # Mette le etichette in verticale
    plt.show()   # Mostra l'istogramma
    return mgram_distribution


def coincidence_index(mgram_distribution):   # Calcola l'indice di coincidenza per blocchi di lunghezza m
    total_mgrams = sum(mgram_distribution.values())   # Calcola il numero totale di m-grammi
    ic = sum((frequency*(frequency-1)) for frequency in mgram_distribution.values())/(total_mgrams*(total_mgrams-1))     
    return ic


def shannon_entropy(mgram_distribution):   # Calcola l'entropia di shannon per blocchi di lunghezza m
    total_mgrams = sum(mgram_distribution.values())
    entropy = -sum((frequency / total_mgrams) * math.log2(frequency / total_mgrams) for frequency in mgram_distribution.values())
    print(total_mgrams)
    # Clacola frequenza relativa, la moltiplica per il suo logaritmo in base due e somma tutti i valori, moltiplicando per -1 per 
    return entropy    


if __name__ == "__main__":
    with open("moby.txt", "r", encoding="utf8") as moby_dick:
        text = moby_dick.read()   

    frequency_histogram(text)   # Istogramma delle frequenze delle 26 lettere
    
    for i in range(1, 5):
        distribution = mgram_distribution(text, i)   # Distribuzione empirica degli m-grammi
        ic = coincidence_index(distribution)   # Indice di coincidenza della distribuzione degli m-grammi
        entropy = shannon_entropy(distribution)   # Entropia della distribuzione degli m-grammi
        print(f"Indice di coincidenza con blocchi di lunghezza {i}: {ic}")
        print(f"Entropia di Shannon con blocchi di lunghezza {i}: {entropy}")
