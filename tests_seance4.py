#!/usr/bin/env python3

from game.monopoly import Monopoly
from models.ia import IAAgressive, IAConservative, IAStrategique

def tester_strategies():
    print("\nTEST DES STRATÉGIES IA")
    
    strategies = [
        ("Agressive", IAAgressive()),
        ("Conservative", IAConservative()),
        ("Stratégique", IAStrategique())
    ]
    
    for nom_strat, strat in strategies:
        print(f"\n{'='*60}")
        print(f"Stratégie: {nom_strat}")
        print(f"{'='*60}")
        
        joueurs_config = [(f"IA1_{nom_strat}", strat), (f"IA2_{nom_strat}", strat), (f"IA3_{nom_strat}", strat)]
        jeu = Monopoly(joueurs_config)
        gagnant = jeu.jouer_partie(max_tours=50)
        
        if gagnant:
            print(f"Gagnant: {gagnant.nom}")
        
        jeu.stats.afficher_statistiques()

if __name__ == "__main__":
    print("=== TESTS SÉANCE 4 - IA ET STATISTIQUES ===")
    tester_strategies()
    print("\n=== FIN DES TESTS ===")