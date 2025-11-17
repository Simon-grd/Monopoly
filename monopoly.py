import random
from typing import List, Optional

class Case:
    def __init__(self, nom: str, position: int):
        self.nom = nom
        self.position = position
    
    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        pass

class Propriete(Case):
    def __init__(self, nom: str, position: int, prix: int, loyer: int, couleur: str):
        super().__init__(nom, position)
        self.prix = prix
        self.loyer_base = loyer
        self.couleur = couleur
        self.proprietaire: Optional['Joueur'] = None
        self.nb_maisons = 0
        self.a_hotel = False
    
    def calculer_loyer(self) -> int:
        return self.loyer_base
    
    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        if self.proprietaire is None:
            if joueur.argent >= self.prix:
                decision = jeu.strategie.decider_achat(joueur, self)
                if decision:
                    joueur.acheter_propriete(self)
                    print(f"✓ {joueur.nom} achète {self.nom} pour {self.prix}€")
        elif self.proprietaire != joueur:
            loyer = self.calculer_loyer()
            if loyer > 0:
                print(f"→ {joueur.nom} paie {loyer}€ à {self.proprietaire.nom} pour {self.nom}")
                joueur.payer(loyer, self.proprietaire)

class CaseSpeciale(Case):
    def __init__(self, nom: str, position: int, type_case: str):
        super().__init__(nom, position)
        self.type_case = type_case
    
    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        pass

class Joueur:
    def __init__(self, nom: str, argent_initial: int = 1500):
        self.nom = nom
        self.argent = argent_initial
        self.position = 0
        self.proprietes: List[Propriete] = []
        self.en_prison = False
        self.tours_en_prison = 0
        self.est_en_faillite = False
        self.doubles_consecutifs = 0
    
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
        else:
            montant_paye = self.argent
            self.argent = 0
            if beneficiaire:
                beneficiaire.recevoir(montant_paye)
            self.declarer_faillite(beneficiaire)
    
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
    
    def recevoir(self, montant: int):
        self.argent += montant
    
    def acheter_propriete(self, propriete: Propriete) -> bool:
        if propriete.proprietaire is not None:
            return False
        
        if self.argent < propriete.prix:
            return False
        
        self.argent -= propriete.prix
        propriete.proprietaire = self
        self.proprietes.append(propriete)
        
        return True
    
    def possede_quartier(self, couleur: str, toutes_proprietes: List[Propriete]) -> bool:
        pass

class Plateau:
    def __init__(self):
        self.cases: List[Case] = []
        self._creer_plateau()
    
    def _creer_plateau(self):
        self.cases.append(CaseSpeciale("Départ", 0, "depart"))
        self.cases.append(Propriete("Boulevard de Belleville", 1, 60, 2, "marron"))
        self.cases.append(CaseSpeciale("Caisse de Communauté", 2, "caisse"))
        self.cases.append(Propriete("Rue Lecourbe", 3, 60, 4, "marron"))
        self.cases.append(CaseSpeciale("Impôts sur le revenu", 4, "taxe"))
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
        self.cases.append(CaseSpeciale("Taxe de Luxe", 38, "taxe"))
        self.cases.append(Propriete("Rue de la Paix", 39, 400, 40, "bleu foncé"))
    
    def get_case(self, position: int) -> Case:
        return self.cases[position % len(self.cases)]

class CarteCommunaute:
    def __init__(self, description: str, action):
        self.description = description
        self.action = action

class PaquetCartes:
    def __init__(self, type_paquet: str):
        self.type_paquet = type_paquet
        self.cartes: List[CarteCommunaute] = []
        self._creer_cartes()
    
    def _creer_cartes(self):
        pass
    
    def piocher(self) -> CarteCommunaute:
        pass

