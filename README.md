# Monopoly - Jeu Python

Implémentation complète du jeu Monopoly en Python avec architecture modulaire et intelligence artificielle.

## 🎮 Lancer le jeu

```bash
python main.py
```

## 📋 Configuration

- **Joueur 1** : Obligatoirement humain
- **Joueurs 2-4** : Humain ou IA (Agressive, Conservative, Stratégique)
- **Total** : 2 à 4 joueurs

### Types d'IA

- **IA Agressive** : Achète systématiquement toutes les propriétés
- **IA Conservative** : Achète seulement si argent > 2× prix
- **IA Stratégique** : Privilégie les quartiers complets + construction intelligente

## 📁 Structure

```
Monopoly/
├── models/          # Modèles de données
│   ├── case.py     # Cases, Propriétés, Cases spéciales
│   ├── joueur.py   # Joueur
│   ├── plateau.py  # Plateau
│   ├── cartes.py   # Cartes Chance et Communauté
│   ├── gare.py     # Gares
│   ├── compagnie.py # Compagnies
│   ├── ia.py       # Stratégies IA
│   └── statistiques.py # Statistiques de partie
├── game/           # Logique du jeu
│   └── monopoly.py # Classe principale
├── ui/             # Interface utilisateur
│   └── interface.py # Configuration des joueurs
└── main.py         # Point d'entrée
```

## ✨ Fonctionnalités

### Jeu complet
- ✅ Plateau de 40 cases
- ✅ Propriétés, gares, compagnies
- ✅ Achat et loyers
- ✅ Construction de maisons et hôtels
- ✅ Cases spéciales (Départ, Prison, Taxes, Parc)
- ✅ Cartes Chance et Caisse de Communauté
- ✅ Système de prison complet
- ✅ Gestion des faillites

### Intelligence Artificielle
- ✅ 3 stratégies d'IA distinctes
- ✅ Décisions d'achat automatiques
- ✅ Construction intelligente (IA Stratégique)
- ✅ Parties mixtes humains/IA

### Statistiques
- ✅ Cases les plus visitées
- ✅ Propriétés les plus rentables
- ✅ Durée des parties
- ✅ Identification du gagnant

## 🧪 Tests

```bash
python tests_seance4.py
```

## 🎯 Commandes du jeu

- `jouer` - Lancer les dés et se déplacer
- `construire` - Construire maisons/hôtels
- `hypothequer` - Hypothéquer une propriété
- `infos` - Voir ses informations
- `plateau` - Voir l'état du plateau
- `joueurs` - Voir tous les joueurs
- `quitter` - Arrêter la partie

## 📝 Règles implémentées

- Passage par la case Départ : +200€
- Arrivée sur la case Départ : +200€ bonus
- Prison : 3 façons de sortir (carte, payer 50€, double)
- Construction équitable dans un quartier
- Loyers doublés sur monopole sans construction
- Faillite avec transfert des propriétés
- 32 maisons et 12 hôtels disponibles
