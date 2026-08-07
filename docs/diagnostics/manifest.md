# Diagnostics des manifestes

Les métadonnées de types de notes doivent respecter
`project/schema/metadata.schema.json`. Le champ `schemaVersion` est obligatoire.

| Code | Signification |
| --- | --- |
| `invalid-json` | Un manifeste ne contient pas du JSON valide. |
| `invalid-schema-version` | La version de schéma n'est pas prise en charge. |
| `invalid-manifest-field` | Un champ obligatoire est absent ou invalide. |
| `unknown-manifest-field` | Un champ non prévu par le contrat est présent. |
