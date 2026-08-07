# SPEC.md

Version : 1.0 (Draft)
Statut : En cours de rédaction

---

# 1. Présentation

## 1.1 Objet du projet

Ce projet a pour objectif de fournir un environnement complet de développement, de validation, de compilation et de synchronisation de types de notes Anki.

Il permet de développer les modèles de cartes (templates HTML, feuilles de style CSS, ressources, métadonnées, etc.) comme un véritable projet logiciel, en bénéficiant notamment :

- du contrôle de version Git ;
- d'une organisation claire des sources ;
- d'un système de compilation ;
- de validations automatiques ;
- de tests ;
- d'un déploiement automatisé vers un ou plusieurs profils Anki.

Le projet ne stocke aucune carte Anki.

Il ne gère que la définition des types de notes.

---

# 2. Motivation

Les types de notes Anki présentent plusieurs limitations lorsqu'ils sont développés directement dans l'éditeur intégré.

En particulier :

- absence de contrôle de version ;
- édition peu confortable ;
- impossibilité de partager des fragments HTML ;
- duplication des modèles entre plusieurs profils ;
- absence de validation avant installation ;
- difficulté à revenir à une version antérieure.

Ce projet résout ces limitations en considérant les types de notes comme des artefacts logiciels.

---

# 3. Philosophie

Le projet repose sur plusieurs principes fondamentaux.

## 3.1 Git est la source de vérité

Les sources sont exclusivement stockées dans le dépôt Git.

Les modifications ne doivent jamais être effectuées directement dans Anki.

Anki est uniquement une cible de déploiement.

---

## 3.2 Les sources sont immuables

Les fichiers contenus dans le dossier `project/` constituent les sources des types de notes.

Ils ne sont jamais modifiés automatiquement.

Toute transformation est réalisée dans le dossier `build/`.

---

## 3.3 Les profils Anki sont autonomes

Chaque profil Anki contient sa propre copie :

- des templates ;
- des feuilles de style ;
- des ressources.

Le projet ne crée jamais de dépendance permanente entre un profil Anki et le dépôt Git.

Chaque profil doit continuer à fonctionner normalement même si le dépôt est supprimé.

---

## 3.4 Le projet est déclaratif

Les sources décrivent uniquement ce qui doit être obtenu.

Elles ne décrivent jamais comment l'obtenir.

Le moteur décide de la manière de produire le résultat.

---

## 3.5 L'add-on est une interface

L'add-on Anki ne contient aucune logique métier.

Toutes les opérations sont réalisées par le moteur.

L'add-on se limite à :

- lancer les opérations ;
- afficher leur progression ;
- afficher leur résultat.

---

## 3.6 Le moteur est indépendant

Le moteur doit pouvoir fonctionner :

- sans Anki ;
- sans interface graphique ;
- depuis une ligne de commande ;
- dans un environnement de test.

---

# 4. Objectifs

Le projet poursuit les objectifs suivants.

## 4.1 Versionnement

Tous les éléments d'un type de note doivent être versionnables avec Git.

---

## 4.2 Lisibilité

Les sources doivent être agréables à modifier dans un éditeur de texte.

Aucun élément ne doit être caché dans une base SQLite.

---

## 4.3 Réutilisabilité

Le projet doit permettre la réutilisation de code grâce notamment :

- aux partials HTML ;
- aux feuilles de style communes ;
- aux ressources partagées.

---

## 4.4 Validation

Aucune modification ne doit être envoyée à Anki tant que les sources ne sont pas valides.

---

## 4.5 Déploiement

Le déploiement doit être automatisé.

Le moteur doit être capable de synchroniser :

- le profil courant ;
- plusieurs profils.

---

## 4.6 Performances

Une synchronisation ne doit mettre à jour que les éléments ayant réellement changé.

Le projet utilise pour cela un système de hachage.

---

# 5. Hors périmètre

Le projet ne gère pas :

- les cartes ;
- les statistiques Anki ;
- les médias des cartes (hors ressources appartenant aux types de notes) ;
- la synchronisation AnkiWeb ;
- les paquets (.apkg) ;
- les decks ;
- les tags ;
- les révisions.

Le projet ne remplace pas Anki.

Il complète Anki.

---

# 6. Public visé

Le projet s'adresse principalement :

- aux développeurs de types de notes ;
- aux utilisateurs possédant plusieurs profils Anki ;
- aux utilisateurs souhaitant bénéficier d'un véritable environnement de développement.

---

# 7. Terminologie

Dans toute la documentation, les termes suivants ont une signification précise.

## Projet

Ensemble complet des sources versionnées.

---

## Type de note

Définition complète d'un modèle Anki.

Il comprend notamment :

- les templates ;
- les feuilles de style ;
- les métadonnées ;
- les ressources.

---

## Template

Modèle HTML utilisé par Anki.

Un type de note peut contenir plusieurs templates.

---

## Partial

Fragment HTML réutilisable.

Les partials ne sont jamais envoyés directement à Anki.

Ils sont résolus lors de la compilation.

---

## Compilation

Transformation des sources du dossier `project/` vers les fichiers produits dans `build/`.

---

## Synchronisation

Copie des fichiers compilés vers un ou plusieurs profils Anki.

---

## Profil

Profil utilisateur Anki.

Chaque profil possède :

- sa collection ;
- son dossier media ;
- ses propres types de notes.

---

## Workspace

Racine du projet.

---

# 8. Principes d'architecture

Le pipeline général est le suivant.

```

project/
│
▼

Validation
│
▼

Compilation
│
▼

build/
│
▼

Synchronisation
│
▼

Profil(s) Anki

```

Chaque étape possède une responsabilité unique.

Une étape ne connaît pas les détails internes des autres.

---

# 9. Principes de conception

Le projet applique les principes suivants.

## Responsabilité unique

Chaque module possède une seule responsabilité.

