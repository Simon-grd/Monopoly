from typing import List
from models.case import Case, Propriete, CaseSpeciale

class Plateau:
    def __init__(self):
        self.cases: List[Case] = []
        self._creer_plateau()
    
    def _creer_plateau(self):
        self.cases.append(CaseSpeciale("Départ", 0, "depart"))
        self.cases.append(Propriete("Boulevard de Belleville", 1, 60, 2, "marron"))
        self.cases.append(CaseSpeciale("Caisse de Communauté", 2, "caisse"))
        self.cases.append(Propriete("Rue Lecourbe", 3, 60, 4, "marron"))
        self.cases.append(CaseSpeciale("Impôts sur le revenu", 4, "impot"))
        self.cases.append(Propriete("Gare Montparnasse", 5, 200, 25, "gare"))
        self.cases.append(Propriete("Rue de Vaugirard", 6, 100, 6, "bleu clair"))
        self.cases.append(CaseSpeciale("Chance", 7, "chance"))
        self.cases.append(Propriete("Rue de Courcelles", 8, 100, 6, "bleu clair"))
        self.cases.append(Propriete("Avenue de la République", 9, 120, 8, "bleu clair"))
        
        self.cases.append(CaseSpeciale("Prison", 10, "prison"))
        self.cases.append(Propriete("Boulevard de la Villette", 11, 140, 10, "rose"))
        self.cases.append(Propriete("Compagnie d'Électricité", 12, 150, 0, "service"))
        self.cases.append(Propriete("Avenue de Neuilly", 13, 140, 10, "rose"))
        self.cases.append(Propriete("Rue de Paradis", 14, 160, 12, "rose"))
        self.cases.append(Propriete("Gare de Lyon", 15, 200, 25, "gare"))
        self.cases.append(Propriete("Avenue Mozart", 16, 180, 14, "orange"))
        self.cases.append(CaseSpeciale("Caisse de Communauté", 17, "caisse"))
        self.cases.append(Propriete("Boulevard Saint-Michel", 18, 180, 14, "orange"))
        self.cases.append(Propriete("Place Pigalle", 19, 200, 16, "orange"))
        
        self.cases.append(CaseSpeciale("Parc Gratuit", 20, "parc"))
        self.cases.append(Propriete("Avenue Matignon", 21, 220, 18, "rouge"))
        self.cases.append(CaseSpeciale("Chance", 22, "chance"))
        self.cases.append(Propriete("Boulevard Malesherbes", 23, 220, 18, "rouge"))
        self.cases.append(Propriete("Avenue Henri-Martin", 24, 240, 20, "rouge"))
        self.cases.append(Propriete("Gare du Nord", 25, 200, 25, "gare"))
        self.cases.append(Propriete("Faubourg Saint-Honoré", 26, 260, 22, "jaune"))
        self.cases.append(Propriete("Place de la Bourse", 27, 260, 22, "jaune"))
        self.cases.append(Propriete("Compagnie des Eaux", 28, 150, 0, "service"))
        self.cases.append(Propriete("Rue La Fayette", 29, 280, 24, "jaune"))
        
        self.cases.append(CaseSpeciale("Allez en Prison", 30, "allez_prison"))
        self.cases.append(Propriete("Avenue de Breteuil", 31, 300, 26, "vert"))
        self.cases.append(Propriete("Avenue Foch", 32, 300, 26, "vert"))
        self.cases.append(CaseSpeciale("Caisse de Communauté", 33, "caisse"))
        self.cases.append(Propriete("Boulevard des Capucines", 34, 320, 28, "vert"))
        self.cases.append(Propriete("Gare Saint-Lazare", 35, 200, 25, "gare"))
        self.cases.append(CaseSpeciale("Chance", 36, "chance"))
        self.cases.append(Propriete("Avenue des Champs-Élysées", 37, 350, 35, "bleu foncé"))
        self.cases.append(CaseSpeciale("Taxe de Luxe", 38, "taxe_luxe"))
        self.cases.append(Propriete("Rue de la Paix", 39, 400, 40, "bleu foncé"))
    
    def get_case(self, position: int) -> Case:
        return self.cases[position % len(self.cases)]