class Monopoly:
    def __init__(self, noms_joueurs: List[str]):
        self.plateau = Plateau()
        self.joueurs = [Joueur(nom) for nom in noms_joueurs]
        self.joueur_actuel_index = 0
        self.cartes_chance = PaquetCartes("chance")
        self.cartes_communaute = PaquetCartes("communaute")
        self.tour_numero = 0
        self.strategie = IAAgressive()
    
    def lancer_des(self) -> tuple:
        de1 = random.randint(1, 6)
        de2 = random.randint(1, 6)
        return de1, de2
    
    def jouer_tour(self, joueur: Joueur):
        print(f"\n--- Tour de {joueur.nom} ---")
        print(f"Position: {joueur.position}, Argent: {joueur.argent}€")
        
        de1, de2 = self.lancer_des()
        total = de1 + de2
        print(f"Dés: {de1} + {de2} = {total}")
        
        passage_par_depart = joueur.deplacer(total)
        if passage_par_depart:
            print(f"✓ {joueur.nom} passe par la case Départ et reçoit 200€")
        
        case_actuelle = self.plateau.get_case(joueur.position)
        print(f"→ {joueur.nom} arrive à: {case_actuelle.nom}")
        case_actuelle.action(joueur, self)
        
        if de1 == de2:
            joueur.doubles_consecutifs = joueur.doubles_consecutifs + 1 if hasattr(joueur, 'doubles_consecutifs') else 1
            if joueur.doubles_consecutifs >= 3:
                print(f"⚠ {joueur.nom} a 3 doubles ! Aller en prison !")
                joueur.aller_en_prison()
            else:
                print(f"🎲 {joueur.nom} a un double ! Relancer !")
                self.jouer_tour(joueur)
        else:
            joueur.doubles_consecutifs = 0 if hasattr(joueur, 'doubles_consecutifs') else 0
    
    def partie_terminee(self) -> bool:
        joueurs_actifs = [j for j in self.joueurs if not j.est_en_faillite]
        return len(joueurs_actifs) <= 1
    
    def obtenir_gagnant(self) -> Optional[Joueur]:
        joueurs_actifs = [j for j in self.joueurs if not j.est_en_faillite]
        return joueurs_actifs[0] if len(joueurs_actifs) == 1 else None
    
    def jouer_partie(self, max_tours: int = 200):
        print("=== DÉBUT DE LA PARTIE ===\n")
        
        while not self.partie_terminee() and self.tour_numero < max_tours:
            joueur = self.joueurs[self.joueur_actuel_index]
            
            if not joueur.est_en_faillite:
                self.jouer_tour(joueur)
            
            self.joueur_actuel_index = (self.joueur_actuel_index + 1) % len(self.joueurs)
            
            if self.joueur_actuel_index == 0:
                self.tour_numero += 1
        
        gagnant = self.obtenir_gagnant()
        if gagnant:
            print(f"\n🎉 {gagnant.nom} a gagné avec {gagnant.argent}€ !")
        else:
            print(f"\nPartie terminée après {max_tours} tours (limite atteinte)")

class StrategieIA:
    def decider_achat(self, joueur: Joueur, propriete: Propriete) -> bool:
        return False
    
    def decider_construction(self, joueur: Joueur, proprietes_quartier: List[Propriete]) -> Optional[Propriete]:
        return None

class IAAgressive(StrategieIA):
    def decider_achat(self, joueur: Joueur, propriete: Propriete) -> bool:
        return joueur.argent >= propriete.prix

class StatistiquesPartie:
    def __init__(self):
        self.passages_par_case = {}
        self.revenus_par_propriete = {}
        self.duree_partie = 0
    
    def enregistrer_passage(self, case: Case):
        pass
    
    def afficher_statistiques(self):
        pass

def simuler_parties(nb_parties: int, nb_joueurs: int):
    print(f"Simulation de {nb_parties} parties avec {nb_joueurs} joueurs...")
    pass

if __name__ == "__main__":
    noms = ["Alain", "Béa", "Charles"]
    jeu = Monopoly(noms)
    
    print("Squelette de code chargé. Prêt pour le développement !")
