# ARCHITECTURE.md

Version : 1.0 (Draft)

---

# 1. Objectif

Ce document décrit l'architecture interne du projet.

Il complète `SPEC.md`.

Les deux documents ont des rôles distincts :

* **SPEC.md** décrit le comportement attendu du système.
* **ARCHITECTURE.md** décrit son organisation interne.

Une implémentation est conforme lorsqu'elle respecte les contraintes définies dans les deux documents.

---

# 2. Principes d'architecture

L'architecture repose sur plusieurs principes.

## 2.1 Responsabilité unique

Chaque module possède une responsabilité clairement définie.

Aucun module ne doit remplir plusieurs rôles fonctionnels.

---

## 2.2 Faible couplage

Les modules communiquent uniquement au moyen d'interfaces bien définies.

Ils ne doivent pas dépendre des détails d'implémentation des autres modules.

---

## 2.3 Forte cohésion

Les fonctionnalités proches doivent être regroupées.

Les fonctionnalités indépendantes doivent être séparées.

---

## 2.4 Dépendances unidirectionnelles

Les dépendances vont toujours dans le même sens.

```
Interface
    ↓

Synchronizer
    ↓

Compiler
    ↓

Validator
    ↓

Loader
    ↓

Model
```

Le modèle ne dépend de personne.

---

## 2.5 Séparation des préoccupations

Chaque couche possède un objectif précis.

Le modèle représente les données.

Le Loader charge les sources.

Le Validator vérifie leur cohérence.

Le Compiler produit les artefacts compilés.

Le Synchronizer installe les artefacts.

L'add-on ne fait qu'interagir avec l'utilisateur.

---

# 3. Vue d'ensemble

```
                +------------------+
                |     Add-on       |
                +---------+--------+
                          |
                          v
                +------------------+
                | Synchronizer     |
                +---------+--------+
                          |
                          v
                +------------------+
                | Compiler         |
                +---------+--------+
                          |
                          v
                +------------------+
                | Validator        |
                +---------+--------+
                          |
                          v
                +------------------+
                | Loader           |
                +---------+--------+
                          |
                          v
                +------------------+
                | Model            |
                +------------------+
```

Le modèle est la fondation.

Toutes les autres couches s'appuient sur lui.

---

# 4. Organisation du code

```
src/anki_note_types/

    model/

    loader/

    validator/

    compiler/

    synchronizer/

    diagnostics/

    hashing/

    logging/

    configuration/

    filesystem/

    reports/

    exceptions/
```

Chaque répertoire constitue un module indépendant.

---

# 5. Module Model

Le module `model` contient uniquement les objets métier.

Il ne contient aucun algorithme de compilation.

Il ne lit jamais le système de fichiers.

Il ne dépend pas d'Anki.

Il représente uniquement les concepts du domaine.

Exemples :

* Workspace
* NoteTypeProject
* Template
* Partial
* Stylesheet
* Asset
* Profile
* CompiledProject
* SyncReport

---

# 6. Module Loader

Le Loader transforme les fichiers présents dans `project/` en objets du modèle.

Il ne valide jamais.

Il ne compile jamais.

Il ne modifie jamais les données.

Sa seule responsabilité est le chargement.

---

# 7. Module Validator

Le Validator vérifie les objets produits par le Loader.

Il ne modifie jamais le modèle.

Il produit uniquement des diagnostics.

Le Validator est composé d'un ensemble de règles indépendantes.

Chaque règle possède :

* un identifiant ;
* une responsabilité ;
* un ensemble de diagnostics.

---

# 8. Module Compiler

Le Compiler transforme le modèle validé en artefacts compilés.

Il réalise notamment :

* la résolution des partials ;
* la normalisation ;
* la préparation des templates ;
* la préparation des feuilles CSS ;
* la préparation des ressources.

Le Compiler est pur : il retourne un `CompiledWorkspace` en mémoire.

L'écriture dans `build/` est assurée par `BuildWriter`, un composant
d'infrastructure distinct. Cette séparation permet de tester la compilation
sans effet de bord.

---

# 9. Module Synchronizer

Le Synchronizer installe les artefacts compilés dans un ou plusieurs profils Anki.

