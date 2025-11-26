import random
from typing import List, Optional

from models.joueur import Joueur
from models.plateau import Plateau
from models.cartes import PaquetCartes
from models.case import Propriete
from models.compagnie import Compagnie

class Monopoly:
    def __init__(self, noms_joueurs: List[str]):
        self.plateau = Plateau()
        self.joueurs = [Joueur(nom) for nom in noms_joueurs]
        self.joueur_actuel_index = 0
        self.cartes_chance = PaquetCartes("chance")
        self.cartes_communaute = PaquetCartes("communaute")
        self.tour_numero = 0
        self.houses_available = 32
        self.hotels_available = 12
        self.dernier_total_des = 0
        self.plateau.jeu = self
        for j in self.joueurs:
            j.jeu = self
    
    def lancer_des(self) -> tuple:
        de1 = random.randint(1, 6)
        de2 = random.randint(1, 6)
        return de1, de2
    
    def faire_encheres(self, propriete: Propriete):
        print(f"\n🏷️ Enchères pour {propriete.nom}")
        encheres = {}
        prix_actuel = 0
        
        for joueur in self.joueurs:
            if joueur.est_en_faillite or joueur.argent == 0:
                continue
            
            while True:
                try:
                    encheres_str = input(f"{joueur.nom}, enchères (minimum {prix_actuel + 10}€, ou 0 pour passer): ")
                    encheres_int = int(encheres_str)
                    
                    if encheres_int == 0:
                        break
                    if encheres_int <= prix_actuel:
                        print(f"Enchères trop basses! Minimum: {prix_actuel + 10}€")
                        continue
                    if encheres_int > joueur.argent:
                        print(f"Tu n'as que {joueur.argent}€!")
                        continue
                    
                    encheres[joueur] = encheres_int
                    prix_actuel = encheres_int
                    break
                except ValueError:
                    print("Entre un nombre valide!")
        
        if encheres:
            gagnant = max(encheres.items(), key=lambda x: x[1])
            gagnant[0].payer(gagnant[1], None)
            gagnant[0].proprietes.append(propriete)
            propriete.proprietaire = gagnant[0]
            print(f"✓ {gagnant[0].nom} remporte les enchères pour {gagnant[1]}€!")
        else:
            print("Aucune enchère. La propriété reste libre.")
    
    def _gerer_prison(self, joueur: Joueur) -> bool:
        print(f"\n👮 {joueur.nom} est en prison!")
        joueur.tours_en_prison += 1
        print(f"Tour en prison: {joueur.tours_en_prison}/3")
        
        # Option 1: Carte libération
        if joueur.cartes_liberte > 0:
            response = input("Utiliser une carte 'Sortir de prison'? (oui/non): ").lower().strip()
            if response == "oui":
                joueur.cartes_liberte -= 1
                joueur.sortir_de_prison()
                print(f"✓ {joueur.nom} utilise une carte et sort de prison!")
                return True
        
        # Option 2: Payer 50€
        if joueur.argent >= 50:
            response = input("Payer 50€ pour sortir? (oui/non): ").lower().strip()
            if response == "oui":
                joueur.payer(50, None)
                joueur.sortir_de_prison()
                print(f"✓ {joueur.nom} paie 50€ et sort de prison")
                return True
        
        # Option 3: Tenter un double
        de1, de2 = self.lancer_des()
        self.dernier_total_des = de1 + de2
        print(f"🎲 Tentative: {de1} et {de2}")
        
        if de1 == de2:
            print("✓ Double! Sortie de prison!")
            joueur.sortir_de_prison()
            joueur.deplacer(de1 + de2)
            case = self.plateau.get_case(joueur.position)
            print(f"→ {joueur.nom} arrive à: {case.nom}")
            case.action(joueur, self)
            return False
        elif joueur.tours_en_prison >= 3:
            print("✓ Sortie forcée (50€)")
            joueur.payer(50, None)
            joueur.sortir_de_prison()
            joueur.deplacer(de1 + de2)
            case = self.plateau.get_case(joueur.position)
            print(f"→ {joueur.nom} arrive à: {case.nom}")
            case.action(joueur, self)
            return False
        else:
            print("❌ Reste en prison")
            return False
    
    def jouer_tour(self, joueur: Joueur) -> bool:
        if joueur.en_prison:
            self._gerer_prison(joueur)
            if joueur.en_prison:
                return False
        
        print(f"\n--- Tour de {joueur.nom} ---")
        print(f"Position: {joueur.position}, Argent: {joueur.argent}€")
        
        de1, de2 = self.lancer_des()
        total = de1 + de2
        self.dernier_total_des = total
        print(f"Dés: {de1} + {de2} = {total}")
        
        a_un_double = de1 == de2
        
        if joueur.tours_en_prison > 0 and a_un_double:
            print(f"🎲 {joueur.nom} a un double en prison et sort gratuitement!")
            joueur.en_prison = False
            joueur.tours_en_prison = 0
        
        passage_par_depart = joueur.deplacer(total)
        if passage_par_depart:
            print(f"✓ {joueur.nom} passe par la case Départ et reçoit 200€")
        
        case_actuelle = self.plateau.get_case(joueur.position)
        print(f"→ {joueur.nom} arrive à: {case_actuelle.nom}")
        
        case_actuelle.action(joueur, self)
        
        if a_un_double:
            joueur.doubles_consecutifs = joueur.doubles_consecutifs + 1 if hasattr(joueur, 'doubles_consecutifs') else 1
            if joueur.doubles_consecutifs >= 3:
                print(f"⚠ {joueur.nom} a 3 doubles ! Aller en prison !")
                joueur.aller_en_prison()
                joueur.tours_en_prison = 0
                return False
            else:
                print(f"🎲 {joueur.nom} a un double ! Rejeu!")
                return True
        else:
            joueur.doubles_consecutifs = 0 if hasattr(joueur, 'doubles_consecutifs') else 0
            return False
    
    def partie_terminee(self) -> bool:
        joueurs_actifs = [j for j in self.joueurs if not j.est_en_faillite]
        return len(joueurs_actifs) <= 1
    
    def obtenir_gagnant(self) -> Optional[Joueur]:
        joueurs_actifs = [j for j in self.joueurs if not j.est_en_faillite]
        return joueurs_actifs[0] if len(joueurs_actifs) == 1 else None
    
    def _afficher_resultat_final(self):
        gagnant = self.obtenir_gagnant()
        print(f"\n{'='*60}")
        if gagnant:
            print(f"🏆 {gagnant.nom} a GAGNÉ avec {gagnant.argent}€!")
            print(f"Propriétés: {len(gagnant.proprietes)}")
            for prop in gagnant.proprietes:
                print(f"  - {prop.nom}")
        else:
            print(f"Limite de {self.tour_numero} tours atteinte")
            print("\nClassement par argent:")
            classement = sorted(self.joueurs, key=lambda j: j.argent, reverse=True)
            for i, j in enumerate(classement, 1):
                statut = "FAILLITE" if j.est_en_faillite else "ACTIF"
                print(f"{i}. {j.nom}: {j.argent}€ ({len(j.proprietes)} propriétés) - {statut}")
        print('='*60)
    
    def jouer_partie(self, max_tours: int = 200, mode_interactif: bool = False):
        print("=== DÉBUT DE LA PARTIE ===\n")
        
        while not self.partie_terminee() and self.tour_numero < max_tours:
            joueur = self.joueurs[self.joueur_actuel_index]
            
            if not joueur.est_en_faillite:
                self.jouer_tour(joueur)
            
            if mode_interactif:
                input("\n[Appuyez sur Entrée...]")
            
            self.joueur_actuel_index = (self.joueur_actuel_index + 1) % len(self.joueurs)
            
            if self.joueur_actuel_index == 0:
                self.tour_numero += 1
                if self.tour_numero % 10 == 0:
                    actifs = sum(1 for j in self.joueurs if not j.est_en_faillite)
                    faillites = len(self.joueurs) - actifs
                    print(f"\n--- Tour {self.tour_numero}: {actifs} actifs, {faillites} en faillite ---")
        
        self._afficher_resultat_final()
        return self.obtenir_gagnant()