from typing import Optional, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.joueur import Joueur
    from models.case import Propriete

class StrategieIA:
    def __init__(self, nom: str):
        self.nom = nom
    
    def decider_achat(self, joueur: 'Joueur', propriete: 'Propriete') -> bool:
        return False
    
    def decider_construction(self, joueur: 'Joueur') -> Optional['Propriete']:
        return None

class IAAgressive(StrategieIA):
    def __init__(self):
        super().__init__("Agressive")
    
    def decider_achat(self, joueur: 'Joueur', propriete: 'Propriete') -> bool:
        return joueur.argent >= propriete.prix

class IAConservative(StrategieIA):
    def __init__(self):
        super().__init__("Conservative")
    
    def decider_achat(self, joueur: 'Joueur', propriete: 'Propriete') -> bool:
        return joueur.argent >= propriete.prix * 2

class IAStrategique(StrategieIA):
    def __init__(self):
        super().__init__("Stratégique")
    
    def decider_achat(self, joueur: 'Joueur', propriete: 'Propriete') -> bool:
        if joueur.argent < propriete.prix * 1.5:
            return False
        
        if hasattr(propriete, 'couleur'):
            nb_possede = sum(1 for p in joueur.proprietes
                           if hasattr(p, 'couleur') and p.couleur == propriete.couleur)
            
            couleurs_map = {
                "marron": 2, "bleu clair": 3, "rose": 3, "orange": 3,
                "rouge": 3, "jaune": 3, "vert": 3, "bleu foncé": 2
            }
            
            if propriete.couleur in couleurs_map:
                total_couleur = couleurs_map[propriete.couleur]
                if nb_possede + 1 >= total_couleur:
                    return True
        
        return joueur.argent >= propriete.prix * 3
    
    def decider_construction(self, joueur: 'Joueur') -> Optional['Propriete']:
        quartiers = self._trouver_quartiers(joueur)
        
        if not quartiers:
            return None
        
        meilleure = None
        meilleur_roi = 0
        
        for proprietes in quartiers.values():
            for prop in proprietes:
                if self._peut_construire(prop, joueur):
                    loyer_actuel = prop.calculer_loyer()
                    prop.nb_maisons += 1
                    loyer_futur = prop.calculer_loyer()
                    prop.nb_maisons -= 1
                    
                    roi = (loyer_futur - loyer_actuel) / prop._get_prix_maison()
                    
                    if roi > meilleur_roi:
                        meilleur_roi = roi
                        meilleure = prop
        
        return meilleure
    
    def _trouver_quartiers(self, joueur: 'Joueur') -> Dict[str, List['Propriete']]:
        from models.case import Propriete
        from models.gare import Gare
        from models.compagnie import Compagnie
        
        quartiers = {}
        for prop in joueur.proprietes:
            if isinstance(prop, Propriete) and not isinstance(prop, (Gare, Compagnie)):
                couleur = prop.couleur
                if prop.est_monopole():
                    if couleur not in quartiers:
                        quartiers[couleur] = []
                    quartiers[couleur].append(prop)
        return quartiers
    
    def _peut_construire(self, propriete: 'Propriete', joueur: 'Joueur') -> bool:
        if propriete.nb_maisons >= 4 or propriete.a_hotel:
            return False
        if joueur.argent < propriete._get_prix_maison():
            return False
        return True