---

## Faible couplage

Les modules doivent dépendre les uns des autres le moins possible.

---

## Forte cohésion

Les éléments appartenant à un même domaine doivent être regroupés.

---

## Déterminisme

Une compilation réalisée deux fois avec les mêmes sources doit produire exactement les mêmes résultats.

---

## Idempotence

Lancer deux fois une synchronisation ne doit provoquer aucune modification supplémentaire.

---

## Reproductibilité

Le dossier `build/` doit pouvoir être recréé intégralement à partir de `project/`.

---

## Traçabilité

Toute modification installée dans un profil doit pouvoir être reliée à une version des sources.

---

## Testabilité

Chaque module doit pouvoir être testé indépendamment.

Le moteur ne doit dépendre ni de l'interface graphique ni d'Anki pour être testé.

---

# 10. Contraintes

Le projet doit fonctionner sur les systèmes officiellement supportés par Anki.

Il ne doit jamais modifier directement la base SQLite de la collection.

Toutes les interactions avec Anki doivent passer par son API Python officielle.

Le projet doit minimiser ses dépendances externes.

Les bibliothèques de la bibliothèque standard Python doivent être privilégiées lorsque cela est raisonnable.

---

# 11. Invariants

Les propriétés suivantes doivent toujours être vraies.

- `project/` n'est jamais modifié automatiquement.
- `build/` peut être supprimé à tout moment.
- Git constitue toujours la source de vérité.
- Les profils Anki restent autonomes.
- Le moteur ne dépend pas de l'interface graphique.
- Les validations sont exécutées avant toute synchronisation.
- Une synchronisation ne modifie que les éléments réellement différents.
- Les erreurs ne doivent jamais laisser un état incohérent lorsque cela peut être évité.

---

# 12. Organisation du dépôt

Le dépôt constitue l'unique source de vérité du projet.

Tous les fichiers nécessaires au développement des types de notes sont contenus dans ce dépôt.

Aucun fichier présent dans les profils Anki ne doit être considéré comme une source.

L'organisation suivante est adoptée.

```
workspace/
│
├── src/
├── project/
├── build/
├── addon/
├── tests/
├── docs/
├── README.md
└── pyproject.toml
```

---

# 13. Description des dossiers

## project/

Contient exclusivement les sources des types de notes.

Ce dossier est modifié uniquement par le développeur.

Aucun outil ne doit modifier automatiquement son contenu.

---

## build/

Contient les fichiers produits par le moteur.

Ce dossier est entièrement jetable.

Il peut être supprimé à tout moment.

Une nouvelle compilation doit permettre de le reconstruire intégralement.

---

## src/anki_note_types/

Contient toute la logique métier.

Ce dossier ne dépend ni d'Anki, ni de l'interface graphique.

---

## addon/

Contient uniquement l'extension Anki.

L'extension agit comme une interface graphique vers le moteur.

---

## tests/

Contient tous les tests automatisés.

---

## docs/

Documentation complémentaire.

Exemples :

- ADR
- DECISIONS
- guides
- captures d'écran

---

# 14. Structure du dossier project

```
project/
│
├── css/
│
├── partials/
│
├── assets/
│
└── note-types/
```

---

# 15. css/

Contient les feuilles de style communes.

Exemple :

```
css/
    common.css
    dark.css
    print.css
```

Le moteur copie les feuilles nécessaires dans les profils Anki.

---

# 16. partials/

Contient les fragments HTML réutilisables.

Exemple :

```
partials/

    header.html

    footer.html

    pronunciation.html

    examples.html
```

Les partials ne sont jamais envoyés directement vers Anki.

Ils sont toujours résolus durant la compilation.

---

# 17. assets/

Contient les ressources appartenant aux types de notes.

Exemples :

- icônes
- images
- sons
- polices

Ces ressources pourront être copiées dans les profils si elles sont référencées.

---

# 18. note-types/

Chaque sous-dossier représente un projet de type de note.

Exemple :

```
note-types/

    Vocabulary/

    Grammar/

    Kanji/

    ArabicRoot/
```

Le nom du dossier ne constitue pas le nom officiel du type de note.

Le nom officiel est défini dans metadata.json.

---

# 19. Structure d'un projet

Chaque type de note possède la structure suivante.

```
Vocabulary/

    metadata.json

    templates/

    README.md
```

---

# 20. templates/

Ce dossier contient tous les templates du type de note.

Exemple :

```
templates/

    Recognition/

        template.json

        front.html

        back.html

    Production/

        front.html

        back.html
```

Cette organisation permet à un même type de note de posséder plusieurs templates.

Le moteur ne limite pas leur nombre.

Chaque répertoire de template contient un `template.json`. Son schéma est
versionné par `schemaVersion` et sa référence est
`project/schema/template.schema.json`.

---

# 21. metadata.json

Chaque projet possède exactement un fichier metadata.json.

Ce fichier constitue le manifeste du projet.

Il décrit toutes les informations nécessaires à sa compilation.

---

# 22. Exemple minimal

```
{
    "schemaVersion": 1,

    "name": "Vocabulary",

    "stylesheet": "common.css",

    "fields": ["Word", "Definition"]
}
```

---

# 23. Principes

Le manifeste est :

- lisible ;
- déclaratif ;
- indépendant d'Anki autant que possible.

Il ne contient jamais d'informations calculables.

---

# 24. Version du schéma

Le champ

```
schemaVersion
```

est obligatoire.

Il permet au moteur de faire évoluer le format.

---

# 25. Nom

Le champ

```
name
```

est obligatoire.

Il correspond au nom officiel du type de note dans Anki.

Deux projets ne peuvent jamais posséder le même nom.

---

# 26. Stylesheet

Le champ

```
stylesheet
```

désigne la feuille de style principale.

Exemple :

```
common.css
```

Le moteur vérifie automatiquement son existence.

---

