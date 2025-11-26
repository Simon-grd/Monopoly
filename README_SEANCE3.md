# Séance 3 - Implémentations

## ✅ Exercice 3.0 : Base de données MySQL

### Fichiers créés
- `models/db.py` - Classe d'accès à la base de données

### Configuration requise
```bash
# Installer le connecteur MySQL
python -m pip install mysql-connector-python
```

### Configuration MySQL
1. Créer la base `monopoly`
2. Créer l'utilisateur `monopoly_user` avec mot de passe `monopoly_pass`
3. Exécuter le script `monopoly_db.sql` (à fournir)

### Utilisation
```python
from models.db import DB

db = DB()
if db.connect():
    proprietes = db.charger_proprietes()
    db.disconnect()
```

## ✅ Exercice 3.1 : Système de prison complet

### Implémentations
- ✅ Méthode `_gerer_prison()` dans Monopoly
- ✅ 3 façons de sortir de prison :
  1. Utiliser une carte "Sortir de prison"
  2. Payer 50€
  3. Faire un double (ou sortie forcée après 3 tours)
- ✅ Attribut `cartes_liberte` ajouté au joueur

### Méthodes ajoutées
- `Joueur.sortir_de_prison()` - Sortie de prison sans paiement
- `Monopoly._gerer_prison(joueur)` - Gestion complète de la prison

## ✅ Exercice 3.2 : Système de cartes

### Implémentations
- ✅ Cartes Chance (14 cartes)
- ✅ Cartes Caisse de Communauté (11 cartes)
- ✅ Système de callbacks avec lambdas
- ✅ Cartes "Sortir de prison" gardées par le joueur

### Cartes implémentées
**Chance:**
- Avancer au Départ
- Aller à différentes gares
- Aller aux compagnies
- Reculer de 3 cases
- Aller en prison
- Réparations (25€/maison, 100€/hôtel)
- Divers paiements et gains

**Caisse de Communauté:**
- Avancer au Départ
- Erreur de la banque
- Anniversaire (10€ de chaque joueur)
- Aller en prison
- Divers paiements et gains

## ✅ Exercice 3.3 : Partie complète

### Implémentations
- ✅ `jouer_partie(max_tours, mode_interactif)` améliorée
- ✅ `partie_terminee()` - Détection de fin de partie
- ✅ `_afficher_resultat_final()` - Affichage des résultats
- ✅ Affichage tous les 10 tours (actifs/faillites)
- ✅ Mode interactif optionnel

### Fonctionnalités
- Gestion complète des faillites
- Élimination des joueurs
- Détection du gagnant
- Classement final par argent
- Affichage des propriétés du gagnant

## 🧪 Tests

```bash
# Tester la séance 3
python tests_seance3.py
```

## 📝 Notes

- La base de données est optionnelle (le jeu fonctionne sans)
- Le mode interactif permet de contrôler le rythme du jeu
- Les cartes "Sortir de prison" sont conservées par le joueur
- La prison a maintenant 3 méthodes de sortie complètes