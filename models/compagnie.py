from typing import TYPE_CHECKING
from models.case import Propriete

if TYPE_CHECKING:
    from models.joueur import Joueur
    from game.monopoly import Monopoly

class Compagnie(Propriete):
    def __init__(self, nom: str, position: int):
        super().__init__(nom, position, prix=150, loyer=0, couleur="compagnie")
        self.dernier_lancer_des = 0
    
    def calculer_loyer(self) -> int:
        if self.hypothequee or not self.proprietaire:
            return 0
        nb_compagnies = sum(1 for p in self.proprietaire.proprietes if isinstance(p, Compagnie))
        multiplicateur = 4 if nb_compagnies == 1 else 10
        return self.dernier_lancer_des * multiplicateur
    
    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        self.dernier_lancer_des = jeu.dernier_total_des
        super().action(joueur, jeu)