## Champs

Le champ `fields` est obligatoire. Il liste, dans leur ordre Anki, les champs
du type de note. Toute migration de ces champs reste une opération explicite.

---

# 27. Évolutivité

Le manifeste pourra être enrichi dans les versions futures.

Par exemple :

- version
- auteur
- description
- dépendances
- champs
- options

Les nouveaux champs devront toujours être optionnels tant que cela est possible.

---

# 28. README.md

Chaque projet peut contenir un README.

Il documente :

- le fonctionnement du type ;
- les choix de conception ;
- les conventions éventuelles.

Ce fichier n'est jamais utilisé par le moteur.

---

# 29. Ressources interdites

Le projet ne doit jamais contenir :

- collection.anki2
- fichiers SQLite
- profils Anki
- médias utilisateurs
- statistiques

---

# 30. build/

Après compilation, la structure est proche de celle des sources.

Exemple :

```
build/

    Vocabulary/

        metadata.json

        templates/

        hash.json

    Grammar/

        ...
```

Tous les partials ont alors été résolus.

Tous les templates sont définitifs.

---

# 31. Fichiers générés

Les fichiers générés ne doivent jamais être modifiés manuellement.

Toute modification serait perdue lors de la prochaine compilation.

---

# 32. Principe de compilation

Le moteur transforme :

```
project/
```

vers

```
build/
```

sans jamais modifier les sources.

Le résultat est entièrement déterministe.

---

# 33. Déterminisme

Deux compilations successives des mêmes sources doivent produire des fichiers strictement identiques.

Y compris :

- ordre des attributs JSON
- encodage
- fins de ligne
- espaces significatifs

Cette propriété garantit la stabilité des hashes.

---

# 34. Encodage

Tous les fichiers texte utilisent :

UTF-8

sans BOM.

---

# 35. Fin de ligne

Le projet adopte :

LF

sur toutes les plateformes.

---

# 36. Convention de nommage

Les noms de fichiers doivent être explicites.

Exemples :

```
recognition.front.html

recognition.back.html
```

Préférer les noms descriptifs aux suffixes numériques.

---

# 37. Interdictions

Les noms suivants sont déconseillés :

```
front2.html

test.html

new.html

copie.html
```

Ils ne décrivent pas leur rôle.

---

# 38. Responsabilité

Chaque fichier possède une responsabilité unique.

Exemples :

Un template ne contient pas de CSS.

Une feuille CSS ne contient pas de HTML.

Le manifeste ne contient pas de contenu HTML.

---

# 39. Vue d'ensemble du moteur

Le moteur transforme les sources du projet en une représentation prête à être installée dans un ou plusieurs profils Anki.

Le moteur est constitué d'une succession d'étapes indépendantes.

Chaque étape possède une responsabilité unique.

Une étape ne connaît jamais les détails d'implémentation des autres.

---

# 40. Pipeline général

Le pipeline est le suivant.

```

Workspace

↓

Loader

↓

Validator

↓

Compiler

↓

Hasher

↓

Generated/

↓

Synchronizer

↓

Profil(s) Anki

↓

Report

```

Chaque étape est indépendante.

Le résultat d'une étape constitue l'entrée de la suivante.

---

# 41. Loader

Le Loader lit les sources du projet.

Il ne réalise aucune transformation.

Il construit uniquement une représentation mémoire.

Le Loader ne valide pas les données.

---

Responsabilités :

- découverte des projets
- lecture des manifests
- lecture des templates
- lecture des partials
- lecture des feuilles de style
- lecture des ressources

---

Le Loader ne connaît pas Anki.

---

# 42. Validator

Le Validator vérifie que les sources sont cohérentes.

Il ne modifie jamais les données.

---

Exemples de validations :

- fichiers manquants

- manifeste invalide

- template absent

- stylesheet absente

- nom de type dupliqué

- template dupliqué

- encodage invalide

- schéma JSON invalide

---

Si une erreur est détectée, la compilation est interrompue.

Aucun fichier n'est produit.

---

# 43. Compiler

Le Compiler transforme les sources en fichiers définitifs.

Il effectue notamment :

- résolution des partials

- normalisation

- génération des fichiers définitifs

Le Compiler n'écrit jamais directement dans un profil Anki.

---

# 44. Résolution des partials

Les partials sont remplacés avant la génération des templates.

Après compilation, aucun template ne contient de référence vers un partial.

---

# 45. Résolution récursive

Les partials peuvent contenir d'autres partials.

Le moteur doit résoudre cette hiérarchie.

---

Les boucles sont interdites.

Exemple interdit :

```

header

↓

footer

↓

header

```

Une erreur est produite.

---

# 46. Détection des cycles

Le moteur détecte automatiquement les dépendances circulaires.

La compilation est interrompue.

---

# 47. Normalisation

Le Compiler produit des fichiers normalisés.

Par exemple :

- encodage UTF-8

- fins de ligne LF

- suppression des espaces inutiles

- ordre stable des propriétés JSON

Cette normalisation garantit des hashes stables.

---

# 48. Assets

Le Compiler construit également la liste des ressources utilisées.

Il ne copie pas les fichiers.

Il produit uniquement un manifeste des ressources nécessaires.

---

# 49. Build

Le résultat du Compiler est écrit dans le dossier :

```

build/

```

Ce dossier contient exclusivement des fichiers prêts à être synchronisés.

---

# 50. Hasher

Le Hasher calcule les empreintes cryptographiques.

Il ne modifie aucun fichier.

---

Le Hasher est indépendant du Compiler.

---

# 51. Types de hash

Le moteur distingue plusieurs catégories.

## Source Hash

Empreinte des sources.

Permet de détecter une modification du projet.

---

## Compiled Hash

Empreinte des fichiers générés.

Permet de déterminer si le résultat final a changé.

---

## Installed Hash

Empreinte de la dernière version installée dans un profil.

