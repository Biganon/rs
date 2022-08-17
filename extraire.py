import sys
from bs4 import BeautifulSoup as bs
import re

fichiers = sys.argv[1:]

def processer(fichier):
    with open(fichier, "r") as f:
        contenu_brut = f.read()
    soupe = bs(contenu_brut, features="html.parser")

    # Effacer toutes les notes de bas de page :
    for div in soupe.find_all("div", {"class":"footnotes"}):
        div.decompose()

    # Effacer tous les exposants :
    for sup in soupe.find_all("sup"):
        sup.decompose()

    # Effacer tous les tableaux :
    for table in soupe.find_all("table"):
        table.decompose()

    # Récupérer les balises contenant du texte matériellement important :
    sortie = ""
    textes = [b.text.strip() for b in soupe.find_all(["p", "dd"])]
    for texte in textes:
        texte = texte.replace("\u00ad", "") # effacer les "soft dashes"
        if not texte: # texte vide
            continue
        if texte == "…":
            continue

        if texte[-1] in ".!":
            sortie += f"{texte}\n"
        else:
            sortie += f"{texte} "

    print(sortie)
if __name__ == "__main__":
    for fichier in fichiers:
        processer(fichier)