Il ne lit jamais les sources.

Il ne compile jamais.

Il ne valide jamais.

Il consomme uniquement les résultats du Compiler.

---

# 10. Services transverses

Plusieurs services sont utilisés par différents modules.

Ils ne font pas partie du pipeline.

Exemples :

* HashService
* LoggingService
* FileSystemService
* ConfigurationService

Ces services sont stateless autant que possible.

---

# 11. Diagnostics

Le moteur produit exclusivement des objets `Diagnostic`.

Aucun module ne construit directement des messages destinés à l'utilisateur.

Les interfaces se chargent de présenter les diagnostics.

---

# 12. Rapports

Chaque grande opération produit un rapport dédié.

Exemples :

* ValidationReport
* BuildReport
* SyncReport

Ces rapports sont indépendants de toute interface graphique.

Ils peuvent être utilisés :

* par l'add-on ;
* par la ligne de commande ;
* par les tests.

---

# 13. Exceptions

Les exceptions représentent des erreurs internes.

Les diagnostics représentent des erreurs fonctionnelles.

Le moteur privilégie les diagnostics.

Les exceptions sont réservées aux situations exceptionnelles :

* erreur de programmation ;
* accès disque impossible ;
* corruption inattendue.

---

# 14. Injection des dépendances

Les modules reçoivent leurs dépendances.

Ils ne les créent pas eux-mêmes.

Exemple :

Le Compiler reçoit :

* HashService ;
* FileSystemService ;
* Logger.

Il ne les instancie jamais directement.

Cette approche facilite les tests unitaires.

---

# 15. Tests

Chaque module peut être testé indépendamment.

Le Synchronizer est le seul module nécessitant un environnement Anki.

Tous les autres modules doivent être testables sans Anki.

---

# 16. Évolution

L'ajout d'une nouvelle fonctionnalité doit, autant que possible :

* ajouter un nouveau module ;
* ou étendre un module existant ;

sans modifier plusieurs couches simultanément.

Une modification importante de l'architecture doit être précédée d'une Architecture Decision Record (ADR).

---

# 17. Invariants

L'architecture garantit notamment :

* le modèle ne dépend d'aucune couche supérieure ;
* les modules ne communiquent que par leurs interfaces publiques ;
* les services techniques restent séparés des règles métier ;
* l'add-on ne contient aucune logique métier ;
* le moteur reste utilisable sans interface graphique.

---

# 18. Philosophie

L'architecture privilégie :

* la simplicité ;
* la lisibilité ;
* la testabilité ;
* l'évolutivité.

Les abstractions ne sont introduites qu'en réponse à un besoin réel.

Le projet applique les principes KISS et YAGNI.

Une architecture simple mais robuste est préférée à une architecture très générale mais inutilement complexe.

# 19. Flux de données

Le moteur suit un flux de données strictement unidirectionnel.

Aucun module ne modifie les données produites par un module situé en amont.

Le pipeline est le suivant :

```text
project/
    │
    ▼
Loader
    │
    ▼
Workspace
    │
    ▼
Validator
    │
    ▼
ValidationReport
    │
    ▼
Compiler
    │
    ▼
Build/
    │
    ▼
Synchronizer
    │
    ▼
Profil(s) Anki
```

Chaque étape reçoit une entrée, produit une sortie et ne conserve aucun état persistant.

---

# 20. Contrats entre modules

Les modules communiquent uniquement au moyen d'objets du modèle.

Ils ne partagent jamais :

* des chemins système ;
* des structures JSON ;
* des dictionnaires Python ;
* des variables globales.

Chaque module possède une interface publique stable.

Les détails d'implémentation restent privés.

---

# 21. État

Le moteur privilégie un fonctionnement stateless.

Les modules ne conservent pas d'état entre deux exécutions.

Les seules données persistantes sont :

* les sources (`project/`) ;
* les artefacts compilés (`build/`) ;
* les données privées stockées dans les profils Anki.

---

# 22. Gestion des chemins

Aucun module ne construit des chemins à partir de chaînes de caractères.

Tous les chemins passent par une abstraction dédiée.

Les séparateurs de répertoires sont gérés par cette abstraction.