Chaque profil possède ses propres Installed Hashes.

---

# 52. Algorithme

L'algorithme retenu est :

SHA-256

Il est considéré comme suffisamment stable.

---

# 53. Hash d'un type

Le hash d'un type de note est calculé à partir de tous les éléments influençant son résultat.

Exemple :

- manifeste

- templates

- stylesheet

- ressources

- partials utilisés

Toute modification de l'un de ces éléments modifie le hash.

---

# 54. Hashes indépendants

Chaque type de note possède son propre hash.

Chaque feuille de style possède également son propre hash.

Cela permet des mises à jour partielles.

---

# 55. Synchronizer

Le Synchronizer est responsable du déploiement.

Il ne compile jamais.

Il ne valide jamais.

Il ne transforme jamais les données.

---

Ses responsabilités sont uniquement :

- comparaison

- copie

- installation

- rapport

---

# 56. Synchronisation

La synchronisation est incrémentale.

Le moteur compare :

Compiled Hash

↓

Installed Hash

Si les deux valeurs sont identiques :

aucune modification n'est réalisée.

---

# 57. Profil courant

Le Synchronizer peut mettre à jour uniquement le profil actuellement ouvert.

---

# 58. Tous les profils

Le Synchronizer peut également parcourir tous les profils disponibles.

Chaque profil est traité indépendamment.

Une erreur dans un profil ne doit pas rendre les autres incohérents.

---

# 59. Copie des ressources

Les ressources sont copiées uniquement lorsqu'elles ont changé.

Le moteur évite toute copie inutile.

---

# 60. Installation

L'installation comprend notamment :

- mise à jour des templates

- copie des feuilles CSS

- copie des ressources

- mise à jour des hashes installés

---

# 61. Rapport

Chaque synchronisation produit un rapport.

Le rapport contient notamment :

- profils traités

- durée

- nombre de types mis à jour

- fichiers copiés

- avertissements

- erreurs

---

# 62. Dry Run

Le moteur possède un mode simulation.

Aucune modification n'est réalisée.

Le rapport indique uniquement les opérations qui seraient exécutées.

---

# 63. Idempotence

Deux synchronisations successives sans modification des sources doivent produire :

Aucune mise à jour.

---

# 64. Atomicité

Lorsqu'une opération échoue, le moteur doit laisser le profil dans l'état le plus cohérent possible.

Les mises à jour partielles doivent être évitées autant que possible.

---

# 65. Journalisation

Toutes les opérations importantes sont journalisées.

Le moteur distingue :

INFO

WARNING

ERROR

Le niveau DEBUG pourra être ajouté ultérieurement.

---

# 66. Gestion des erreurs

Les erreurs sont propagées sous forme d'exceptions spécialisées.

Exemples :

ValidationError

CompilationError

SynchronizationError

ProfileError

InternalError

L'utilisation d'une exception générique est déconseillée.

---

# 67. Moteur sans interface

Le moteur ne dépend jamais :

- d'Anki

- de Qt

- d'une interface graphique

- d'une ligne de commande

Il peut être utilisé dans un test automatisé sans modification.

---

# 68. Synchronisation avec Anki

Le moteur est capable d'installer les types de notes compilés dans un ou plusieurs profils Anki.

La synchronisation est la seule étape du projet qui modifie des données extérieures au dépôt.

Elle est donc soumise à des règles de sécurité particulières.

---

# 69. Principe fondamental

Le moteur ne considère jamais les profils Anki comme des sources.

Ils constituent uniquement une destination.

Le contenu des profils n'est jamais réinjecté automatiquement dans le dépôt.

---

# 70. Source de vérité

Le dépôt Git constitue toujours la référence.

En cas de divergence entre le dépôt et un profil Anki :

le dépôt l'emporte.

---

# 71. Modification manuelle

Les modifications réalisées directement dans Anki sont possibles.

Cependant elles sont considérées comme temporaires.

Le développeur est responsable de reporter ces modifications dans les sources.

Le moteur ne tente jamais de fusionner automatiquement les différences.

---

# 72. Profils

Chaque profil est traité comme une unité indépendante.

Le moteur ne partage jamais de données internes entre deux profils.

Chaque profil possède notamment :

- ses propres types de notes ;

- son propre dossier media ;

- ses propres hashes installés ;

- sa propre configuration.

---

# 73. Découverte des profils

Le moteur découvre automatiquement les profils présents dans le répertoire utilisateur d'Anki.

Aucun profil n'est codé en dur.

---

# 74. Profil courant

Le moteur peut synchroniser uniquement le profil actuellement ouvert.

Cette opération constitue le mode de fonctionnement recommandé durant le développement.

---

# 75. Tous les profils

Le moteur peut également synchroniser tous les profils.

Les profils sont traités séquentiellement.

Chaque synchronisation est indépendante.

---

# 76. Échec d'un profil

Une erreur rencontrée dans un profil ne doit pas empêcher la synchronisation des profils suivants.

Le rapport final indique les profils ayant échoué.

---

# 77. État du profil

Avant toute modification, le moteur vérifie que le profil est dans un état compatible.

Par exemple :

- profil correctement ouvert ;

- accès autorisé ;

- dossier media accessible.

En cas d'échec, aucune modification n'est entreprise.

---

# 78. Vérification préalable

Avant toute installation, le moteur vérifie :

- la validité du projet ;

- la cohérence des hashes ;

- l'existence des fichiers ;

- les droits d'accès.

Toute erreur interrompt la synchronisation du profil concerné.

---

# 79. Installation d'un type

Pour chaque type de note :

1. comparaison du hash compilé ;

2. comparaison du hash installé ;

3. décision d'installation.

Si les hashes sont identiques :

aucune opération n'est effectuée.

---

# 80. Installation des templates

Le moteur remplace les templates existants du type de note.

