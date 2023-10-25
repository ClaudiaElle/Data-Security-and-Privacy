from collections import Counter
import matplotlib.pyplot as plt
import math


def clean_text (text):
    text_letters = "".join(filter(str.isalpha, text)).lower()   # Rimuove ciò che non è testo e trasforma in minuscolo
    return text_letters


def frequency_histogram(text):
    cleaned_text=clean_text(text)
    counter = Counter(cleaned_text)
    letters, frequencies = zip(*sorted(counter.items()))   # Estrae le lettere e le relative occorrenze e ordina in ordine alfabetico    
    plt.bar(letters, frequencies)   # Creazione istogramma
    plt.xlabel('Letters')   # Aggiunge le etichette all'istogramma
    plt.ylabel('Frequencies')
    plt.title('Frequency Histogram')    
    plt.show()   # Mostra l'istogramma


def mgram_distribution(text, m):
    cleaned_text=clean_text(text) 
    #mgram_distribution = Counter(cleaned_text[i:i + m] for i in range(len(cleaned_text) - m + 1)) #con sovrapposizione  
    mgram_distribution = Counter(cleaned_text[i:i + m] for i in range(0, len(cleaned_text) - m + 1, m))
    blocks, b_frequencies = zip(*sorted(mgram_distribution.items()))   # Estrae le lettere e le relative occorrenze e ordina in ordine alfabetico    
    num_to_show = min(50, len(blocks))    
    plt.bar(blocks[:num_to_show], b_frequencies[:num_to_show])
    plt.xlabel('Blocks')
    plt.ylabel('Block Frequencies')
    plt.title(f'{m}-Grams Frequency Histogram')
    plt.xticks(rotation='vertical')
    plt.show()   # Mostra l'istogramma  
    return mgram_distribution


def coincidence_index(mgram_distribution):
    total_mgrams = sum(mgram_distribution.values())   # Calcola il numero totale di m-grammi
    ic = sum((frequency*(frequency-1))for frequency in mgram_distribution.values())/(total_mgrams*(total_mgrams-1))     
    # Calcola le frequenze relative, le eleva al quadrato e ne fa la somma
    return ic


def shannon_entropy(mgram_distribution):
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



