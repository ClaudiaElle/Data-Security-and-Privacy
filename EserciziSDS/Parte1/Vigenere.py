from collections import Counter



def  trigrams_frequencies(ciphertext):
    range_limit = (len(ciphertext)-len(ciphertext)%3)-1
    trigram_frequencies = Counter(ciphertext[i:i + 3] for i in range(0, range_limit, 3))
    return trigram_frequencies


def equals_trigrams_positions(ciphertext):
    range_limit = (len(ciphertext)-len(ciphertext)%3)-1
    trigrams = [ciphertext[i:i + 3] for i in range(0, range_limit, 3)]
    print(trigrams)
    trigram_positions = {}
    for index, trigram in enumerate(trigrams):
        if trigram in trigram_positions:
            trigram_positions[trigram].append(index*3)
        else:
            trigram_positions.update({trigram: [index*3]})
    print(trigram_positions)
    return trigram_positions

def trigram_distances(ciphertext):
    trigrams_positions = equals_trigrams_positions(ciphertext)


    



if __name__ == '__main__':
    c="ZYIVIUPYKFJZLKRRIFVJMTGBLTSAVYEPXFWYIJTUKSSXHKRJOKLKEYEBTVQGRCAYQVHYXXAVMYXGX"\
    "NIZVRYRWZOBJYMYKXOHTUETHLOHTULOQYEYLGYYLKDVTKSGDUNRUWMTGXENYZRMZOSPUJMZCZHRGZ"\
    "VGVUUAJYMSFKCBSZRMTGIALLPRCANLOVPJMTGOKWSXINEFRZTVIJFEKVXUSTEFOUIZLKSRTJIZLGT"\
    "QOJGUZKRVTXECEETBHIIGGNTUOJFGVXIRXNSAPJSBSVLUARIOKIEZINIZCRWISSPRRCMTKHUGNVOT"\
    "ICIGCRWGFYUEJVZKROFUKUMJJONQGWPGAONGNVTXSMRNSNLOGNEAGSPKHNIZZFFXIGKGNISAKNHRQ"\
    "EICLKDTGZRTSZHVTXFAXJEPXVEYMTGYEIIGPOSGOTWAVXOHTUMTKYTUKIIISXDVTXGUYRDBTCCIST"\
    "TNOEGUQVLRZVMTJURZGKMURLOEVFMTXYOSBZICAOTUOEEIIXTNOEJOROTRFFRKERLGNVVKAGSGUVW"\
    "IEVEGUNEYEXETOFRCLKRRNZWBMKWBLKLKGOTLCFYRHHESACPUJJIFZFVZMUNFGEHUQOSFOFRYETDJ"\
    "ULPJIBEAZLERPEFNJVXUFRAPQYIYXKPCKUFGGQFEUDXNIIOETVVNERFQOJTOVOTRJYERJGMHYVHCL"\
    "GTUGULKLUPRJKSLMTDNJFSXEZTUKVHMIUFGNVQUHKLZGIOKHKXVZKLXSAGUCYMILNEPULPJAGLXUL"\
    "XORZOEKRPOXE"
    equals_trigrams_positions(c)