Aucune modification partielle d'un template n'est réalisée.

Le template est remplacé dans son intégralité.

---

# 81. Installation du CSS

Le moteur copie la feuille de style uniquement lorsqu'elle a changé.

La copie est réalisée avant la mise à jour des templates.

---

# 82. Installation des ressources

Les ressources sont copiées uniquement lorsqu'elles sont nouvelles ou modifiées.

Les ressources identiques ne sont jamais recopiées.

---

# 83. Suppression

Le moteur ne supprime jamais automatiquement :

- un type de note ;

- un template ;

- une ressource.

La suppression constitue une opération explicite.

Elle pourra être ajoutée dans une version future.

---

# 84. Synchronisation partielle

Le moteur est capable d'installer uniquement :

- un type ;

- plusieurs types ;

- ou l'ensemble des types.

---

# 85. Synchronisation complète

Une synchronisation complète installe tous les types présents dans le projet.

---

# 86. Dry Run

En mode simulation :

aucune modification n'est réalisée.

Le rapport indique :

- les types qui seraient installés ;

- les fichiers qui seraient copiés ;

- les ressources concernées.

---

# 87. Données privées

Le moteur peut stocker des informations techniques propres à son fonctionnement.

Ces données ne sont jamais utilisées par Anki.

---

# 88. Stockage privé

Les données privées sont regroupées dans un emplacement réservé au projet.

Exemple :

```
_addon-data/

    hashes.json

    version.json

    settings.json
```

L'emplacement exact dépend de l'API fournie par Anki.

Le moteur ne doit pas dépendre d'un chemin particulier.

---

# 89. Hashes installés

Chaque profil possède son propre ensemble de hashes.

Ces hashes ne sont jamais partagés entre profils.

---

# 90. Version du moteur

Le moteur peut enregistrer sa propre version dans les données privées.

Cette information facilite les migrations futures.

---

# 91. Compatibilité

Le moteur doit rester compatible avec les versions supportées d'Anki.

Lorsque plusieurs comportements sont possibles, l'API officielle d'Anki est toujours privilégiée.

---

# 92. Base de données

Le moteur ne modifie jamais directement la base SQLite de la collection.

Toutes les modifications passent exclusivement par l'API Python officielle d'Anki.

---

# 93. Robustesse

Une erreur interne ne doit jamais laisser le moteur dans un état incohérent.

Les ressources ouvertes doivent toujours être libérées.

Les fichiers temporaires doivent être supprimés.

---

# 94. Reprise

Une synchronisation interrompue peut être relancée.

Le moteur recalcule systématiquement l'état courant avant de poursuivre.

Il ne suppose jamais que la synchronisation précédente s'est terminée correctement.

---

# 95. Journal de synchronisation

Chaque synchronisation produit un journal structuré.

Le journal contient notamment :

- heure de début ;

- heure de fin ;

- durée ;

- profils ;

- types installés ;

- ressources copiées ;

- avertissements ;

- erreurs.

---

# 96. Niveaux de gravité

Les événements sont classés selon leur gravité.

INFO

Le fonctionnement est normal.

---

WARNING

Une situation inhabituelle est détectée mais la synchronisation continue.

---

ERROR

La synchronisation du profil est interrompue.

---

# 97. Résultat

Le moteur produit un objet représentant le résultat complet de la synchronisation.

Cet objet est indépendant de toute interface graphique.

Il peut être utilisé :

- par l'add-on ;

- par les tests ;

- par une interface CLI.

---

# 98. Interface graphique

L'interface Anki n'accède jamais directement aux profils.

Elle communique uniquement avec le moteur.

Toutes les décisions métier sont prises par le moteur.

---

# 99. Invariants de synchronisation

Les propriétés suivantes doivent toujours rester vraies.

- Git est la source de vérité.

- Le moteur ne lit jamais les profils pour reconstruire les sources.

- Les profils restent autonomes.

- Les suppressions sont toujours explicites.

- Les mises à jour sont incrémentales.

- Les données privées restent séparées des données Anki.

- Le moteur utilise exclusivement l'API officielle.

---

# 100. Modèle de données interne

Le moteur manipule une représentation interne des projets.

Cette représentation constitue l'unique modèle de données utilisé par les différents modules.

Les modules ne manipulent jamais directement :

- des dictionnaires JSON ;
- des fichiers ;
- des chemins système.

Ils utilisent exclusivement les objets du modèle.

---

# 101. Principe

Chaque objet représente un concept métier.

Exemples :

- Workspace
- NoteTypeProject
- Template
- Stylesheet
- Asset
- Partial
- Profile

Le moteur ne mélange jamais plusieurs concepts dans un même objet.

---

# 102. Workspace

Le Workspace représente un dépôt complet.

Il constitue le point d'entrée du moteur.

Il contient notamment :

- la configuration ;
- les projets ;
- les feuilles CSS ;
- les partials ;
- les ressources.

Il ne contient aucune donnée Anki.

---

# 103. NoteTypeProject

Cet objet représente un projet de type de note.

Il contient :

- son manifeste ;
- ses templates ;
- ses ressources ;
- sa feuille de style ;
- sa documentation.

Il ne contient aucune donnée provenant d'Anki.

---

# 104. Template

Un Template représente un modèle de carte.

Il contient notamment :

- son nom ;
- son template front ;
- son template back.

Il peut également contenir d'autres métadonnées.

---

# 105. Partial

Un Partial représente un fragment HTML.

Il possède :

- un identifiant ;
- son contenu.

Il n'est jamais synchronisé vers Anki.

---

# 106. Stylesheet

Une Stylesheet représente une feuille CSS.

Elle est indépendante des types de notes.

Plusieurs projets peuvent référencer la même feuille.

---

# 107. Asset

Une ressource représente un fichier non textuel.

Exemples :

- image
- audio
- police

Le moteur ne fait aucune hypothèse sur leur nature.

