# IMPLEMENTATION.md

Version : 1.0 (Draft)

---

# Objectif

Ce document sert de journal de mise en œuvre.

Il complète :

* SPEC.md
* ARCHITECTURE.md
* ROADMAP.md
* CONTRIBUTING.md

Il est mis à jour tout au long du développement.

---

# État du projet

| Élément           | État |
| ----------------- | ---- |
| SPEC.md           | ✅    |
| ARCHITECTURE.md   | ✅    |
| ROADMAP.md        | ✅    |
| CONTRIBUTING.md   | ✅    |
| IMPLEMENTATION.md | 🚧   |

---

# Phase -1 — Exploration

## API Anki

* [ ] Vérifier l'API officielle disponible.
* [ ] Identifier les méthodes de lecture des types de notes.
* [ ] Identifier les méthodes de modification des types de notes.
* [ ] Vérifier comment modifier les templates.
* [ ] Vérifier comment modifier le CSS.
* [ ] Vérifier comment enregistrer les modifications.

### Résultat

À compléter.

---

## Données privées

* [ ] Identifier le meilleur emplacement de stockage.
* [ ] Vérifier que les données survivent aux redémarrages.
* [ ] Vérifier qu'elles sont propres à chaque profil.

### Résultat

À compléter.

---

## CSS

* [ ] Vérifier le fonctionnement de `@import`.
* [ ] Vérifier le comportement avec plusieurs feuilles.
* [ ] Vérifier la copie des ressources.

### Résultat

À compléter.

---

# Phase 0 — Initialisation

## Dépôt

* [ ] Créer le dépôt Git.
* [x] Ajouter `.gitignore`.
* [x] Ajouter `README.md`.

---

## Python

* [x] Créer `pyproject.toml`.
* [x] Choisir la version minimale de Python (3.12).
* [ ] Configurer l'environnement virtuel.

---

## Structure

* [x] Créer `src/`.
* [x] Créer `project/`.
* [x] Créer `build/`.
* [x] Créer `addon/`.
* [x] Créer `tests/`.
* [x] Créer `docs/`.

---

## Outils

* [ ] Installer pytest.
* [ ] Configurer Ruff.
* [ ] Configurer Black.
* [ ] Configurer MyPy (optionnel).

---

# Phase 1 — Modèle métier

## Workspace

* [x] Créer la dataclass.
* [x] Ajouter les tests.

---

## NoteType (projet de type de note)

* [x] Créer la dataclass.
* [x] Ajouter les tests.

---

## Manifest

* [x] Créer la dataclass.
* [ ] Ajouter les tests.

---

## Template

* [x] Créer la dataclass.
* [ ] Ajouter les tests.

---

## Partial

* [x] Créer la dataclass.
* [ ] Ajouter les tests.

---

## Stylesheet

* [x] Créer la dataclass.
* [ ] Ajouter les tests.

---

## Asset

* [x] Créer la dataclass.
* [ ] Ajouter les tests.

---

## Reports

* [x] BuildReport.
* [x] ValidationReport.
* [x] SyncReport.

---

# Phase 2 — Loader

## Lecture

* [x] Workspace.
* [x] Projects.
* [x] Templates.
* [x] Partials.
* [x] CSS.
* [x] Assets.

---

## Tests

* [x] Projet minimal.
* [x] Plusieurs projets.
* [ ] Projet vide.

---

# Phase 3 — Validator

## Manifests

* [ ] Validation JSON Schema.
* [x] Validation métier.

---

## Templates

* [x] Existence.
* [ ] Doublons.

---

## Partials

* [x] Existence.
* [x] Cycles.

---

## CSS

* [x] Existence.
* [ ] Encodage.

---

## Diagnostics

* [x] Codes.
* [x] Messages.
* [ ] Suggestions.

---

# Phase 4 — Compiler

## Partials

* [x] Résolution simple.
* [x] Résolution récursive.
* [x] Détection des cycles.

---

## Build

* [x] Génération des templates.
* [x] Génération des manifests.
* [x] Génération des hashes.

---

## Tests

* [x] Déterminisme.
* [ ] Comparaison avec les golden files.

---

# Phase 5 — Synchronizer

## Profil courant

* [ ] Découverte.
* [ ] Lecture de l'état.
* [x] Comparaison des hashes.
* [x] Installation via un adaptateur Anki injecté.

---

## Plusieurs profils

* [ ] Découverte.
* [ ] Boucle.
* [ ] Rapport global.

---

## Dry Run

* [x] Aucune modification.
* [x] Rapport complet.

---

# Phase 6 — Add-on

## Menus

* [ ] Synchroniser le profil courant.
* [ ] Synchroniser tous les profils.
* [ ] Simulation.

---

## Interface

* [ ] Barre de progression.
* [ ] Journal.
* [ ] Rapport.

---

# Tests finaux

## Validation

* [ ] Tous les tests passent.

---

## Documentation

* [ ] Vérifier SPEC.md.
* [ ] Vérifier ARCHITECTURE.md.
* [ ] Vérifier ROADMAP.md.
* [ ] Vérifier CONTRIBUTING.md.

---

## Publication

* [x] CHANGELOG.
* [ ] Numéro de version.
* [ ] Tag Git.

---

# Journal

## YYYY-MM-DD

### Décisions

À compléter.

### Difficultés

À compléter.

### Solutions

À compléter.

### ADR créés

À compléter.

---

# Idées futures

Les idées non planifiées sont notées ici.

Elles ne doivent pas interrompre le développement en cours.

Avant d'être implémentée, chaque idée doit répondre aux questions suivantes :

* Quel problème résout-elle ?
* Est-elle compatible avec SPEC.md ?
* Est-elle réellement nécessaire ?
* Peut-elle attendre une version ultérieure ?

Une idée n'entre dans la roadmap qu'après avoir été analysée.

---

# Définition de terminé

Le projet est considéré comme terminé lorsque :

* toutes les tâches prévues sont réalisées ;
* tous les tests passent ;
* la documentation est à jour ;
* aucune régression connue n'est présente ;
* une version stable peut être publiée.
