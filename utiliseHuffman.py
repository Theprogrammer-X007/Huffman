from Huffmanv1 import CodageHuffman

path="Mail.txt"

# Compression
compresseur = CodageHuffman(path)
fichier_compresse = compresseur.compresser()

# Décompression
decompresseur = CodageHuffman("mon_fichier.txt")
fichier_decompresse = decompresseur.decompresser(fichier_compresse)