---

# 108. Manifest

Chaque projet possède un manifeste.

Le manifeste est chargé une seule fois.

Il devient ensuite un objet du modèle.

Le moteur ne manipule plus directement le JSON.

---

# 109. CompiledProject

Après compilation, le projet produit un CompiledProject.

Cet objet contient uniquement les données prêtes à être installées.

Il est indépendant des sources.

---

# 110. InstallationManifest

Chaque profil possède un manifeste d'installation.

Ce manifeste contient :

- les versions installées ;
- les hashes ;
- les informations techniques.

Il n'est jamais versionné dans Git.

---

# 111. Profile

Le moteur représente chaque profil Anki par un objet Profile.

Il contient notamment :

- son identifiant ;
- son nom ;
- son dossier media ;
- son manifeste d'installation.

Le moteur ne manipule jamais directement les chemins système.

---

# 112. SyncReport

Chaque synchronisation produit un rapport.

Ce rapport contient :

- les profils ;
- les opérations réalisées ;
- les avertissements ;
- les erreurs ;
- la durée.

Il est totalement indépendant de l'interface graphique.

---

# 113. ValidationReport

La validation produit également un rapport.

Le rapport contient :

- les erreurs ;
- les avertissements ;
- les statistiques éventuelles.

---

# 114. BuildReport

La compilation produit un BuildReport.

Il décrit notamment :

- les projets compilés ;
- les partials résolus ;
- les ressources détectées ;
- les fichiers générés.

---

# 115. Principes

Tous les objets du modèle respectent les principes suivants.

- responsabilité unique ;

- cohérence interne ;

- sérialisation possible ;

- indépendance vis-à-vis d'Anki.

---

# 116. Immutabilité

Les objets produits par le Loader sont considérés comme immuables.

Les transformations produisent de nouveaux objets.

Les modifications en place sont évitées.

---

# 117. Égalité

Deux objets sont considérés égaux lorsque leurs propriétés métier sont identiques.

Leur identité mémoire n'est jamais utilisée.

---

# 118. Identifiants

Chaque objet possède un identifiant stable.

Les identifiants générés aléatoirement sont évités.

---

# 119. Dépendances

Les relations entre objets sont explicites.

Les références implicites sont interdites.

---

# 120. Chargement

Le Loader construit entièrement le modèle avant toute validation.

Le Validator travaille exclusivement sur ce modèle.

---

# 121. Validation

La validation ne modifie jamais les objets.

Elle produit uniquement des diagnostics.

---

# 122. Compilation

La compilation transforme le modèle en un CompiledProject.

Le modèle d'origine reste inchangé.

---

# 123. Synchronisation

La synchronisation consomme un CompiledProject.

Elle ne relit jamais les sources.

---

# 124. Extensibilité

De nouveaux objets pourront être ajoutés sans modifier les objets existants.

Le moteur privilégie la composition à l'héritage.

---

# 125. Encapsulation

Chaque objet garantit sa propre cohérence.

Les autres modules ne modifient jamais directement son état interne.

---

# 126. Découplage

Le modèle métier ne dépend :

- ni d'Anki ;
- ni de Qt ;
- ni du système de fichiers.

Les adaptations vers ces environnements sont réalisées par des composants spécialisés.

---

# 127. Validation

La validation vérifie que les sources du projet sont cohérentes.

Elle est exécutée avant toute compilation.

En présence d'une erreur bloquante, la compilation n'est jamais lancée.

---

# 128. Objectifs

La validation poursuit plusieurs objectifs.

- détecter les erreurs le plus tôt possible ;

- produire des diagnostics compréhensibles ;

- empêcher la production de fichiers invalides ;

- éviter que des erreurs atteignent Anki.

---

# 129. Principes

La validation :

- ne modifie jamais les données ;

- ne produit aucun fichier ;

- n'accède jamais aux profils Anki ;

- ne dépend jamais de l'interface graphique.

---

# 130. Diagnostic

Toute anomalie est représentée par un objet Diagnostic.

Le moteur ne manipule jamais directement des chaînes de caractères.

---

# 131. Contenu d'un Diagnostic

Un Diagnostic contient notamment :

- identifiant ;
- gravité ;
- message ;
- origine ;
- fichier concerné ;
- position éventuelle ;
- suggestion éventuelle.

---

# 132. Gravité

Le moteur distingue trois niveaux.

## Information

Message informatif.

La compilation continue.

---

## Warning

Situation inhabituelle.

La compilation continue.

---

## Error

Erreur bloquante.

La compilation est interrompue.

---

# 133. Codes

Chaque diagnostic possède un code stable.

Exemples :

```
NT001

NT002

CSS001

HTML003

...
```

Les codes ne changent jamais de signification.

Ils permettent :

- la recherche dans la documentation ;

- l'écriture de tests ;

- l'automatisation.

---

# 134. Messages

Les messages sont destinés aux utilisateurs.

Ils doivent être :

- clairs ;

- précis ;

- actionnables.

Éviter les formulations ambiguës.

---

# 135. Localisation

Le moteur indique autant que possible :

- le fichier ;

- la ligne ;

- la colonne.

---

# 136. Suggestions

Lorsque cela est possible, le moteur propose une solution.

Exemple :

```
Le partial "footer" est introuvable.

Avez-vous voulu écrire "footer.html" ?
```

---

# 137. Validation du manifeste

Le manifeste est validé :

- contre son schéma JSON ;

- puis par des règles métier.

Les deux validations sont distinctes.

---

# 138. Validation des templates

Le moteur vérifie notamment :

- présence des fichiers ;

- références aux partials ;

- dépendances circulaires ;

- cohérence interne.

---

# 139. Validation des partials

Le moteur vérifie :

- existence ;

- unicité ;

- absence de cycles.

---

# 140. Validation du CSS

Le moteur vérifie notamment :

- existence ;

