# Gauche ou Droite

Un mini-jeu quotidien sur la politique française. Chaque jour, une mesure réellement
proposée ou votée : le visiteur devine si elle vient de la gauche ou de la droite,
puis la page lui montre qui la porte, comment les groupes de l'Assemblée ont voté,
et ce que veut dire la notion technique qui se cache derrière.

Le jeu est une page HTML statique, sans serveur, sans compte, sans traceur.
Les réponses du visiteur restent dans son propre navigateur.

## Ce que contient une fiche

Pour chaque date, un fichier JSON dans `fiches/` :

- **la mesure** et son contexte en une phrase ;
- **le camp** (gauche ou droite), et un drapeau `clivage_brouille` quand la mesure
  traverse les camps — dans ce cas les deux réponses comptent comme bonnes ;
- **qui la porte et qui la combat**, nommément ;
- **la position des dix groupes** de l'Assemblée, rangés de la gauche à la droite ;
- **le scrutin réel** quand il existe : intitulé, date, chiffres, détail par groupe,
  et le lien vers la page officielle de l'Assemblée ;
- **la notion expliquée** : la répartition, le taux effectif d'imposition, le
  contradictoire, le facteur de charge… ;
- **les arguments des deux camps**, sans arbitrage ;
- **les sources**.

Un lexique commun (`lexique/lexique.json`) définit les termes techniques.
La page pose automatiquement un « ? » sur leur première occurrence.

## Faire tourner le projet en local

```bash
git clone https://github.com/hugrodev/GaucheOuDroite.git
cd GaucheOuDroite
python3 scripts/build.py      # assemble fiches/ + lexique/ dans data.js
```

Puis ouvrir `index.html` dans un navigateur. Aucune dépendance, aucun serveur.

## Structure

```
index.html              la page : mise en forme et logique du jeu
data.js                 engendré par scripts/build.py — ne pas modifier à la main
fiches/AAAA-MM-JJ.json  une fiche par date
lexique/lexique.json    les définitions des termes techniques
lexique/easter-eggs.json  les fiches cachées, en double-cliquant sur certains mots
scripts/build.py        assemble les fiches en data.js
scripts/valider.py      vérifie le format de chaque fiche
scripts/equilibre.py    mesure l'équilibre politique du corpus
```

## Ajouter un mois

La page n'est pas figée sur un mois : elle lit les dates présentes dans `fiches/`
et ouvre automatiquement la fiche du jour. Le calendrier affiche le mois de la
fiche en cours et les flèches `‹ ›` naviguent entre tous les mois qui ont au moins
une fiche.

Pour ouvrir octobre, il suffit donc de déposer `fiches/2026-10-01.json` et les
suivants, puis de relancer `python3 scripts/build.py`. Rien d'autre à toucher :
ni la page, ni le calendrier, ni le compteur.

Une fiche datée du futur reste verrouillée jusqu'à son jour. On peut donc préparer
un mois entier à l'avance et le publier d'un coup : les cases s'ouvriront une par une.

**Rythme conseillé.** Une passe par mois suffit. Entre deux passes, les sujets qui
alimentent les fiches suivantes sont les mêmes que ceux qui font l'actualité :
les scrutins solennels de l'Assemblée, les annonces de campagne, les textes
budgétaires de l'automne, et les notions qui apparaissent dans le débat sans que
personne ne les explique. C'est cette dernière catégorie qui fait les meilleures
fiches.

## Contribuer

Les contributions sont l'objet même du projet : une erreur de chiffre, un scrutin
oublié, une notion mal expliquée, un camp mal attribué, une date sans fiche.
Tout passe par une pull request sur un seul fichier.

Lire [CONTRIBUTING.md](CONTRIBUTING.md) pour la marche à suivre et
[SCHEMA.md](SCHEMA.md) pour le format exact d'une fiche.

## Ligne éditoriale

Trois règles, non négociables, qui s'appliquent à toute contribution :

1. **Chaque affirmation est sourcée.** De préférence par la page « analyse du
   scrutin » de l'Assemblée nationale, le compte rendu officiel, ou le programme
   publié par le parti concerné. À défaut, un article de presse daté.
2. **Les arguments des deux camps sont présentés à parts égales**, dans les termes
   que leurs défenseurs emploieraient. « Gauche » et « droite » décrivent d'où vient
   une mesure, jamais ce qu'elle vaut.
3. **Quand le clivage ne fonctionne pas, on le dit.** C'est à cela que sert le
   drapeau `clivage_brouille` : les votes où LFI rejoint le RN, où le PS vote avec
   le bloc central, où un groupe se divise. Ces cas ne sont pas des ratés du jeu,
   ce sont les fiches les plus instructives.

## Comment ce projet essaie de rester neutre

Trois règles éditoriales ne suffisent pas : encore faut-il pouvoir vérifier
qu'elles sont tenues. `scripts/equilibre.py` mesure, à chaque fois qu'on le lance,
la répartition des camps, l'agenda des sujets, la symétrie des arguments et la
place faite à chaque parti.

Le point le moins intuitif est l'agenda. Un corpus peut être irréprochable fiche
par fiche et orienté dans son ensemble, simplement parce qu'il consacre un
cinquième de ses questions à un sujet et aucune à un autre. C'est arrivé à la
première version de ce dépôt. La correction n'a pas consisté à changer un
vocabulaire, mais à remplacer des fiches.

Si vous trouvez un déséquilibre que le script ne voit pas, ouvrez une issue :
c'est exactement le genre de contribution qui compte le plus ici.

## Licence

Le code est sous licence MIT. Le contenu des fiches et du lexique est sous licence
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.fr) : réutilisable
à condition de citer le projet et de partager les modifications dans les mêmes termes.
Voir [LICENSE](LICENSE).
