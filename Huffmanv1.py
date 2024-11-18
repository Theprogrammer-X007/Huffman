import heapq
import os

class CodageHuffman:
    def __init__(self, chemin):
        self.chemin = chemin
        self.tas = []
        self.codes = {}
        self.mapping_inverse = {}

    class NoeudTas:
        def __init__(self, caractere, frequence):
            self.caractere = caractere
            self.frequence = frequence
            self.gauche = None
            self.droite = None

        def __lt__(self, autre):
            return self.frequence < autre.frequence

        def __eq__(self, autre):
            return isinstance(autre, CodageHuffman.NoeudTas) and self.frequence == autre.frequence

    def calculer_frequences(self, texte):
        # Compte la fréquence de chaque caractère
        frequences = {}
        for caractere in texte:
            frequences[caractere] = frequences.get(caractere, 0) + 1
        return frequences

    def creer_tas(self, frequences):
        # Crée un tas de noeuds à partir des fréquences
        self.tas = [self.NoeudTas(car, freq) for car, freq in frequences.items()]
        heapq.heapify(self.tas)

    def fusionner_noeuds(self):
        # Fusionne les noeuds avec les plus basses fréquences
        while len(self.tas) > 1:
            noeud1 = heapq.heappop(self.tas)
            noeud2 = heapq.heappop(self.tas)

            # Crée un nouveau noeud parent
            noeud_fusionne = self.NoeudTas(None, noeud1.frequence + noeud2.frequence)
            noeud_fusionne.gauche = noeud1
            noeud_fusionne.droite = noeud2

            heapq.heappush(self.tas, noeud_fusionne)

    def generer_codes_recursif(self, racine, code_courant=""):
        # Génère les codes Huffman de manière récursive
        if not racine:
            return

        if racine.caractere is not None:
            self.codes[racine.caractere] = code_courant
            self.mapping_inverse[code_courant] = racine.caractere
            return

        # Parcourt l'arbre (0 à gauche, 1 à droite)
        self.generer_codes_recursif(racine.gauche, code_courant + "0")
        self.generer_codes_recursif(racine.droite, code_courant + "1")

    def generer_codes(self):
        # Génère les codes à partir de l'arbre de Huffman
        racine = heapq.heappop(self.tas)
        self.generer_codes_recursif(racine)

    def compresser(self):
        # Processus de compression principal
        nom_fichier, _ = os.path.splitext(self.chemin)
        chemin_sortie = nom_fichier + ".bin"

        with open(self.chemin, 'r') as fichier_entree, open(chemin_sortie, 'wb') as fichier_sortie:
            # Lire et préparer le texte
            texte = fichier_entree.read().rstrip()

            # Étapes de compression
            frequences = self.calculer_frequences(texte)
            self.creer_tas(frequences)
            self.fusionner_noeuds()
            self.generer_codes()

            # Encoder le texte
            texte_encode = ''.join(self.codes[caractere] for caractere in texte)

            # Ajouter du bourrage si nécessaire
            bourrage = 8 - len(texte_encode) % 8
            texte_encode += '0' * bourrage

            # Convertir en octets
            octets = bytearray(int(texte_encode[i:i+8], 2) for i in range(0, len(texte_encode), 8))
            fichier_sortie.write(bytes(octets))

        print("Compression terminée")
        return chemin_sortie

    def decompresser(self, chemin_entree):
        # Processus de décompression principal
        nom_fichier, _ = os.path.splitext(self.chemin)
        chemin_sortie = nom_fichier + "_decompresse.txt"

        with open(chemin_entree, 'rb') as fichier_entree, open(chemin_sortie, 'w') as fichier_sortie:
            # Lire et convertir les octets en bits
            bits = ''.join(bin(octet)[2:].zfill(8) for octet in fichier_entree.read())

            # Décoder le texte
            texte_decompresse = self.decoder_texte(bits)
            fichier_sortie.write(texte_decompresse)

        print("Décompression terminée")
        return chemin_sortie

    def decoder_texte(self, bits_entree):
        # Décode le texte compressé
        texte_decode = []
        code_courant = ""
        
        for bit in bits_entree:
            code_courant += bit
            if code_courant in self.mapping_inverse:
                texte_decode.append(self.mapping_inverse[code_courant])
                code_courant = ""
        
        return ''.join(texte_decode)