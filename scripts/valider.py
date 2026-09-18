#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie que chaque fiche respecte le format attendu.

    python3 scripts/valider.py

Lancé automatiquement sur chaque pull request.
"""
import json
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
FICHES = RACINE / "fiches"
LEXIQUE = RACINE / "lexique" / "lexique.json"

GROUPES = ["LFI", "PCF", "ÉCO", "PS", "REN", "MoDem", "HOR", "LR", "UDR", "RN"]
POSITIONS = set("pcadx")
CAMPS = {"gauche", "droite"}

OBLIGATOIRES = [
    "date", "theme", "mesure", "contexte", "camp", "clivage_brouille",
    "porteurs", "opposants", "groupes", "notion",
    "arguments_pour", "arguments_contre", "a_retenir", "sources",
]

RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_POS = re.compile(r"^[pcadx]\d*$")


def verifier_fiche(chemin, erreurs):
    nom = chemin.name
    def err(m):
        erreurs.append("%s : %s" % (nom, m))

    try:
        f = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err("JSON invalide (%s)" % e)
        return

    for k in OBLIGATOIRES:
        if k not in f:
            err("champ manquant « %s »" % k)
    if erreurs and any(nom in e for e in erreurs[-len(OBLIGATOIRES):]):
        pass

    date = f.get("date", "")
    if not RE_DATE.match(str(date)):
        err("date « %s » : format attendu AAAA-MM-JJ" % date)
    elif nom != date + ".json":
        err("le nom du fichier doit être %s.json" % date)

    if f.get("camp") not in CAMPS:
        err("camp doit valoir « gauche » ou « droite »")
    if not isinstance(f.get("clivage_brouille"), bool):
        err("clivage_brouille doit être true ou false")

    g = f.get("groupes", {})
    if sorted(g.keys()) != sorted(GROUPES):
        err("groupes doit contenir exactement : %s" % ", ".join(GROUPES))
    else:
        for cle, val in g.items():
            if not RE_POS.match(str(val)):
                err("groupes.%s = « %s » : attendu p/c/a/d/x suivi d'un nombre facultatif" % (cle, val))

    for cle in ("porteurs", "opposants", "arguments_pour", "arguments_contre"):
        v = f.get(cle)
        if not isinstance(v, list) or len(v) < 2:
            err("%s doit être une liste d'au moins deux entrées" % cle)

    n = f.get("notion", {})
    if not n.get("terme") or not n.get("explication"):
        err("notion doit contenir « terme » et « explication »")
    elif len(n["explication"]) < 200:
        err("notion.explication est trop courte : vise 400 à 900 signes")

    s = f.get("sources", [])
    if not isinstance(s, list) or not s:
        err("au moins une source est obligatoire")
    else:
        for i, src in enumerate(s):
            if not isinstance(src, dict) or not src.get("titre") or not src.get("url"):
                err("sources[%d] doit avoir « titre » et « url »" % i)
            elif not str(src["url"]).startswith("http"):
                err("sources[%d].url doit être une adresse http(s)" % i)

    sc = f.get("scrutin")
    if sc is not None:
        if not isinstance(sc, dict):
            err("scrutin doit être un objet ou null")
        else:
            for k in ("intitule", "reference", "detail", "url"):
                if not sc.get(k):
                    err("scrutin.%s manquant" % k)
            for k in ("pour", "contre", "abstentions"):
                if not isinstance(sc.get(k), int):
                    err("scrutin.%s doit être un nombre entier (0 si inconnu)" % k)


def main():
    erreurs = []
    fichiers = sorted(FICHES.glob("*.json"))
    if not fichiers:
        sys.exit("Aucune fiche dans fiches/")

    dates = []
    for c in fichiers:
        verifier_fiche(c, erreurs)
        dates.append(c.stem)
    doublons = {d for d in dates if dates.count(d) > 1}
    if doublons:
        erreurs.append("dates en double : %s" % ", ".join(sorted(doublons)))

    try:
        lex = json.loads(LEXIQUE.read_text(encoding="utf-8"))
        for terme, v in lex.items():
            if not v.get("titre") or not v.get("definition"):
                erreurs.append("lexique : « %s » doit avoir « titre » et « definition »" % terme)
    except json.JSONDecodeError as e:
        erreurs.append("lexique/lexique.json invalide : %s" % e)

    if erreurs:
        print("%d problème(s) :\n" % len(erreurs))
        for e in erreurs:
            print("  - " + e)
        sys.exit(1)

    print("%d fiches valides, %d termes au lexique." % (len(fichiers), len(lex)))


if __name__ == "__main__":
    main()
