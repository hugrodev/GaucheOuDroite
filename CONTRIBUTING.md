# Contribuer

Le projet est fait pour être corrigé et complété. Une fiche = un fichier =
une pull request. Pas besoin de savoir programmer : les fiches sont des fichiers
texte que l'on peut éditer directement depuis GitHub.

## Les cinq façons d'aider

### 1. Corriger une erreur

Un chiffre faux, une date inexacte, un groupe mal classé, un lien mort.
Ouvre `fiches/AAAA-MM-JJ.json`, clique sur le crayon, corrige, décris le problème
en une phrase dans la pull request et **donne la source qui te donne raison**.

C'est la contribution la plus utile. Les erreurs factuelles sont corrigées en priorité.

### 2. Ajouter une fiche

Il manque des dates ? Crée `fiches/AAAA-MM-JJ.json` en partant de
[`scripts/modele-fiche.json`](scripts/modele-fiche.json), et lis
[SCHEMA.md](SCHEMA.md) pour le détail des champs.

Une bonne fiche répond à ces questions :

- La mesure a-t-elle vraiment été proposée ou votée ? Par qui, quand, où ?
- Si elle a été votée, quel est le numéro du scrutin à l'Assemblée ?
- Le clivage gauche/droite fonctionne-t-il, ou faut-il cocher `clivage_brouille` ?
- Quelle est la **notion** que le lecteur ne connaît probablement pas, et qui rend
  le débat compréhensible une fois expliquée ? C'est le cœur de la fiche.

### 3. Enrichir le lexique

`lexique/lexique.json` associe un terme à une définition. La page pose
automatiquement un « ? » cliquable sur la première occurrence du terme dans une
fiche — aucun marquage à faire dans les fiches elles-mêmes.

Une bonne définition fait quatre à six phrases, part de zéro, donne une date et un
ordre de grandeur, et signale les confusions courantes (la CEDH n'est pas l'Union
européenne, l'EPR le réacteur n'est pas le groupe EPR).

### 4. Cacher un œuf de Pâques

`lexique/easter-eggs.json` contient des fiches de chiffres qui s'ouvrent en
**double-cliquant** sur certains mots du site. Rien ne les signale : on tombe
dessus par hasard, et c'est le but.

Un bon œuf part d'un mot qu'on lit sans y penser — « 49.3 », « APL »,
« héritage », « pétition » — et donne l'ordre de grandeur que personne n'a en
tête. Il tient en un tableau court, se termine par une chute qui remet le chiffre
en perspective, et cite une source solide : Insee, DREES, Conseil d'analyse
économique, Cour des comptes, Assemblée nationale.

```json
"mon-oeuf": {
  "declencheurs": ["le mot", "une variante"],
  "titre": "…",
  "intro": "…",
  "colonnes": ["…", "…"],
  "tableau": [["…", "…"]],
  "chute": "…",
  "source": {"titre": "…", "url": "https://…"}
}
```

Toute fiche ajoutée ici apparaît automatiquement dans `curiosites.html`, la page
qui les rassemble : il n'y a rien à déclarer ailleurs.

La page pose l'œuf sur la première occurrence de l'un des déclencheurs, où
qu'elle se trouve. Un mot déjà défini dans le lexique peut porter les deux : le
clic simple ouvre la définition, le double-clic ouvre l'œuf.

Même exigence que pour les fiches : **un chiffre sans source ne passe pas**. Et
la chute doit éclairer, pas asséner — « les APL coûtent moins que les intérêts de
la dette » donne une échelle, « les APL ruinent le pays » est un slogan.

### 5. Améliorer la page

`index.html` contient toute la mise en forme et la logique. Pas de dépendance,
pas d'outil de compilation, pas de framework — et c'est voulu : le projet doit
rester lisible par quelqu'un qui débute. Merci de garder cette contrainte.

## Avant d'ouvrir la pull request

```bash
python3 scripts/valider.py    # vérifie le format de toutes les fiches
python3 scripts/equilibre.py  # mesure l'équilibre politique du corpus
python3 scripts/build.py      # régénère data.js
```

`data.js` est engendré à partir des fiches : **il fait partie du commit**.
Si tu l'oublies, l'intégration continue te le signalera.

Ouvre ensuite `index.html` dans un navigateur et joue ta fiche une fois. C'est le
meilleur test : on voit tout de suite si le texte est trop long, si la notion
n'explique rien, ou si la réponse est devinable sans réfléchir.

## Ce qui sera refusé

- **Une affirmation sans source.** Sans exception.
- **Un argument présenté comme un fait.** « Cette mesure ruinerait le pays » n'a
  sa place que dans `arguments_contre`, attribué à ceux qui le disent.
- **Un camp déséquilibré.** `arguments_pour` et `arguments_contre` doivent être
  aussi soignés l'un que l'autre, y compris pour une mesure que tu détestes.
  Si tu n'arrives pas à écrire honnêtement le camp d'en face, la fiche n'est pas prête.
- **Une attaque personnelle** contre un élu, une insulte, une caricature.
  On parle de mesures, pas de personnes.
- **Une mesure inventée, exagérée ou sortie de son contexte** pour rendre un camp
  ridicule. Le jeu perd tout intérêt si les fiches ne sont pas fiables.

## Équilibre du mois

C'est la partie la plus facile à rater, parce qu'elle ne se voit dans aucune fiche
prise isolément.

Le biais d'un jeu comme celui-ci ne vient presque jamais du vocabulaire. Il vient
du **choix des sujets**. On peut traiter six fiches sur l'immigration de façon
impeccablement sourcée et équilibrée, et avoir malgré tout produit un mois orienté
— parce que décider de quoi on parle est un acte plus politique que décider
comment on en parle. Ce projet s'est d'ailleurs fait prendre : sa première version
consacrait 20 % du mois au régalien et zéro fiche à l'école, à l'hôpital ou au
chômage.

D'où un script dédié :

```bash
python3 scripts/equilibre.py          # rapport complet
python3 scripts/equilibre.py 2026-10  # un mois en particulier
```

Il mesure cinq choses :

- **l'équilibre des camps** — autant de mesures de gauche que de droite ;
- **l'alternance** — si les camps alternent trop régulièrement, la réponse se
  devine à la parité du jour et le jeu n'a plus d'intérêt ;
- **l'agenda** — la part de chaque famille de sujets, et les thèmes jamais traités.
  C'est la mesure la plus importante du script ;
- **la symétrie du traitement** — les arguments pour et contre doivent peser
  autant, camp par camp. Un écart durable signale que l'un des deux est bâclé ;
- **l'occupation du terrain** — quels partis sont nommés, et à quelle fréquence.

Les seuils inscrits dans le script sont discutables, et c'est le but. S'ils sont
dépassés, il le dit sans bloquer quoi que ce soit : ce sont des arbitrages à
assumer ou à corriger, pas des erreurs.

Une règle pratique pour un mois neuf : viser quinze mesures de chaque camp, aucune
famille de sujets au-dessus d'un tiers, et une proportion de `clivage_brouille`
entre un quart et un tiers. Ce sont ces fiches-là qui apprennent le plus, mais
elles perdent leur effet si elles deviennent la majorité.

## Code de conduite

On discute des faits et des sources, pas des intentions supposées de qui les
apporte. Une pull request bien sourcée venant de quelqu'un dont on devine le vote
est une bonne pull request. Les commentaires qui cherchent la polémique plutôt que
l'exactitude sont fermés sans débat.