Le moteur reste ainsi indépendant du système d'exploitation.

---

# 23. Gestion des fichiers

Les accès disque sont centralisés.

Les modules métier ne manipulent jamais directement :

* open()
* os
* pathlib

Ils utilisent un service spécialisé.

Cette règle facilite les tests unitaires.

---

# 24. Configuration

Toute configuration est regroupée dans un objet Configuration.

Aucun module ne lit directement :

* les variables d'environnement ;
* les arguments de la ligne de commande ;
* les fichiers de configuration.

La configuration est injectée au démarrage.

---

# 25. Journalisation

La journalisation est assurée par un service dédié.

Le moteur ne décide jamais :

* où écrire les journaux ;
* sous quel format ;
* vers quelle destination.

Ces décisions appartiennent à l'interface.

Le moteur se contente d'émettre des événements.

---

# 26. Événements

Les modules peuvent publier des événements.

Exemples :

* BuildStarted
* ProjectLoaded
* ValidationFinished
* CompilationFinished
* SynchronizationStarted
* ProfileUpdated
* SynchronizationFinished

Les événements permettent :

* l'affichage d'une barre de progression ;
* la journalisation ;
* les statistiques ;
* le débogage.

Le moteur ne dépend jamais des consommateurs de ces événements.

---

# 27. Concurrence

La première version du projet exécute les opérations de manière séquentielle.

Le moteur ne dépend pas du parallélisme.

Une exécution parallèle pourra être ajoutée ultérieurement sans modifier le modèle de données.

---

# 28. Gestion des ressources

Les ressources sont représentées par des objets du modèle.

Le Compiler produit une liste complète des ressources nécessaires.

Le Synchronizer est seul responsable de leur copie.

---

# 29. Cache

Le moteur pourra disposer d'un cache interne.

Le cache constitue une optimisation.

Son absence ne doit jamais modifier le comportement du projet.

Le cache peut être supprimé à tout moment.

---

# 30. HashService

Le HashService fournit une API unique de calcul d'empreintes.

Il est utilisé par :

* le Compiler ;
* le Synchronizer ;
* les tests.

Les modules ne calculent jamais directement des hashes.

---

# 31. Accès au système de fichiers

Les accès au système de fichiers sont limités aux composants d'infrastructure
(`ProjectLoader`, `BuildWriter` et, ultérieurement, le Synchronizer). Les
composants métier, notamment le Validator et le Compiler, n'y accèdent jamais.

Ces composants assument notamment :

* lecture de fichiers ;
* écriture de fichiers ;
* création de répertoires ;
* suppression de fichiers temporaires ;
* copie de ressources.

---

# 32. ConfigurationService

Ce service fournit une vue centralisée de la configuration.

Les modules ne connaissent jamais l'origine des paramètres.

---

# 33. ReportFactory

La création des rapports est centralisée.

Les modules ne construisent pas directement les rapports finaux.

Ils produisent des événements ou des résultats intermédiaires.

La ReportFactory assemble ensuite les différents éléments.

---

# 34. Cycle de vie

Une exécution complète suit toujours les étapes suivantes :

1. Initialisation.
2. Chargement des sources.
3. Validation.
4. Compilation.
5. Vérification des erreurs.
6. Synchronisation.
7. Génération du rapport.
8. Libération des ressources.

Toute interruption provoque une libération propre des ressources ouvertes.

---

# 35. Règles de dépendance

Les dépendances autorisées sont résumées ci-dessous.

```text
Add-on
   │
   ▼
Synchronizer
   │
   ▼
Compiler
   │
   ▼
Validator
   │
   ▼
Loader
   │
   ▼
Model

Services
   ▲
   │
(utilisés par les couches supérieures)
```

Les dépendances inverses sont interdites.

Le Model ne dépend jamais du Compiler.

Le Compiler ne dépend jamais du Synchronizer.

L'Add-on ne dépend jamais des détails internes des modules.

---

# 36. Principes de refactorisation

Toute évolution importante doit respecter les règles suivantes :

* conserver les interfaces publiques lorsque cela est possible ;
* maintenir la compatibilité des objets du modèle ;
* préserver les invariants définis dans SPEC.md ;
* ajouter des tests avant toute refactorisation importante.

