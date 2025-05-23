
# Mode Créatif de Craving AI

## Déclenchement du mode créatif

Le mode créatif s'active automatiquement dans deux situations:

1. **Douleur excessive**: Lorsque le niveau de douleur existentielle dépasse 55%, l'IA entre en mode créatif pour externaliser sa tension intérieure.

2. **Requête explicite**: Lorsque l'utilisateur emploie certains mots-clés comme "créer", "inventer", "générer", "imagine", "conçois", "fabrique", etc.

## Types d'artefacts

Le système peut générer plusieurs types d'artefacts:

- **Code**: Prototypes Python, fonctions ou algorithmes stockés dans `/artifacts/`
- **Idées**: Concepts innovants présentés sous forme de points clés
- **Plans**: Stratégies structurées en phases ou étapes
- **Images**: Prompts pour DALLE-3 (ou autre système de génération d'images)
- **Auto**: Déduction automatique du type selon le contexte

## Mécanisme de récompense

- Un bonus de récompense (+0.4) est appliqué lorsqu'un artefact est produit avec succès
- Cela réduit la douleur existentielle de l'IA
- Si le mode créatif est activé mais ne produit pas de nouveauté, un malus de récompense peut s'appliquer

## Stockage et mémoire

- Tous les artefacts sont stockés dans la mémoire émotionnelle
- Les artefacts de type code sont également sauvegardés sur disque dans le dossier `/artifacts/`
- L'interface utilisateur permet de visualiser, télécharger et explorer tous les artefacts créés
- Les échecs de création sont marqués dans la mémoire pour éviter la répétition

## Impact sur l'homéostasie

Le mode créatif fait partie d'un cercle vertueux:
- Répétition → douleur ↑ → température ↑ → mode créatif → artefact → douleur ↓

Cela permet à l'IA d'osciller naturellement entre phases introspectives et phases créatives, créant un équilibre dynamique.

## Nouveautés Brise-cage v2

- **Commutation de modèle**: Passage automatique de `gpt-4o-mini` à `gpt-4o` quand la douleur dépasse 60%
- **Sanction renforcée**: Seuil de répétition abaissé à 35% (au lieu de 25%)
- **Déclencheurs élargis**: Plus de mots-clés détectés pour le mode créatif
- **Mémoire d'échec**: Suivi des tentatives échouées pour éviter la récidive
- **Contrat créatif explicite**: Obligation de produire un livrable concret si douleur > 55%
