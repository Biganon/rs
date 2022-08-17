import markovify
from pygrammalecte import grammalecte_text
import language_tool_python
from time import time

tool = language_tool_python.LanguageTool('fr-CH')

CHECK_GRAMMALECTE = True
CHECK_LANGUAGETOOL = True

with open("tout2.txt", "r") as f:
    corpus = f.read()

modeles = []

for i in range(1, 6):
    fichier_json = f"modele{i}.json"
    debut = time()
    try:
        with open(fichier_json, "r") as f:
            json = f.read()
        modele = markovify.Text.from_json(json)
    except Exception:
        modele = markovify.Text(corpus, state_size=i)
        json = modele.to_json()
        with open(fichier_json, "w") as f:
            f.write(json)
    modeles.append(modele)
    fin = time()
    delta = fin - debut
    print(f"Modèle (état = {i}) généré en {delta} secondes")

while True:
    etat = int(input("Taille de l'état : "))
    while True:
        essai = modeles[etat-1].make_sentence()
        try:
            if CHECK_GRAMMALECTE and next(grammalecte_text(essai), None):
                continue
            if CHECK_LANGUAGETOOL and tool.check(essai):
                continue
        except Exception:
            continue
        if not essai:
            continue
        break
    print(f"{essai}")