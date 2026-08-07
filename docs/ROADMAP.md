# ROADMAP.md

Version : 1.0 (Draft)

---

# Objectif

Cette feuille de route décrit les différentes étapes de développement du projet.

Chaque étape doit produire une version stable et utilisable.

Le projet est développé de manière incrémentale.

Une fonctionnalité n'est considérée comme terminée que lorsqu'elle est :

* implémentée ;
* testée ;
* documentée.

---

# Principes

Le développement suit les principes suivants.

* Une seule fonctionnalité majeure à la fois.
* Le projet doit toujours rester exécutable.
* Les tests accompagnent le développement.
* Les optimisations viennent après les fonctionnalités.
* La simplicité est privilégiée.

---

# Phase 0 — Initialisation

## Objectifs

Créer les fondations du projet.

## Tâches

* Initialiser le dépôt Git.
* Mettre en place la structure des dossiers.
* Configurer Python.
* Configurer les outils de développement.
* Ajouter les documents du projet.
* Mettre en place les tests.

## Critères de réussite

* Le dépôt compile.
* Les tests peuvent être lancés.
* Les documents existent.

---

# Phase 1 — Modèle métier

## Objectifs

Créer tous les objets du modèle.

## Tâches

* Workspace
* Project
* Manifest
* Template
* Partial
* Stylesheet
* Asset
* Profile
* Reports

## Critères

* Les objets sont immuables.
* Les tests unitaires passent.

---

# Phase 2 — Loader

## Objectifs

Construire le modèle à partir des fichiers.

## Fonctionnalités

* découverte des projets
* lecture des manifests
* lecture des templates
* lecture des partials
* lecture des feuilles CSS
* lecture des assets

## Critères

* Tous les objets sont correctement chargés.
* Aucun traitement métier.

---

# Phase 3 — Validator

## Objectifs

Détecter les erreurs.

## Fonctionnalités

* validation JSON
* validation métier
* diagnostics
* ValidationReport

## Critères

* Les projets invalides sont refusés.
* Les diagnostics sont corrects.

---

# Phase 4 — Compiler

## Objectifs

Produire les artefacts compilés.

## Fonctionnalités

* résolution des partials
* normalisation
* génération des templates
* génération du répertoire build

## Critères

* Compilation déterministe.
* Deux compilations successives produisent les mêmes résultats.

---

# Phase 5 — Hashes

## Objectifs

Mettre en place la détection des modifications.

## Fonctionnalités

* HashService
* Source Hash
* Compiled Hash

## Critères

* Une modification entraîne un hash différent.
* Deux compilations identiques produisent le même hash.

---

# Phase 6 — Tests d'intégration

## Objectifs

Valider l'ensemble du pipeline.

## Fonctionnalités

* projets valides
* projets invalides
* compilation
* rapports

## Critères

* Tous les scénarios principaux sont testés.

---

# Phase 7 — Synchronizer

## Objectifs

Installer les artefacts dans un profil.

## Fonctionnalités

* découverte du profil courant
* comparaison des hashes
* installation
* manifeste d'installation

## Critères

* Une seconde synchronisation n'effectue aucune modification.

---

# Phase 8 — Plusieurs profils

## Objectifs

Synchroniser plusieurs profils.

## Fonctionnalités

* découverte automatique
* boucle de synchronisation
* rapport global

## Critères

* Une erreur sur un profil n'interrompt pas les autres.

---

# Phase 9 — Add-on Anki

## Objectifs

Créer l'interface utilisateur.

## Fonctionnalités

* menu
* synchroniser le profil courant
* synchroniser tous les profils

## Critères

* Le moteur est utilisable depuis Anki.

---

# Phase 10 — Interface avancée

## Fonctionnalités

* barre de progression
* mode simulation
* rapport détaillé
* journal

---

# Phase 11 — Optimisations

## Fonctionnalités

* cache
* amélioration des performances
* optimisation des copies
* optimisation des validations

Aucune optimisation ne doit modifier le comportement observable.

---

# Phase 12 — Publication

## Objectifs

Préparer une première version stable.

## Tâches

* revue complète du code
* nettoyage
* documentation
* tests finaux
* changelog
* numéro de version

---

# Fonctionnalités futures

Les fonctionnalités suivantes ne font pas partie de la première version.

* Suppression automatique des types de notes.
* Prévisualisation graphique des cartes.
* Ligne de commande (CLI).
* Génération automatique de documentation.
* Gestion de plusieurs feuilles CSS.
* Compilation SCSS.
* Variables de templates.
* Plugins.

Elles pourront être développées ultérieurement.

---

# Définition de terminé (Definition of Done)

Une tâche est terminée uniquement si :

* le code compile ;
* les tests passent ;
* la documentation est à jour ;
* les diagnostics sont documentés si nécessaire ;
* aucune régression n'est introduite.

---

# Priorités

Les priorités sont les suivantes :

1. Fiabilité.
2. Simplicité.
3. Lisibilité.
4. Testabilité.
5. Performances.

Les performances ne priment jamais sur la fiabilité.

---

# Jalons

## MVP

Le MVP est atteint lorsque :

* le projet peut être chargé ;
* validé ;
* compilé ;
* synchronisé avec un profil Anki.

## Version 1.0

La version 1.0 est atteinte lorsque toutes les phases précédentes sont terminées, documentées et testées.

Fin du document.