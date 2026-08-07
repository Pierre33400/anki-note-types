# CONTRIBUTING.md

Version : 1.0 (Draft)

---

# Objectif

Ce document définit les conventions de développement du projet.

Son objectif est de garantir :

* une architecture cohérente ;
* un style de code homogène ;
* une maintenance facilitée ;
* des évolutions prévisibles.

Ces règles s'appliquent à tout le code du projet.

---

# Philosophie

Le projet privilégie :

* la simplicité ;
* la lisibilité ;
* la fiabilité ;
* la testabilité.

Une solution simple est préférée à une solution sophistiquée si elles répondent au même besoin.

---

# Organisation des modules

Chaque module possède une responsabilité unique.

Avant de créer un nouveau module, se demander :

> Peut-on ajouter cette fonctionnalité dans un module existant sans lui donner une seconde responsabilité ?

Si la réponse est non, créer un nouveau module.

---

# Organisation des fichiers

Un fichier ne doit pas devenir excessivement volumineux.

À titre indicatif :

* moins de 300 lignes : idéal ;
* 300 à 600 lignes : acceptable ;
* plus de 600 lignes : envisager un découpage.

Ces seuils sont indicatifs.

La cohésion reste le critère principal.

---

# Nommage

Les noms doivent être explicites.

Préférer :

```text
PartialResolver
```

à :

```text
Resolver
```

Préférer :

```text
InstallationManifest
```

à :

```text
Manifest2
```

Éviter les abréviations inutiles.

---

# Style Python

Le projet suit :

* PEP 8 ;
* PEP 257 (docstrings).

Utiliser des annotations de types partout où elles apportent de la clarté.

---

# Dataclasses

Les objets du modèle sont, par défaut, des dataclasses immuables.

Les classes classiques sont réservées :

* aux composants ;
* aux services ;
* aux orchestrateurs.

---

# Fonctions

Les fonctions doivent être courtes.

Une fonction devrait généralement faire une seule chose.

Si un commentaire devient nécessaire pour expliquer une partie d'une fonction, envisager d'extraire cette partie dans une nouvelle fonction.

---

# Commentaires

Le code doit être compréhensible sans commentaires excessifs.

Les commentaires expliquent :

* le pourquoi ;
* jamais le quoi.

Exemple :

Bon :

```python
# Le hash est calculé avant normalisation afin de détecter
# les modifications des sources.
```

Mauvais :

```python
# Incrémente i.
i += 1
```

---

# TODO

Éviter les commentaires :

```python
# TODO
```

Préférer :

* une entrée dans `ROADMAP.md` ;
* une issue Git.

---

# Gestion des erreurs

Les erreurs attendues deviennent des diagnostics.

Les erreurs inattendues deviennent des exceptions.

Ne jamais masquer une exception sans raison.

---

# Journalisation

Ne jamais utiliser directement :

```python
print(...)
```

Utiliser le Logger du projet.

---

# Dépendances

Avant d'ajouter une dépendance externe :

1. Vérifier si la bibliothèque standard suffit.
2. Vérifier la licence.
3. Vérifier la maintenance du projet.
4. Documenter la raison de son ajout.

---

# Tests

Toute fonctionnalité importante est accompagnée de tests.

Toute correction de bug est accompagnée d'un test de régression.

Les tests doivent rester lisibles.

---

# Documentation

Toute nouvelle fonctionnalité implique, si nécessaire :

* une mise à jour de `SPEC.md` ;
* une mise à jour de `ARCHITECTURE.md` ;
* une mise à jour de `ROADMAP.md` ;
* une mise à jour du `CHANGELOG.md`.

La documentation est considérée comme du code.

---

# Commits

Les commits doivent être :

* petits ;
* atomiques ;
* explicites.

Exemples :

```text
Add partial dependency graph

Validate template manifests

Implement HashService
```

Éviter :

```text
Update

Fixes

Various changes
```

---

# Branches

Au début du projet, le développement se fait sur :

```text
main
```

Des branches dédiées pourront être introduites si le projet devient collaboratif.

---

# Architecture Decision Records

Toute décision importante est documentée dans un ADR.

Les ADR ne sont jamais supprimés.

Si une décision évolue, un nouvel ADR est créé.

---

# Refactorisation

Une refactorisation :

* ne change pas le comportement observable ;
* conserve les tests existants ;
* améliore la structure du code.

Si le comportement change, il ne s'agit plus d'une simple refactorisation.

---

# Compatibilité

Les interfaces publiques sont considérées comme stables.

Toute modification incompatible doit être documentée.

---

# Revue personnelle

Avant chaque commit important, vérifier :

* le code est-il plus simple qu'avant ?
* les responsabilités sont-elles toujours bien séparées ?
* les tests passent-ils ?
* la documentation est-elle encore correcte ?
* une dépendance supplémentaire est-elle réellement nécessaire ?

---

# Principe du moindre étonnement

Le projet doit rester prévisible.

Un nouveau développeur (ou toi-même dans un an) doit pouvoir anticiper le comportement du code en lisant son nom et sa structure.

---

# Règle d'or

Lorsqu'un choix est difficile :

Choisir la solution :

* la plus simple ;
* la plus lisible ;
* la plus facile à tester.

L'architecture doit servir le projet.

Le projet ne doit jamais être compliqué uniquement pour satisfaire l'architecture.

Fin du document.