- encodage ;

- importations autorisées.

Le moteur n'effectue pas une validation complète du langage CSS.

---

# 141. Validation des ressources

Les ressources référencées doivent exister.

Le moteur vérifie également les doublons.

---

# 142. Validation des noms

Les noms doivent être uniques lorsqu'ils identifient un même type d'objet.

Exemple :

Deux projets ne peuvent pas porter le même nom.

---

# 143. Validation des chemins

Le moteur interdit notamment :

- les chemins absolus ;

- les remontées de répertoire (`..`) ;

- les chemins invalides.

---

# 144. Validation des encodages

Tous les fichiers texte doivent être encodés en UTF-8 sans BOM.

---

# 145. Validation des fins de ligne

Le moteur peut signaler les fichiers ne respectant pas la convention LF.

Cette anomalie est un avertissement.

---

# 146. Validation des caractères interdits

Le moteur peut signaler certains caractères problématiques dans les noms de fichiers ou les identifiants.

---

# 147. Validation des références

Toutes les références doivent pouvoir être résolues.

Exemples :

- stylesheet ;

- partial ;

- ressource.

---

# 148. Validation des dépendances

Le moteur construit un graphe de dépendances.

Les cycles sont interdits.

---

# 149. Validation incrémentale

À terme, le moteur pourra limiter la validation aux éléments modifiés.

Cette optimisation n'est pas requise pour la première version.

---

# 150. Validation déterministe

Deux validations successives des mêmes sources doivent produire exactement les mêmes diagnostics.

---

# 151. Rapport

La validation produit un ValidationReport.

Il contient :

- diagnostics ;

- statistiques ;

- durée.

---

# 152. Échec

La présence d'au moins une erreur bloque la compilation.

Les warnings n'empêchent pas la compilation.

---

# 153. Tests

Chaque règle de validation doit posséder au moins un test automatisé.

---

# 154. Évolution

Les nouvelles règles de validation ne doivent pas rendre invalides des projets corrects sans justification documentée.

Lorsqu'une règle devient plus stricte, cette évolution doit être mentionnée dans le changelog.

---

# 155. Documentation

Chaque code de diagnostic doit être documenté.

La documentation indique :

- la signification du code ;

- les causes possibles ;

- les solutions recommandées.

---

# 156. Tests

Le moteur doit être entièrement testable.

Les tests constituent une partie intégrante du projet.

Ils permettent de garantir :

- la stabilité du moteur ;
- la reproductibilité des résultats ;
- la compatibilité entre versions.

---

# 157. Philosophie

Les tests vérifient le comportement observable.

Ils ne doivent pas dépendre de l'implémentation interne.

Le remplacement d'un algorithme ne doit pas nécessiter la réécriture des tests tant que le comportement reste identique.

---

# 158. Catégories

Le projet distingue plusieurs catégories de tests.

- unitaires ;
- intégration ;
- régression ;
- performances.

---

# 159. Tests unitaires

Les tests unitaires vérifient une classe ou un module isolé.

Ils ne dépendent jamais :

- d'Anki ;
- du système de fichiers réel ;
- d'une interface graphique.

---

# 160. Tests d'intégration

Ils vérifient plusieurs composants fonctionnant ensemble.

Par exemple :

Workspace

↓

Loader

↓

Validator

↓

Compiler

↓

Generated

---

# 161. Tests de régression

Chaque bug corrigé doit être accompagné d'un test reproduisant ce bug.

Le test empêche sa réapparition.

---

# 162. Tests de performance

Ils vérifient notamment :

- temps de compilation ;

- temps de synchronisation ;

- nombre de fichiers copiés.

Ils ne recherchent pas une valeur absolue.

Ils détectent principalement les régressions.

---

# 163. Fixtures

Les tests utilisent des projets de démonstration.

Ces projets sont regroupés dans :

tests/fixtures/

---

# 164. Fixtures minimales

Le projet contient notamment :

valid/

Projet minimal valide.

---

missing-template/

Template absent.

---

invalid-manifest/

Manifeste invalide.

---

duplicate-name/

Deux types portant le même nom.

---

missing-partial/

Partial introuvable.

---

cyclic-partials/

Cycle entre partials.

---

invalid-css/

CSS invalide.

---

multi-profile/

Projet destiné aux tests de synchronisation.

---

# 165. Organisation

Les tests sont organisés par domaine.

Exemple :

tests/

    unit/

    integration/

    regression/

    performance/

    fixtures/

---

# 166. Déterminisme

Les tests doivent produire les mêmes résultats quelle que soit la plateforme.

---

# 167. Données temporaires

Les tests créent leurs propres espaces de travail.

Ils ne modifient jamais :

- le dépôt ;

- les profils Anki réels.

---

# 168. Faux profils

Les tests de synchronisation utilisent des profils temporaires.

Ils ne dépendent jamais du profil personnel du développeur.

---

# 169. Isolation

Chaque test est indépendant.

L'exécution d'un test ne doit jamais influencer un autre.

---

# 170. Ordre

Les tests peuvent être exécutés dans n'importe quel ordre.

---

# 171. Couverture

Le projet ne fixe pas de pourcentage minimal de couverture.

L'objectif est de couvrir :

- les algorithmes ;
- les règles métier ;
- les bugs corrigés.

---

# 172. Tests obligatoires

Toute fonctionnalité importante doit posséder au moins un test.

Toute règle de validation doit posséder au moins un test.

---

# 173. Tests des hashes

Le projet vérifie notamment :

- stabilité ;

- reproductibilité ;

- modification lorsqu'une source change.

---

# 174. Tests des partials

Les tests vérifient :

- résolution simple ;

- résolution multiple ;

- récursion ;

- détection des cycles.

---

# 175. Tests du Compiler

Le résultat produit est comparé à une sortie attendue.

---

# 176. Golden Files