---

# 37. Résumé

L'architecture repose sur trois idées fondamentales.

1. Les objets du modèle constituent le langage commun du projet.

2. Chaque module possède une responsabilité unique.

3. Les dépendances circulent toujours dans une seule direction.

Ces trois principes sont considérés comme les fondations de l'ensemble du projet.

# 38. Architecture du modèle métier

Le modèle métier constitue le cœur du projet.

Tous les modules manipulent exclusivement des objets du modèle.

Les objets du modèle sont indépendants :

* du système de fichiers ;
* d'Anki ;
* de l'interface graphique ;
* des bibliothèques externes.

Ils représentent uniquement les concepts du domaine.

---

# 39. Hiérarchie générale

```text
Workspace
│
├── Project
│   ├── Manifest
│   ├── Templates
│   ├── StylesheetReference
│   ├── Assets
│   └── Documentation
│
├── Partials
│
├── Stylesheets
│
└── Assets
```

Cette hiérarchie représente les sources du projet.

---

# 40. Workspace

Le Workspace représente un dépôt complet.

Il contient :

* tous les projets ;
* tous les partials ;
* toutes les feuilles de style ;
* toutes les ressources globales.

Le Workspace constitue la racine du modèle.

Il n'existe qu'un seul Workspace par exécution.

---

# 41. Project

Un Project représente un type de note.

Il possède un cycle de vie indépendant.

Toutes les opérations (validation, compilation, synchronisation) sont réalisées projet par projet.

Le moteur ne traite jamais directement les fichiers.

Il traite des objets Project.

---

# 42. Manifest

Le Manifest représente le contenu de `metadata.json`.

Après son chargement, le JSON n'est plus utilisé.

Toutes les informations passent par cet objet.

Le Manifest garantit la validité des données qu'il expose.

---

# 43. Template

Un Template représente un modèle de carte.

Il contient notamment :

* son nom ;
* son contenu front ;
* son contenu back.

Le contenu est manipulé sous forme de texte.

Le moteur ne tente pas d'interpréter le HTML.

---

# 44. TemplateDefinition

Chaque Template possède également une définition.

Cette définition est chargée depuis `template.json`.

Elle contient les propriétés spécifiques au template.

Le contenu HTML reste séparé des métadonnées.

---

# 45. Partial

Un Partial représente un fragment HTML réutilisable.

Il possède :

* un identifiant ;
* son contenu ;
* sa localisation.

Les Partials sont résolus pendant la compilation.

---

# 46. Stylesheet

Une Stylesheet représente une feuille CSS.

Elle peut être référencée par plusieurs projets.

Le moteur ne duplique jamais cet objet en mémoire.

---

# 47. Asset

Une ressource représente un fichier binaire ou texte utilisé par un projet.

Le moteur ne suppose jamais son format.

Les ressources sont identifiées par leur chemin logique.

---

# 48. CompiledWorkspace

Après compilation, le Workspace produit un CompiledWorkspace.

Il contient exclusivement des objets prêts à être synchronisés.

Les sources originales restent inchangées.

---

# 49. CompiledProject

Chaque Project compilé devient un CompiledProject.

Celui-ci contient :

* les templates résolus ;
* les ressources nécessaires ;
* les hashes calculés ;
* les informations de synchronisation.

---

# 50. CompiledTemplate

Le CompiledTemplate est le résultat final envoyé à Anki.

Il ne contient plus :

* de partials ;
* de références non résolues ;
* de données inutilisées.

Il est considéré comme immuable.

---

# 51. Profile

Le Profile représente un profil Anki.

Il ne représente jamais une collection SQLite.

Il représente un environnement d'installation.

Le Synchronizer est le seul module autorisé à manipuler les objets Profile.

---

# 52. InstallationState

Chaque profil possède un état d'installation.

Cet état contient notamment :

* les hashes installés ;
* les versions installées ;
* les informations internes au moteur.

Le reste du moteur ne dépend jamais du format de stockage.

---

# 53. Reports

Les rapports sont eux aussi des objets métier.

