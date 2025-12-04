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
    jeu.stats.afficher_statistiques()

if __name__ == "__main__":
    main()
