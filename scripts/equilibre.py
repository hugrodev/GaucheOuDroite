#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mesure l'équilibre politique du corpus de fiches.

    python3 scripts/equilibre.py            # rapport complet
    python3 scripts/equilibre.py --strict   # sort en erreur si un seuil est dépassé
    python3 scripts/equilibre.py 2026-09    # se limite à un mois

Le biais d'un jeu comme celui-ci ne vient presque jamais du vocabulaire :
il vient du choix des sujets. Traiter impeccablement six fiches sur
l'immigration et aucune sur l'école, c'est déjà prendre parti, même en citant
ses sources à chaque ligne. Ce script rend cet arbitrage visible.
"""
import json
import pathlib
import sys
from collections import Counter, defaultdict

RACINE = pathlib.Path(__file__).resolve().parent.parent
FICHES = RACINE / "fiches"

# Regroupement des thèmes en familles. Un thème absent d'ici tombe dans « Autres ».
FAMILLES = {
    "Régalien": ["Immigration", "Sécurité", "Justice"],
    "Économie et fiscalité": ["Fiscalité", "Budget", "Travail", "Salaires", "Emploi", "Industrie"],
    "Social et services publics": ["Santé", "Logement", "Retraites", "Services publics", "Éducation"],
    "Écologie et énergie": ["Écologie", "Énergie", "Agriculture", "Transports"],
    "Institutions, Europe, société": ["Institutions", "Europe", "Société"],
}

# Seuils indicatifs, discutables — c'est le but qu'ils soient discutés.
SEUILS = {
    "ecart_camps": 2,        # écart maximal entre fiches de gauche et de droite
    "part_regalien": 0.20,   # part maximale du régalien dans le corpus
    "asymetrie_args": 0.15,  # écart maximal entre longueur des arguments pour et contre
    "alternance": 0.70,      # part maximale d'alternances gauche/droite consécutives
}


def charger(prefixe=None):
    f = []
    for c in sorted(FICHES.glob("*.json")):
        if prefixe and not c.stem.startswith(prefixe):
            continue
        f.append(json.loads(c.read_text(encoding="utf-8")))
    return sorted(f, key=lambda x: x["date"])


def signes(liste):
    return sum(len(s) for s in liste)


def barre(part, largeur=28):
    n = int(round(part * largeur))
    return "█" * n + "·" * (largeur - n)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    fiches = charger(args[0] if args else None)
    if not fiches:
        sys.exit("Aucune fiche à analyser.")

    total = len(fiches)
    alertes = []
    print("\n%d fiches analysées, du %s au %s\n" % (total, fiches[0]["date"], fiches[-1]["date"]))

    # --- 1. équilibre des camps ---
    g = sum(1 for f in fiches if f["camp"] == "gauche")
    d = total - g
    print("CAMPS")
    print("  gauche %2d   droite %2d   écart %d" % (g, d, abs(g - d)))
    if abs(g - d) > SEUILS["ecart_camps"]:
        alertes.append("écart entre camps trop élevé (%d)" % abs(g - d))

    # --- 2. alternance : la réponse doit rester imprévisible ---
    suite = [f["camp"] for f in fiches]
    bascules = sum(1 for i in range(1, len(suite)) if suite[i] != suite[i - 1])
    part = bascules / max(1, len(suite) - 1)
    print("  alternance %.0f%% (%s)" % (part * 100,
          "".join("G" if c == "gauche" else "D" for c in suite)))
    if part > SEUILS["alternance"]:
        alertes.append("la réponse devient devinable : %.0f%% d'alternance" % (part * 100))

    # --- 3. agenda : de quoi parle-t-on, et dans quelle proportion ---
    print("\nAGENDA — la part de chaque famille de sujets")
    place = {}
    for fam, ths in FAMILLES.items():
        for t in ths:
            place[t] = fam
    parfam = defaultdict(lambda: [0, 0])
    for f in fiches:
        fam = place.get(f["theme"], "Autres")
        parfam[fam][0 if f["camp"] == "gauche" else 1] += 1
    for fam in sorted(parfam, key=lambda k: -sum(parfam[k])):
        gg, dd = parfam[fam]
        n = gg + dd
        print("  %-30s %s %2d  %3.0f%%   (g %d / d %d)" % (fam, barre(n / total), n, n / total * 100, gg, dd))

    reg = sum(parfam["Régalien"])
    if reg / total > SEUILS["part_regalien"]:
        alertes.append("le régalien occupe %.0f%% du corpus (seuil %.0f%%)"
                       % (reg / total * 100, SEUILS["part_regalien"] * 100))

    absents = [t for t in sorted(place) if t not in {f["theme"] for f in fiches}]
    if absents:
        print("\n  Thèmes jamais traités : " + ", ".join(absents))

    # --- 4. symétrie du traitement ---
    print("\nTRAITEMENT — longueur moyenne des arguments, en signes")
    for camp in ("gauche", "droite"):
        sub = [f for f in fiches if f["camp"] == camp]
        if not sub:
            continue
        p = signes([a for f in sub for a in f["arguments_pour"]]) / len(sub)
        c = signes([a for f in sub for a in f["arguments_contre"]]) / len(sub)
        ecart = (c - p) / p if p else 0
        print("  mesures de %-7s  pour %4.0f   contre %4.0f   écart %+.0f%%" % (camp, p, c, ecart * 100))
        if abs(ecart) > SEUILS["asymetrie_args"]:
            alertes.append("mesures de %s : %+.0f%% d'écart entre pour et contre" % (camp, ecart * 100))

    # --- 5. qui occupe le terrain ---
    print("\nPARTIS — nombre de mentions dans les porteurs et les opposants")
    cites = Counter()
    for f in fiches:
        for x in f["porteurs"] + f["opposants"]:
            for sigle in ("LFI", "PCF", "Écologistes", "PS", "Renaissance", "MoDem",
                          "Horizons", "LR", "UDR", "RN", "Reconquête"):
                if sigle in x:
                    cites[sigle] += 1
    if cites:
        haut = cites.most_common(1)[0][1]
        for sigle, n in cites.most_common():
            print("  %-13s %s %2d" % (sigle, barre(n / haut, 20), n))

    # --- verdict ---
    print()
    if alertes:
        print("%d point(s) à surveiller :" % len(alertes))
        for a in alertes:
            print("  ! " + a)
        print("\nCe ne sont pas des erreurs : ce sont des arbitrages à assumer ou à corriger.")
        if strict:
            sys.exit(1)
    else:
        print("Aucun seuil dépassé.")
    print()


if __name__ == "__main__":
    main()