Lorsque cela est pertinent, les sorties compilées sont conservées comme référence.

Une modification du résultat doit être volontaire.

---

# 177. Tests de synchronisation

Ils vérifient notamment :

- aucune modification si les hashes sont identiques ;

- mise à jour lorsqu'un template change ;

- copie du CSS ;

- copie des ressources.

---

# 178. Tests Dry Run

Le mode simulation ne doit jamais modifier les profils.

---

# 179. Tests d'erreurs

Chaque erreur importante doit être testée.

Le moteur doit produire le bon diagnostic.

---

# 180. Tests de migration

Les anciennes versions des manifests restent testées.

---

# 181. Exécution

Les tests doivent pouvoir être lancés par une commande unique.

Exemple :

pytest

---

# 182. Temps d'exécution

Les tests unitaires doivent rester rapides.

Les tests plus longs peuvent être regroupés dans une catégorie distincte.

---

# 183. Documentation

Les nouveaux tests doivent être compréhensibles.

Leur nom doit décrire le comportement attendu.

---

# 184. Maintenance

Les tests sont considérés comme du code de production.

Ils suivent les mêmes exigences de qualité.

---

# 185. Compatibilité

Le projet cherche à maintenir la compatibilité avec les versions d'Anki officiellement supportées.

Lorsqu'une version d'Anki n'est plus supportée, cette décision doit être documentée dans le changelog.

---

# 186. Compatibilité des schémas

Chaque manifeste possède un numéro de version (`schemaVersion`).

Le moteur peut gérer plusieurs versions d'un même schéma.

Les anciennes versions ne doivent pas être supprimées sans justification.

---

# 187. Compatibilité des projets

Un projet valide avec une version donnée du moteur doit continuer à fonctionner avec les versions ultérieures lorsque cela est raisonnablement possible.

Toute rupture de compatibilité doit être explicitement documentée.

---

# 188. Évolutions

Les nouvelles fonctionnalités doivent privilégier l'ajout de nouveaux champs plutôt que la modification du comportement des champs existants.

Les changements incompatibles doivent rester exceptionnels.

---

# 189. Dépréciation

Une fonctionnalité ne doit jamais être supprimée immédiatement.

Le processus recommandé est :

1. introduction d'un avertissement ;
2. documentation de la dépréciation ;
3. suppression dans une version majeure ultérieure.

---

# 190. Performances

Le projet privilégie la simplicité de conception.

Les optimisations ne sont introduites qu'après mesure.

Les performances ne doivent jamais dégrader la lisibilité du code sans justification.

---

# 191. Déterminisme

Toutes les opérations du moteur doivent être déterministes.

À partir des mêmes sources, le résultat doit toujours être identique.

Cette propriété est considérée comme fondamentale.

---

# 192. Reproductibilité

Le projet doit pouvoir être compilé sur plusieurs machines sans produire de différences.

Les informations dépendantes de la machine locale ne doivent jamais influencer le résultat compilé.

---

# 193. Sécurité

Le moteur refuse les opérations susceptibles de sortir du répertoire de travail.

Les chemins absolus ou les remontées de répertoire (`..`) sont interdits lorsqu'ils proviennent des sources du projet.

---

# 194. Tolérance aux erreurs

Le moteur doit détecter les erreurs au plus tôt.

Les messages doivent être compréhensibles et permettre une correction rapide.

Les erreurs internes ne doivent jamais être présentées comme des erreurs utilisateur.

---

# 195. Journalisation

Les journaux produits par le moteur doivent permettre de comprendre une exécution sans avoir à reproduire le problème.

Ils ne doivent toutefois pas contenir d'informations sensibles.

---

# 196. Internationalisation

Les messages internes du moteur sont rédigés en anglais.

L'interface utilisateur pourra les traduire si nécessaire.

Les diagnostics utilisent des codes stables indépendants de leur traduction.

---

# 197. Configuration

Le moteur centralise sa configuration.

Les modules ne lisent jamais directement les variables d'environnement ou les fichiers de configuration.

Toute configuration passe par un objet dédié.

---

# 198. Dépendances

Les dépendances externes doivent être limitées au strict nécessaire.

Avant d'ajouter une dépendance, il convient de vérifier si une solution raisonnable existe dans la bibliothèque standard Python.

---

# 199. Évolutivité

Le projet est conçu pour évoluer.

Toute nouvelle fonctionnalité doit pouvoir être ajoutée avec un impact limité sur les composants existants.

Les responsabilités des modules doivent rester clairement séparées.

---

# 200. Documentation

Toute fonctionnalité publique doit être documentée.

La documentation fait partie intégrante du projet.

Elle est versionnée avec le code.

---

# 201. Décisions d'architecture

Les décisions importantes sont consignées dans un document dédié (`DECISIONS.md` ou un dossier `docs/adr/`).

Chaque décision explique :

- le contexte ;
- les alternatives envisagées ;
- la décision retenue ;
- ses conséquences.

---

# 202. Invariants

Les invariants définis dans cette spécification sont considérés comme des contrats.

Ils ne doivent être modifiés qu'après une décision d'architecture documentée.

---

# 203. Critères de réussite

Le projet est considéré comme conforme à cette spécification lorsque les propriétés suivantes sont vérifiées :

- les types de notes sont entièrement définis dans le dépôt Git ;
- les sources sont validées avant toute compilation ;
- la compilation est déterministe ;
- la synchronisation est incrémentale ;
- le moteur n'utilise jamais directement la base SQLite d'Anki ;
- les profils Anki restent autonomes ;
- les tests automatisés couvrent les principales fonctionnalités ;
- les diagnostics sont explicites et documentés.

---

# 204. Révisions de la spécification

Cette spécification est un document vivant.

Toute modification importante de son contenu doit être discutée avant son implémentation.

La spécification précède le code.

Le code doit refléter la spécification, et non l'inverse.

---
