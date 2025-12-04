from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from models.case import Case, Propriete
    from models.joueur import Joueur

class StatistiquesPartie:
    """Collecte des statistiques sur une partie"""
    def __init__(self):
        self.passages_par_case: Dict[int, int] = {}
        self.revenus_par_propriete: Dict[str, int] = {}
        self.duree_partie = 0
        self.nb_tours = 0
        self.gagnant = None
    
    def enregistrer_passage(self, case: 'Case'):
        """Enregistre le passage sur une case"""
        if case.position not in self.passages_par_case:
            self.passages_par_case[case.position] = 0
        self.passages_par_case[case.position] += 1
    
    def enregistrer_loyer(self, propriete: 'Propriete', montant: int):
        """Enregistre un paiement de loyer"""
        if propriete.nom not in self.revenus_par_propriete:
            self.revenus_par_propriete[propriete.nom] = 0
        self.revenus_par_propriete[propriete.nom] += montant
    
    def afficher_statistiques(self):
        """Affiche un résumé des statistiques"""
        print("\n" + "="*60)
        print("STATISTIQUES DE LA PARTIE")
        print("="*60)
        
        print(f"\nDurée: {self.nb_tours} tours")
        if self.gagnant:
            print(f"Gagnant: {self.gagnant.nom} ({self.gagnant.argent}€)")

        print("\nTop 5 des cases les plus visitées:")
        top_cases = sorted(self.passages_par_case.items(),
                          key=lambda x: x[1], reverse=True)[:5]
        for position, nb in top_cases:
            print(f" Position {position}: {nb} passages")

        if self.revenus_par_propriete:
            print("\nTop 5 des propriétés les plus rentables:")
            top_props = sorted(self.revenus_par_propriete.items(),
                             key=lambda x: x[1], reverse=True)[:5]
            for nom, revenus in top_props:
                print(f" {nom}: {revenus}€ de loyers")