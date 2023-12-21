from public_key_cryptography import euclidean_extended, fast_exponentiation


def fix_negative_exp(x, y, c1, c2):
    if x < 0:   # Trova l'esponente negativo, inverte il ciphertext corrispondente e cambia di segno l'esponente
        inv = euclidean_extended(c1, n)   # Inverso di c1
        c1 = inv[1] % n   # Inverso di c1 modulo n
        x = abs(x)   # Valore assoluto di x
    if y < 0:
        inv = euclidean_extended(c2, n)   # Inverso di c2
        c2 = inv[1] % n   # Inverso di c2 modulo n
        y = abs(y)   # Valore assoluto di y
    return x, y, c1, c2


def common_modulus_failure_attack(e1, e2, c1, c2):
    mcd, x, y = euclidean_extended(e1, e2)   # Trova mcd e coefficienti di Bezout
    if mcd != 1:   # Controlla che i due esponenti siano coprimi tra loro
        raise ValueError("Le due chiavi non sono coprime tra loro. Attacco non possibile.")
    x, y, c1, c2 = fix_negative_exp(x, y, c1, c2)   # Inverte il ciphertext corrispondente all'esponente negativo e fa il modulo dell'esponente
    m = (fast_exponentiation(c1, x, n) * fast_exponentiation(c2, y, n)) % n   # Ricava il messaggio originale
    return m


if __name__ == '__main__':
    n =  1309914994772590863210166992356557234456075980579048604758768205496404269677841156459642052158879494989630338961154043468325508153199153204245943547981
    c1 = 1208833588708967444709375
    c2 = 411294544478239271886338859092185183748200324266700081787109375
    e1 = 5
    e2 = 13
    m = common_modulus_failure_attack(e1, e2, c1, c2)
    print("Messaggio decifrato:", m)