#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble les fiches et le lexique en un seul fichier data.js.

    python3 scripts/build.py

À lancer après toute modification dans fiches/ ou lexique/.
"""
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
FICHES = RACINE / "fiches"
LEXIQUE = RACINE / "lexique" / "lexique.json"
SORTIE = RACINE / "data.js"

ENTETE = (
    "/* Fichier engendré par scripts/build.py — ne pas modifier à la main.\n"
    "   Les sources sont dans fiches/ et lexique/. */\n"
)


def construire() -> str:
    fichiers = sorted(FICHES.glob("*.json"))
    if not fichiers:
        sys.exit("Aucune fiche trouvée dans fiches/")

    fiches = []
    for f in fichiers:
        try:
            fiches.append(json.loads(f.read_text(encoding="utf-8")))
        except json.JSONDecodeError as e:
            sys.exit("JSON invalide dans %s : %s" % (f.name, e))
    fiches.sort(key=lambda x: x["date"])

    lexique = json.loads(LEXIQUE.read_text(encoding="utf-8"))

    return (
        ENTETE
        + "window.FICHES = "
        + json.dumps(fiches, ensure_ascii=False, indent=1)
        + ";\n\nwindow.LEXIQUE = "
        + json.dumps(lexique, ensure_ascii=False, indent=1)
        + ";\n"
    )


if __name__ == "__main__":
    contenu = construire()
    if "--verifier" in sys.argv:
        actuel = SORTIE.read_text(encoding="utf-8") if SORTIE.exists() else ""
        if actuel != contenu:
            sys.exit(
                "data.js n'est pas à jour.\n"
                "Lance « python3 scripts/build.py » et ajoute le fichier au commit."
            )
        print("data.js est à jour.")
    else:
        SORTIE.write_text(contenu, encoding="utf-8")
        n = len(json.loads(contenu.split("window.FICHES = ", 1)[1].split(";\n\nwindow.LEXIQUE", 1)[0]))
        print("data.js engendré — %d fiches." % n)
