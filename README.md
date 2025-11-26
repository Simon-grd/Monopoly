# Monopoly - Jeu Python

Implémentation complète du jeu Monopoly en Python avec architecture modulaire.

## 🎮 Lancer le jeu

```bash
python main.py
```

## 📁 Structure du projet

```
Monopoly/
├── models/              # Modèles de données
│   ├── case.py         # Classes Case, Propriete, CaseSpeciale
│   ├── joueur.py       # Classe Joueur
│   ├── plateau.py      # Classe Plateau
│   ├── cartes.py       # Cartes Chance et Communauté
│   ├── gare.py         # Classe Gare
│   ├── compagnie.py    # Classe Compagnie
│   └── db.py           # Accès base de données (optionnel)
├── game/               # Logique du jeu
│   └── monopoly.py     # Classe Monopoly principale
├── ui/                 # Interface utilisateur
│   └── terminal.py     # Interface terminal
├── main.py             # Point d'entrée
├── tests_seance2.py    # Tests séance 2
└── tests_seance3.py    # Tests séance 3
```

## ✨ Fonctionnalités

### Séance 1 : Base du jeu
- ✅ Plateau de 40 cases
- ✅ Propriétés, gares, compagnies
- ✅ Déplacement des joueurs
- ✅ Achat de propriétés
- ✅ Paiement des loyers

### Séance 2 : Mécanique de jeu
- ✅ Cases spéciales (Départ, Prison, Taxes, Parc)
- ✅ Construction de maisons et hôtels
- ✅ Calcul des loyers avec constructions
- ✅ Gares avec loyers progressifs (25€, 50€, 100€, 200€)
- ✅ Compagnies avec loyers basés sur les dés (4× ou 10×)
- ✅ Système de monopole

### Séance 3 : Jouabilité complète
- ✅ Système de prison complet (3 façons de sortir)
- ✅ Cartes Chance et Caisse de Communauté
- ✅ Gestion des faillites
- ✅ Partie complète avec élimination
- ✅ Accès base de données MySQL (optionnel)

## 🧪 Tests

```bash
# Tests séance 2
python tests_seance2.py

# Tests séance 3
python tests_seance3.py
```

## 🗄️ Base de données (optionnel)

### Installation
```bash
pip install mysql-connector-python
```

### Configuration
1. Créer la base `monopoly`
2. Créer l'utilisateur `monopoly_user` / `monopoly_pass`
3. Exécuter le script SQL fourni

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

## 👥 Auteurs

Projet réalisé dans le cadre du TP Monopoly