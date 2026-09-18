# Format d'une fiche

Un fichier par date, nommé `fiches/AAAA-MM-JJ.json`. Le nom du fichier doit être
identique au champ `date`. Encodage UTF-8.

`scripts/valider.py` vérifie tout ce qui suit.

## Champs

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `date` | texte `AAAA-MM-JJ` | oui | Le jour où la fiche s'ouvre. |
| `theme` | texte | oui | Un mot : Retraites, Fiscalité, Logement, Écologie, Immigration, Santé, Sécurité, Énergie, Budget, Europe, Institutions, Société, Travail, Salaires, Agriculture, Services publics. |
| `mesure` | texte | oui | L'énoncé montré au joueur. Une phrase, à l'infinitif de préférence. C'est la question du jeu : elle ne doit pas trahir la réponse. |
| `contexte` | texte | oui | Une ou deux phrases : d'où vient la mesure, quand, dans quel texte. |
| `camp` | `"gauche"` ou `"droite"` | oui | D'où vient la mesure, pas ce qu'elle vaut. |
| `clivage_brouille` | booléen | oui | `true` si la mesure traverse les camps. Les deux réponses comptent alors comme bonnes. |
| `porteurs` | liste de textes | oui, ≥ 2 | Qui la défend. Nomme les partis et les personnes. |
| `opposants` | liste de textes | oui, ≥ 2 | Qui la combat. |
| `groupes` | objet | oui | La position des dix groupes. Voir ci-dessous. |
| `scrutin` | objet ou `null` | oui | Le vote réel, s'il existe. Voir ci-dessous. |
| `notion` | objet | oui | `terme` et `explication`. Le cœur pédagogique de la fiche. |
| `arguments_pour` | liste de textes | oui, ≥ 2 | Les arguments de ceux qui la défendent. |
| `arguments_contre` | liste de textes | oui, ≥ 2 | Ceux de ses adversaires. |
| `a_retenir` | texte | oui | Ce que la fiche apprend et qu'on ne devinait pas. |
| `sources` | liste d'objets | oui, ≥ 1 | `titre` et `url` (http ou https). |

Les textes acceptent quelques balises HTML simples : `<b>`, `<i>`, `<br>`.
Rien d'autre.

## `groupes`

Les dix groupes de l'Assemblée, rangés de la gauche à la droite dans la page.
Les dix clés sont obligatoires, même quand la position est inconnue.

```json
"groupes": {
  "LFI": "p27", "PCF": "x",  "ÉCO": "c14", "PS": "c17", "REN": "c16",
  "MoDem": "c2", "HOR": "d", "LR": "p6",   "UDR": "p4", "RN": "p56"
}
```

Une valeur = une lettre, éventuellement suivie du nombre de députés.

| Lettre | Sens |
|---|---|
| `p` | Pour |
| `c` | Contre |
| `a` | Abstention |
| `d` | Divisé — pas de position majoritaire nette dans le groupe |
| `x` | Pas de position connue, ou groupe non concerné |

Le nombre ne se met que s'il vient d'un scrutin réel : `p27` signifie vingt-sept
députés du groupe ont voté pour. Pour une mesure jamais mise aux voix, on donne la
lettre seule, et la page précise d'elle-même qu'il s'agit de positions déclarées.

Rappel des sigles : `ÉCO` Les Écologistes · `PCF` groupe Gauche démocrate et
républicaine · `REN` Ensemble pour la République (Renaissance) · `HOR` Horizons ·
`LR` Droite républicaine · `UDR` Union des droites.

## `scrutin`

`null` si la mesure n'a jamais été mise aux voix. Sinon :

```json
"scrutin": {
  "intitule":    "Article 15 ter du projet de loi de simplification — suppression des ZFE",
  "reference":   "28 mai 2025 · adopté · scrutin n°2190",
  "pour":        98,
  "contre":      51,
  "abstentions": 6,
  "detail":      "<b>Pour :</b> RN 56, <b>LFI 27</b>…<br><b>Contre :</b> PS 17…",
  "url":         "https://www.assemblee-nationale.fr/dyn/17/scrutins/2190"
}
```

`pour`, `contre` et `abstentions` sont des entiers. Mets `0` partout quand tu
documentes un épisode parlementaire sans décompte exploitable (une commission
mixte paritaire, un vote au Sénat, un texte en cours d'examen) : la page affiche
alors le texte de `detail` sans barre chiffrée.

Les chiffres se relèvent sur la page « analyse du scrutin » du site de
l'Assemblée. **Si une ligne du tableau officiel est illisible ou manquante,
laisse le groupe de côté plutôt que d'estimer.**

## `notion`

```json
"notion": {
  "terme": "L'écologie punitive",
  "explication": "L'expression désigne les politiques environnementales dont le coût tombe d'abord sur…"
}
```

Entre 400 et 900 signes. C'est ce que le joueur retient : pas un résumé de la
mesure, mais le concept qui rend le désaccord compréhensible. Écris-la pour
quelqu'un qui n'a jamais ouvert un budget de sa vie, sans condescendance et sans
jargon non expliqué. Une date, un ordre de grandeur et un contre-exemple valent
mieux qu'une définition abstraite.

## Fiche minimale

```json
{
  "date": "2026-10-01",
  "theme": "Fiscalité",
  "mesure": "…",
  "contexte": "…",
  "camp": "gauche",
  "clivage_brouille": false,
  "porteurs": ["…", "…"],
  "opposants": ["…", "…"],
  "groupes": {"LFI":"p","PCF":"p","ÉCO":"p","PS":"p","REN":"c","MoDem":"c","HOR":"c","LR":"c","UDR":"c","RN":"c"},
  "scrutin": null,
  "notion": {"terme": "…", "explication": "…"},
  "arguments_pour": ["…", "…"],
  "arguments_contre": ["…", "…"],
  "a_retenir": "…",
  "sources": [{"titre": "…", "url": "https://…"}]
}
```
