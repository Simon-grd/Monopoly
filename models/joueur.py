from typing import List, Optional, TYPE_CHECKING
from collections import defaultdict

if TYPE_CHECKING:
    from models.case import Propriete

class Joueur:
    def __init__(self, nom: str, argent_initial: int = 1500):
        self.nom = nom
        self.argent = argent_initial
        self.position = 0
        self.proprietes: List['Propriete'] = []
        self.en_prison = False
        self.tours_en_prison = 0
        self.est_en_faillite = False
        self.doubles_consecutifs = 0
        self.cartes_liberte = 0
    
    def deplacer(self, nombre_cases: int, plateau_taille: int = 40) -> bool:
        ancienne_position = self.position
        self.position = (self.position + nombre_cases) % plateau_taille
        
        passage_par_depart = (self.position < ancienne_position) or (ancienne_position + nombre_cases >= plateau_taille)
        
        if passage_par_depart:
            self.recevoir(200)
        
        return passage_par_depart
    
    def payer(self, montant: int, beneficiaire: Optional['Joueur'] = None):
        if self.argent >= montant:
            self.argent -= montant
            if beneficiaire:
                beneficiaire.recevoir(montant)
            return

        needed = montant - self.argent
        _ = self.vendre_biens_pour(needed)

        if self.argent >= montant:
            self.argent -= montant
            if beneficiaire:
                beneficiaire.recevoir(montant)
        else:
            montant_paye = self.argent
            self.argent = 0
            if beneficiaire and montant_paye > 0:
                beneficiaire.recevoir(montant_paye)
            self.declarer_faillite(beneficiaire)

    def vendre_biens_pour(self, montant_necessaire: int) -> int:
        montant_collecte = 0
        jeu = getattr(self, 'jeu', None)

        # 1) Vendre les maisons uniformément
        from models.case import Propriete
        quartiers = defaultdict(list)
        for p in self.proprietes:
            if isinstance(p, Propriete) and p.couleur not in ["gare", "service"]:
                quartiers[p.couleur].append(p)

        for couleur, props in quartiers.items():
            if not props:
                continue
            if not props[0].est_monopole():
                continue
            while any(pr.nb_maisons > 0 for pr in props) and montant_collecte < montant_necessaire:
                prop = max(props, key=lambda x: x.nb_maisons)
                if prop.nb_maisons <= 0:
                    break
                prix_maison = prop._get_prix_maison()
                montant = prix_maison // 2
                prop.nb_maisons -= 1
                montant_collecte += montant
                self.argent += montant
                if jeu and getattr(jeu, 'houses_available', None) is not None:
                    jeu.houses_available += 1
                if montant_collecte >= montant_necessaire:
                    return montant_collecte

        # 2) Vendre les hôtels
        for prop in list(self.proprietes):
            if montant_collecte >= montant_necessaire:
                break
            if isinstance(prop, Propriete) and prop.a_hotel:
                prix_hotel = prop._get_prix_hotel()
                montant = prix_hotel // 2
                prop.a_hotel = False
                montant_collecte += montant
                self.argent += montant
                if jeu and getattr(jeu, 'houses_available', None) is not None:
                    jeu.houses_available += 4
                if jeu and getattr(jeu, 'hotels_available', None) is not None:
                    jeu.hotels_available += 1

        # 3) Hypothéquer les propriétés restantes
        for prop in list(self.proprietes):
            if montant_collecte >= montant_necessaire:
                break
            if isinstance(prop, Propriete) and not prop.hypothequee and prop.nb_maisons == 0 and not prop.a_hotel:
                montant = prop.prix // 2
                prop.hypothequee = True
                montant_collecte += montant
                self.argent += montant

        return montant_collecte
    
    def declarer_faillite(self, creancier: Optional['Joueur'] = None):
        self.est_en_faillite = True
        
        for propriete in self.proprietes:
            if creancier:
                propriete.proprietaire = creancier
                creancier.proprietes.append(propriete)
            else:
                propriete.proprietaire = None
        
        self.proprietes.clear()
        self.argent = 0
    
    def aller_en_prison(self):
        self.position = 10
        self.en_prison = True
        self.tours_en_prison = 0
        self.doubles_consecutifs = 0
    
    def sortir_prison(self, montant: int = 50):
        if not self.en_prison:
            return False
        if self.argent < montant:
            return False
        self.payer(montant, None)
        self.en_prison = False
        self.tours_en_prison = 0
        return True
    
    def sortir_de_prison(self):
        self.en_prison = False
        self.tours_en_prison = 0
    
    def peut_sortir_prison(self) -> bool:
        return self.en_prison and self.tours_en_prison >= 3
    
    def recevoir(self, montant: int):
        self.argent += montant
    
    def acheter_propriete(self, propriete: 'Propriete') -> bool:
        if propriete.proprietaire is not None:
            return False
        
        if self.argent < propriete.prix:
            return False
        
        self.argent -= propriete.prix
        propriete.proprietaire = self
        self.proprietes.append(propriete)
        
        return True
    
    def possede_quartier(self, couleur: str, toutes_proprietes: List['Propriete']) -> bool:
        pass