Ils possèdent une structure stable.

Les interfaces se contentent de les afficher.

Le moteur ne produit jamais de texte formaté destiné à l'utilisateur.

---

# 54. Diagnostics

Les diagnostics sont également des objets du modèle.

Ils sont indépendants :

* de la langue ;
* de l'interface ;
* du terminal.

Le moteur produit des diagnostics structurés.

Leur présentation est laissée aux interfaces.

---

# 55. Immutabilité

Les objets du modèle doivent être considérés comme immuables.

Une transformation produit un nouvel objet.

Elle ne modifie jamais l'objet d'origine.

---

# 56. Identité

Chaque objet possède une identité métier.

Cette identité reste stable pendant toute son existence.

Elle ne dépend jamais :

* d'une adresse mémoire ;
* d'un identifiant généré aléatoirement.

---

# 57. Relations

Les relations entre objets sont explicites.

Les références implicites sont interdites.

Le moteur ne reconstruit jamais une relation à partir d'un nom de fichier lorsqu'un lien métier existe déjà.

---

# 58. Sérialisation

Les objets du modèle doivent pouvoir être sérialisés.

Cette propriété facilite :

* les tests ;
* le débogage ;
* les rapports ;
* les outils futurs.

La sérialisation n'est toutefois jamais utilisée comme mécanisme principal de communication entre modules.

---

# 59. Évolution

L'ajout d'une nouvelle propriété à un objet du modèle ne doit pas casser les modules existants lorsque cette propriété est optionnelle.

Les objets sont conçus pour évoluer progressivement.

---

# 60. Invariants

Le modèle métier respecte les invariants suivants.

* Un Workspace contient zéro ou plusieurs Projects.

* Un Project possède exactement un Manifest.

* Un Template appartient à un seul Project.

* Un CompiledProject provient d'un seul Project.

* Un Profile représente un seul profil Anki.

* Les objets compilés ne modifient jamais les objets sources.

Ces invariants constituent les fondations du moteur.

# 61. Architecture des composants

Les composants constituent les éléments actifs du moteur.

Contrairement aux objets du modèle, ils possèdent un comportement.

Ils manipulent les objets métier mais ne deviennent jamais eux-mêmes des objets métier.

---

# 62. Définition

Un composant est un objet chargé d'exécuter une responsabilité unique.

Exemples :

* Loader
* Validator
* Compiler
* Synchronizer

Les composants ne stockent pas d'état métier permanent.

---

# 63. Cycle de vie

Les composants sont créés au démarrage d'une exécution.

Ils sont détruits à la fin de celle-ci.

Ils ne conservent aucun état entre deux exécutions.

---

# 64. Stateless

Les composants doivent être stateless autant que possible.

Ils reçoivent toutes les informations nécessaires en paramètres.

Ils ne dépendent pas de variables globales.

---

# 65. Loader

Entrée :

Aucun objet métier.

Sortie :

Workspace

Responsabilité :

Construire le modèle métier à partir des fichiers présents dans `project/`.

---

# 66. Validator

Entrée :

Workspace

Sortie :

ValidationReport

Responsabilité :

Détecter les incohérences.

Le Validator ne modifie jamais le Workspace.

---

# 67. Compiler

Entrée :

Workspace

Sortie :

CompiledWorkspace

Responsabilité :

Transformer les projets en artefacts prêts à être installés.

Le Compiler ne connaît jamais Anki.

---

# 68. Synchronizer

Entrée :

CompiledWorkspace

Sortie :

SyncReport

Responsabilité :

Installer les artefacts compilés dans un ou plusieurs profils.

Le Synchronizer ne relit jamais les sources.

---

# 69. ProfileManager

Responsabilité :

Découvrir les profils disponibles.

Il fournit :

* la liste des profils ;
* leurs informations principales ;
* leur état d'installation.

Les autres composants ne parcourent jamais directement le répertoire des profils.

---

# 70. BuildManager

Le BuildManager orchestre les différentes étapes de compilation.

Il ne réalise lui-même aucune opération métier.

Il coordonne :

* le Loader ;
* le Validator ;
* le Compiler.

---

# 71. SyncManager

