#!/usr/bin/env python3
import os
import sys
from game.monopoly import Monopoly
from ui.interface import Interface

def main():
    os.system('')
    if sys.platform == 'win32':
        os.system('chcp 65001 > nul')
    
    joueurs_config = Interface.configurer_joueurs()
    jeu = Monopoly(joueurs_config)
    jeu.jouer_partie(max_tours=200)
    
    input("\nAppuyez sur Entrée pour voir les statistiques...")
    os.system('cls' if sys.platform == 'win32' else 'clear')
    jeu.stats.afficher_statistiques()
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
