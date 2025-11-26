from models.case import Propriete

class Gare(Propriete):
    def __init__(self, nom: str, position: int):
        super().__init__(nom, position, prix=200, loyer=25, couleur="gare")
    
    def calculer_loyer(self) -> int:
        if self.hypothequee or not self.proprietaire:
            return 0
        nb_gares = sum(1 for p in self.proprietaire.proprietes if isinstance(p, Gare))
        return 25 * (2 ** (nb_gares - 1))