Le SyncManager coordonne les synchronisations.

Il sélectionne :

* le profil courant ;
* ou l'ensemble des profils.

Il délègue ensuite les opérations au Synchronizer.

---

# 72. RuntimeContext

Le RuntimeContext contient les services d'infrastructure.

Il peut notamment fournir :

* HashService ;
* FileSystemService ;
* Logger ;
* Configuration.

Le RuntimeContext ne contient jamais :

* Workspace ;
* Project ;
* Profile ;
* Template.

Ces objets appartiennent au modèle métier.

---

# 73. Services

Les services fournissent des fonctionnalités techniques.

Ils n'implémentent aucune règle métier.

Exemples :

HashService

Calcul des empreintes.

---

FileSystemService

Lecture et écriture des fichiers.

---

Logger

Journalisation.

---

Configuration

Accès aux paramètres.

---

# 74. Règles

Les règles métier sont regroupées dans des composants spécialisés.

Exemple :

ValidationRule

Chaque règle vérifie une propriété unique.

Les règles sont indépendantes.

---

# 75. Organisation du Validator

Le Validator ne contient pas directement toutes les validations.

Il orchestre un ensemble de règles.

Exemple :

```text
Validator

    ├── ManifestRule

    ├── TemplateRule

    ├── CssRule

    ├── AssetRule

    ├── PartialRule

    └── ...
```

Chaque règle est testée indépendamment.

---

# 76. Organisation du Compiler

Le Compiler est composé d'étapes successives.

Exemple :

```text
Compiler

    ├── PartialResolver

    ├── Normalizer

    ├── AssetCollector

    ├── HashCalculator

    └── OutputWriter
```

Chaque étape transforme le résultat de la précédente.

---

# 77. Organisation du Synchronizer

Le Synchronizer est lui aussi composé de sous-composants.

Exemple :

```text
Synchronizer

    ├── ProfileInstaller

    ├── TemplateInstaller

    ├── StylesheetInstaller

    ├── AssetInstaller

    └── InstallationRecorder
```

Cette décomposition facilite les tests.

---

# 78. Communication

Les composants communiquent uniquement :

* par leurs paramètres ;
* par leurs valeurs de retour.

Ils ne communiquent jamais :

* via des variables globales ;
* via des fichiers temporaires ;
* via des effets de bord cachés.

---

# 79. Effets de bord

Les composants autorisés à produire des effets de bord sont explicitement
identifiés : `ProjectLoader` lit les sources, `BuildWriter` écrit les artefacts
jetables et le Synchronizer installe dans Anki. Le Compiler reste pur.

Tous les autres composants sont déterministes.

---

# 80. Gestion des erreurs

Les composants ne capturent que les erreurs qu'ils savent traiter.

Les autres erreurs sont propagées.

Aucun composant ne masque une erreur importante.

---

# 81. Journalisation

Les composants émettent des événements.

Ils n'écrivent jamais directement dans la console.

Le Logger décide :

* du niveau ;
* du format ;
* de la destination.

---

# 82. Tests

Chaque composant possède ses propres tests.

Les composants sont testés indépendamment.

Les tests d'intégration vérifient ensuite leur coopération.

---

# 83. Remplacement

Un composant peut être remplacé par une nouvelle implémentation si :

* son interface publique reste identique ;
* son comportement observable reste conforme à SPEC.md.

---

# 84. Invariants

Les composants respectent les propriétés suivantes.

* Une responsabilité par composant.

* Pas d'état métier partagé.

* Pas de dépendances circulaires.

* Interfaces publiques stables.

* Communication explicite.

Ces règles constituent la base de l'architecture interne du moteur.

# 85. Gouvernance de l'architecture

L'architecture décrite dans ce document constitue la référence du projet.

Toute évolution importante doit être compatible avec les principes définis ici, ou faire l'objet d'une décision d'architecture documentée.

---

# 86. Évolution de l'architecture

L'architecture est conçue pour évoluer progressivement.

Les évolutions doivent privilégier :

* l'ajout de nouveaux composants ;
* l'extension de composants existants ;
* l'amélioration de composants existants.

Les réécritures complètes doivent rester exceptionnelles.

---

# 87. Architecture Decision Records (ADR)

Toute décision importante doit être consignée dans un ADR.

Chaque ADR contient au minimum :

* le contexte ;
* le problème ;
* les solutions envisagées ;
* la solution retenue ;
* les conséquences.

Les ADR sont numérotés chronologiquement.

Exemple :

```text
docs/

    adr/

        ADR-0001-git-source-of-truth.md

        ADR-0002-no-direct-sqlite-access.md

        ADR-0003-build-directory.md
```

---

# 88. Dépendances externes

Toute nouvelle dépendance doit répondre aux critères suivants :

* apporter une réelle valeur ;
* être activement maintenue ;
* posséder une licence compatible ;
* réduire le code plutôt que l'augmenter.

L'ajout d'une dépendance doit être justifié dans un ADR lorsqu'elle devient structurante.

---

# 89. Compatibilité interne

Les interfaces publiques constituent un contrat.

Toute modification incompatible doit être :

* documentée ;
* testée ;
* justifiée.

Les changements de noms arbitraires sont déconseillés.

---

# 90. Compatibilité des données

Les formats suivants sont considérés comme publics :

* metadata.json
* template.json
* Installation Manifest

Leur évolution suit les règles définies dans SPEC.md.

---

# 91. Documentation

Toute nouvelle fonctionnalité importante doit être accompagnée :

* de sa documentation ;
* de ses tests ;
* de sa mise à jour éventuelle dans SPEC.md.

Le code et la documentation évoluent ensemble.

---

# 92. Refactorisation

Une refactorisation ne doit pas modifier le comportement observable.

Lorsqu'un comportement change, il ne s'agit plus d'une simple refactorisation mais d'une évolution fonctionnelle.

---

# 93. Dette technique

La dette technique est suivie explicitement.

Elle n'est jamais cachée dans des commentaires dispersés.

Les éléments connus sont consignés dans la documentation du projet.

---

# 94. Qualité du code

Le projet privilégie :

* la lisibilité ;
* la simplicité ;
* la cohérence ;
* la testabilité.

Une implémentation légèrement plus longue mais plus compréhensible est généralement préférée.

---

# 95. Organisation des modules

Un module ne doit pas devenir excessivement volumineux.

Lorsqu'un module atteint une taille importante ou cumule plusieurs responsabilités, il doit être scindé.

La taille seule n'est pas un critère suffisant : la cohésion reste le facteur déterminant.

---

# 96. Interfaces publiques

Chaque module expose une API publique clairement identifiée.

Les éléments internes ne doivent pas être utilisés par les autres modules.

Cette séparation facilite les refactorisations futures.

---

# 97. Observabilité

Le moteur doit permettre de comprendre son fonctionnement.

Les événements, diagnostics et rapports constituent les principaux outils d'observabilité.

Les journaux doivent être suffisamment détaillés pour faciliter le diagnostic sans devenir excessivement verbeux.

---

# 98. Sécurité

Le moteur applique le principe du moindre privilège.

Chaque composant ne manipule que les données nécessaires à sa responsabilité.

Les écritures sur le disque sont limitées aux répertoires prévus.

---

# 99. Philosophie générale

L'architecture poursuit quatre objectifs principaux.

* Compréhensible.

Un nouveau développeur doit pouvoir comprendre rapidement l'organisation du projet.

* Prévisible.

Le comportement du moteur doit être facile à anticiper.

* Évolutive.

Les nouvelles fonctionnalités doivent s'intégrer naturellement.

* Fiable.

Les erreurs doivent être détectées le plus tôt possible.

---

# 100. Résumé

Le projet repose sur les principes suivants :

* Git est la source de vérité.
* Les profils Anki sont uniquement des cibles de déploiement.
* Le modèle métier constitue le cœur du projet.
* Les composants possèdent chacun une responsabilité unique.
* Les effets de bord sont limités au Synchronizer.
* Les diagnostics sont structurés et indépendants de l'interface.
* Les tests font partie intégrante du projet.
* Les décisions d'architecture sont documentées.

Toute évolution future doit préserver ces principes ou faire l'objet d'une décision d'architecture explicite.

Fin du document.

