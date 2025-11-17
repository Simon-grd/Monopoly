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
        self.hypothequee = False
    
    def calculer_loyer(self) -> int:
        if self.hypothequee:
            return 0
        if self.couleur == "gare":
            nb_gares = sum(1 for p in self.proprietaire.proprietes if isinstance(p, Propriete) and p.couleur == "gare")
            return 25 * (2 ** (nb_gares - 1))
        elif self.couleur == "service":
            return 0
        
        if self.nb_maisons == 0 and not self.a_hotel:
            loyer = self.loyer_base
            if self.est_monopole():
                loyer *= 2
            return loyer
        elif self.nb_maisons == 1:
            return self.loyer_base * 3
        elif self.nb_maisons == 2:
            return self.loyer_base * 9
        elif self.nb_maisons == 3:
            return self.loyer_base * 27
        elif self.nb_maisons == 4:
            return self.loyer_base * 84
        elif self.a_hotel:
            return self.loyer_base * 200
        return self.loyer_base
    
    def est_monopole(self) -> bool:
        if not self.proprietaire or self.couleur in ["gare", "service"]:
            return False
        couleurs_map = {
            "marron": ["Boulevard de Belleville", "Rue Lecourbe"],
            "bleu clair": ["Rue de Vaugirard", "Rue de Courcelles", "Avenue de la République"],
            "rose": ["Rue de Paradis", "Avenue de Neuilly", "Rue de la Fayette"],
            "orange": ["Place de la Bourse", "Faubourg Saint-Honoré", "Rue La Fayette"],
            "rouge": ["Avenue Matignon", "Boulevard Malesherbes", "Avenue Henri-Martin"],
            "jaune": ["Avenue de Breteuil", "Avenue Foch", "Boulevard des Capucines"],
            "vert": ["Rue de la Paix", "Avenue des Champs-Élysées"],
            "bleu foncé": ["Boulevard de la Villette", "Place Pigalle"]
        }
        
        if self.couleur not in couleurs_map:
            return False
        
        proprietes_couleur = [p for p in self.proprietaire.proprietes 
                             if isinstance(p, Propriete) and p.couleur == self.couleur]
        return len(proprietes_couleur) == len(couleurs_map[self.couleur])
    
    def peut_construire_maison(self, joueur: 'Joueur', plateau: 'Plateau') -> bool:
        if self.proprietaire != joueur:
            return False
        if self.nb_maisons >= 4:
            return False
        if self.couleur not in ["marron", "bleu clair", "rose", "orange", "rouge", "jaune", "vert", "bleu foncé"]:
            return False
        
        couleur = self.couleur
        proprietes_couleur = [c for c in plateau.cases if isinstance(c, Propriete) and c.couleur == couleur]
        
        for prop in proprietes_couleur:
            if prop.proprietaire != joueur:
                return False
        
        return True
    
    def construire_maison(self, joueur: 'Joueur', plateau: 'Plateau') -> bool:
        prix_maison = self._get_prix_maison()
        
        if not self.peut_construire_maison(joueur, plateau):
            return False
        
        couleur = self.couleur
        proprietes_couleur = [c for c in plateau.cases if isinstance(c, Propriete) and c.couleur == couleur]
        
        max_maisons = max(p.nb_maisons for p in proprietes_couleur) if proprietes_couleur else 0
        if self.nb_maisons < max_maisons:
            print(f"Construction uniforme requise! Toutes les propriétés {couleur} doivent avoir le même nombre de maisons.")
            return False
        
        if joueur.argent < prix_maison:
            return False
        
        joueur.payer(prix_maison, None)
        self.nb_maisons += 1
        return True
    
    def construire_hotel(self, joueur: 'Joueur', plateau: 'Plateau') -> bool:
        prix_hotel = self._get_prix_hotel()
        
        if self.nb_maisons < 4:
            return False
        
        if joueur.argent < prix_hotel:
            return False
        
        joueur.payer(prix_hotel, None)
        self.nb_maisons = 0
        self.a_hotel = True
        return True
    
    def _get_prix_maison(self) -> int:
        prix_table = {
            "marron": 50, "bleu clair": 100, "rose": 150, "orange": 200,
            "rouge": 200, "jaune": 300, "vert": 300, "bleu foncé": 400
        }
        return prix_table.get(self.couleur, 50)
    
    def _get_prix_hotel(self) -> int:
        prix_table = {
            "marron": 200, "bleu clair": 200, "rose": 300, "orange": 400,
            "rouge": 400, "jaune": 600, "vert": 600, "bleu foncé": 800
        }
        return prix_table.get(self.couleur, 200)
    
    def hypothequer(self, joueur: 'Joueur') -> bool:
        if self.proprietaire != joueur:
            print("Tu ne peux pas hypothéquer une propriété qui ne t'appartient pas!")
            return False
        if self.hypothequee:
            print(f"{self.nom} est déjà hypothéquée!")
            return False
        if self.nb_maisons > 0 or self.a_hotel:
            print("Tu dois d'abord enlever toutes les maisons et hôtels!")
            return False
        
        montant = self.prix // 2
        joueur.recevoir(montant)
        self.hypothequee = True
        print(f"✓ {self.nom} est hypothéquée pour {montant}€")
        return True
    
    def lever_hypotheque(self, joueur: 'Joueur') -> bool:
        if self.proprietaire != joueur:
            print("Tu ne peux pas lever l'hypothèque d'une propriété qui ne t'appartient pas!")
            return False
        if not self.hypothequee:
            print(f"{self.nom} n'est pas hypothéquée!")
            return False
        
        montant = int(self.prix // 2 * 1.1)
        if joueur.argent < montant:
            print(f"Tu n'as pas assez d'argent pour lever l'hypothèque ({montant}€)!")
            return False
        
        joueur.payer(montant, None)
        self.hypothequee = False
        print(f"✓ Hypothèque sur {self.nom} levée ({montant}€)")
        return True
    
    def vendre_a_joueur(self, acheteur: 'Joueur', prix: int) -> bool:
        if acheteur.argent < prix:
            print(f"{acheteur.nom} n'a pas assez d'argent!")
            return False
        acheteur.payer(prix, self.proprietaire)
        acheteur.proprietes.append(self)
        self.proprietaire.proprietes.remove(self)
        self.proprietaire = acheteur
        print(f"✓ {acheteur.nom} a acheté {self.nom} à {self.proprietaire.nom} pour {prix}€")
        return True
    
    def calculer_loyer_service(self, de1: int, de2: int) -> int:
        nb_services = sum(1 for p in self.proprietaire.proprietes if isinstance(p, Propriete) and p.couleur == "service")
        total_des = de1 + de2
        if nb_services == 1:
            return total_des * 4
        elif nb_services == 2:
            return total_des * 10
        return 0
    
    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        if self.proprietaire is None:
            if joueur.argent >= self.prix:
                response = input(f"Veux-tu acheter {self.nom} pour {self.prix}€? (oui/non): ").lower().strip()
                if response == "oui":
                    joueur.acheter_propriete(self)
                    print(f"✓ {joueur.nom} achète {self.nom} pour {self.prix}€")
                else:
                    print(f"✗ {joueur.nom} refuse d'acheter {self.nom}")
            else:
                print(f"✗ {joueur.nom} n'a pas assez d'argent pour {self.nom} ({self.prix}€)")
        elif self.proprietaire != joueur:
            if self.proprietaire.en_prison:
                print(f"→ {self.proprietaire.nom} est en prison et ne touche pas le loyer")
            else:
                loyer = self.calculer_loyer()
                if loyer > 0:
                    print(f"→ {joueur.nom} paie {loyer}€ à {self.proprietaire.nom} pour {self.nom}")
                    joueur.payer(loyer, self.proprietaire)

class CaseSpeciale(Case):
    def __init__(self, nom: str, position: int, type_case: str):
        super().__init__(nom, position)
        self.type_case = type_case
    
    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        if self.type_case == "impot":
            montant = 200
            print(f"💸 {joueur.nom} paie l'impôt: {montant}€")
            joueur.payer(montant, None)
        elif self.type_case == "taxe_luxe":
            montant = 100
            print(f"💸 {joueur.nom} paie la taxe de luxe: {montant}€")
            joueur.payer(montant, None)
        elif self.type_case == "prison":
            if joueur.tours_en_prison == 0:
                print(f"👮 {joueur.nom} est en visite à la prison")
        elif self.type_case == "allez_prison":
            print(f"👮 {joueur.nom} va en prison!")
            joueur.aller_en_prison()
        elif self.type_case == "depart":
            print(f"🏁 {joueur.nom} arrive à la case Départ")
        elif self.type_case == "parc":
            print(f"🌳 {joueur.nom} se repose au parc gratuit")
        elif self.type_case == "chance":
            carte = jeu.cartes_chance.piocher()
            print(f"🎰 {joueur.nom} pioche une Chance: {carte.description}")
        elif self.type_case == "caisse":
            carte = jeu.cartes_communaute.piocher()
            print(f"🎰 {joueur.nom} pioche une Caisse: {carte.description}")


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
    
    def sortir_prison(self, montant: int = 50):
        if not self.en_prison:
            return False
        if self.argent < montant:
            return False
        self.payer(montant, None)
        self.en_prison = False
        return True
    
    def peut_sortir_prison(self) -> bool:
        return self.en_prison and self.tours_en_prison >= 3
    
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

class CarteCommunaute:
    def __init__(self, description: str):
        self.description = description

class PaquetCartes:
    def __init__(self, type_paquet: str):
        self.type_paquet = type_paquet
        self.cartes: List[CarteCommunaute] = []
        self.index_courant = 0
        self._creer_cartes()
    
    def _creer_cartes(self):
        if self.type_paquet == "chance":
            self.cartes = [
                CarteCommunaute("Avancez au Départ (200€)"),
                CarteCommunaute("Aller à la Gare de Lyon"),
                CarteCommunaute("Aller à la Gare Saint-Lazare"),
                CarteCommunaute("Aller à Électricité"),
                CarteCommunaute("Aller à l'Eau"),
                CarteCommunaute("Vous êtes libéré de prison"),
                CarteCommunaute("Reculez de 3 cases"),
                CarteCommunaute("Allez en Prison"),
                CarteCommunaute("Faites des réparations: 25€ par maison, 100€ par hôtel"),
                CarteCommunaute("Payez 50€ d'amende"),
                CarteCommunaute("Recevez 50€"),
                CarteCommunaute("Avancez jusqu'aux Champs-Élysées"),
                CarteCommunaute("Vous avez gagné le gros lot: 200€"),
                CarteCommunaute("Payez 15€ pour frais scolaires"),
            ]
        else:
            self.cartes = [
                CarteCommunaute("Avancez au Départ (200€)"),
                CarteCommunaute("Recevez 200€ d'une rente"),
                CarteCommunaute("Payez 50€ d'impôts"),
                CarteCommunaute("Vous êtes libéré de prison"),
                CarteCommunaute("Recevez 100€ pour erreur de la banque"),
                CarteCommunaute("C'est votre anniversaire: recevez 10€ de chaque joueur"),
                CarteCommunaute("Payez 100€ pour frais de médecin"),
                CarteCommunaute("Allez en Prison"),
                CarteCommunaute("Vendez vos propriétés au-dessus de leur valeur"),
                CarteCommunaute("Recevez 50€"),
                CarteCommunaute("Recevez 100€ d'intérêts"),
                CarteCommunaute("Payez 50€"),
            ]
    
    def piocher(self) -> CarteCommunaute:
        if self.index_courant >= len(self.cartes):
            self.index_courant = 0
        carte = self.cartes[self.index_courant]
        self.index_courant += 1
        return carte

class Monopoly:
    def __init__(self, noms_joueurs: List[str]):
        self.plateau = Plateau()
        self.joueurs = [Joueur(nom) for nom in noms_joueurs]
        self.joueur_actuel_index = 0
        self.cartes_chance = PaquetCartes("chance")
        self.cartes_communaute = PaquetCartes("communaute")
        self.tour_numero = 0
    
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
    
    
    def jouer_tour(self, joueur: Joueur) -> bool:
        if joueur.en_prison:
            print(f"\n👮 {joueur.nom} est en prison!")
            joueur.tours_en_prison += 1
            print(f"Tour en prison: {joueur.tours_en_prison}/3")
            
            if joueur.tours_en_prison < 3:
                response = input("Veux-tu payer 50€ pour sortir? (oui/non): ").lower().strip()
                if response == "oui":
                    if joueur.sortir_prison():
                        print(f"✓ {joueur.nom} sort de prison en payant 50€")
                        joueur.en_prison = False
                        joueur.tours_en_prison = 0
                    else:
                        print("Pas assez d'argent pour sortir")
                        print(f"{joueur.nom} reste en prison")
                        return False
                else:
                    print(f"{joueur.nom} reste en prison")
                    return False
            else:
                print(f"✓ {joueur.nom} sort de prison après 3 tours (gratuit)")
                joueur.en_prison = False
                joueur.tours_en_prison = 0
        
        print(f"\n--- Tour de {joueur.nom} ---")
        print(f"Position: {joueur.position}, Argent: {joueur.argent}€")
        
        de1, de2 = self.lancer_des()
        total = de1 + de2
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
        if isinstance(case_actuelle, Propriete) and case_actuelle.couleur == "service":
            if case_actuelle.proprietaire is None:
                case_actuelle.action(joueur, self)
            elif case_actuelle.proprietaire != joueur:
                if case_actuelle.proprietaire.en_prison:
                    print(f"→ {case_actuelle.proprietaire.nom} est en prison et ne touche pas le loyer")
                else:
                    loyer_service = case_actuelle.calculer_loyer_service(de1, de2)
                    if loyer_service > 0:
                        print(f"→ {joueur.nom} paie {loyer_service}€ à {case_actuelle.proprietaire.nom} pour {case_actuelle.nom} (service)")
                        joueur.payer(loyer_service, case_actuelle.proprietaire)
        else:
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

class JeuTerminal:
    def __init__(self):
        self.jeu = None
    
    def afficher_bienvenue(self):
        print("\n" + "="*60)
        print(" "*15 + "🎲 MONOPOLY FRANÇAIS 🎲")
        print("="*60)
        print("\nBienvenue au Monopoly !")
        print("\nCommandes disponibles:")
        print("  - 'jouer' : Lancer les dés et se déplacer")
        print("  - 'construire' : Construire une maison/hôtel")
        print("  - 'infos' : Voir ses infos (argent, position, propriétés)")
        print("  - 'plateau' : Voir l'état du plateau")
        print("  - 'joueurs' : Voir les infos de tous les joueurs")
        print("  - 'quitter' : Arrêter la partie\n")
    
    def construire_maison(self, joueur):
        proprietes_constructibles = []
        for prop in joueur.proprietes:
            if isinstance(prop, Propriete) and prop.peut_construire_maison(joueur, self.jeu.plateau):
                if not prop.a_hotel:
                    proprietes_constructibles.append(prop)
        
        if not proprietes_constructibles:
            print("Aucune propriété constructible!")
            return
        
        print("\nPropriétés constructibles:")
        for i, prop in enumerate(proprietes_constructibles):
            prix_maison = prop._get_prix_maison()
            prix_hotel = prop._get_prix_hotel()
            status = ""
            if prop.nb_maisons > 0:
                status = f" ({prop.nb_maisons} maisons, {prix_hotel}€ pour hôtel)"
            else:
                status = f" (maison: {prix_maison}€)"
            print(f"  {i+1}. {prop.nom}{status}")
        
        try:
            choix = int(input("Choix (numéro ou 0 pour annuler): "))
            if choix == 0:
                return
            prop = proprietes_constructibles[choix - 1]
            
            if prop.nb_maisons < 4:
                prix_maison = prop._get_prix_maison()
                response = input(f"Construire une maison ({prix_maison}€)? (oui/non): ").lower().strip()
                if response == "oui":
                    if prop.construire_maison(joueur, self.jeu.plateau):
                        print(f"✓ Maison construite sur {prop.nom}")
                    else:
                        print("Impossible de construire")
            else:
                prix_hotel = prop._get_prix_hotel()
                response = input(f"Construire un hôtel ({prix_hotel}€)? (oui/non): ").lower().strip()
                if response == "oui":
                    if prop.construire_hotel(joueur, self.jeu.plateau):
                        print(f"✓ Hôtel construit sur {prop.nom}")
                    else:
                        print("Impossible de construire")
        except (ValueError, IndexError):
            print("Choix invalide")
    
    def hypothequer_propriete(self, joueur):
        proprietes_hypothecables = []
        for prop in joueur.proprietes:
            if isinstance(prop, Propriete) and not prop.hypothequee and prop.nb_maisons == 0 and not prop.a_hotel:
                proprietes_hypothecables.append(prop)
        
        if not proprietes_hypothecables:
            print("Aucune propriété à hypothéquer!")
            return
        
        print("\nPropriétés à hypothéquer:")
        for i, prop in enumerate(proprietes_hypothecables):
            montant = prop.prix // 2
            print(f"  {i+1}. {prop.nom} ({montant}€ reçus)")
        
        try:
            choix = int(input("Choix (numéro ou 0 pour annuler): "))
            if choix == 0:
                return
            prop = proprietes_hypothecables[choix - 1]
            prop.hypothequer(joueur)
        except (ValueError, IndexError):
            print("Choix invalide")

    
    def afficher_plateau(self):
        print("\n" + "-"*80)
        print("PLATEAU")
        print("-"*80)
        for i, case in enumerate(self.jeu.plateau.cases):
            proprietaire = ""
            batiments = ""
            if isinstance(case, Propriete):
                if case.proprietaire:
                    proprietaire = f" [{case.proprietaire.nom}]"
                    if case.a_hotel:
                        batiments = " 🏨"
                    elif case.nb_maisons > 0:
                        batiments = " " + "🏠" * case.nb_maisons
                else:
                    proprietaire = f" [{case.prix}€]"
            print(f"{i:2d}: {case.nom:<35}{proprietaire:<25}{batiments}")

    
    def afficher_infos_joueur(self, joueur):
        print(f"\n--- Infos de {joueur.nom} ---")
        print(f"Argent: {joueur.argent}€")
        pos_case = self.jeu.plateau.get_case(joueur.position)
        print(f"Position: {joueur.position} ({pos_case.nom})")
        
        if joueur.en_prison:
            print(f"Status: 👮 EN PRISON (tour {joueur.tours_en_prison}/3)")
        else:
            print(f"Status: LIBRE")
        
        print(f"Propriétés: {len(joueur.proprietes)}")
        if joueur.proprietes:
            for prop in joueur.proprietes:
                batiments = ""
                if isinstance(prop, Propriete):
                    if prop.a_hotel:
                        batiments = " 🏨"
                    elif prop.nb_maisons > 0:
                        batiments = " " + "🏠" * prop.nb_maisons
                    loyer = prop.calculer_loyer()
                    print(f"  - {prop.nom} ({prop.prix}€, loyer: {loyer}€){batiments}")
        
        print(f"En faillite: {'OUI' if joueur.est_en_faillite else 'NON'}")

    
    def afficher_tous_les_joueurs(self):
        print("\n" + "-"*60)
        print("TOUS LES JOUEURS")
        print("-"*60)
        for joueur in self.jeu.joueurs:
            statut = "EN FAILLITE" if joueur.est_en_faillite else "ACTIF"
            print(f"{joueur.nom}: {joueur.argent}€ | {len(joueur.proprietes)} propriétés | {statut}")
    
    def jouer_partie(self):
        print("\nCombien de joueurs? (2-4)")
        while True:
            try:
                nb_joueurs = int(input("Nombre: "))
                if 2 <= nb_joueurs <= 4:
                    break
                print("Veuillez entrer un nombre entre 2 et 4")
            except ValueError:
                print("Veuillez entrer un nombre valide")
        
        noms = []
        for i in range(nb_joueurs):
            nom = input(f"Nom du joueur {i+1}: ").strip()
            if not nom:
                nom = f"Joueur {i+1}"
            noms.append(nom)
        
        self.jeu = Monopoly(noms)
        self.afficher_bienvenue()
        
        tour = 0
        while not self.jeu.partie_terminee() and tour < 100:
            joueur_actuel = self.jeu.joueurs[self.jeu.joueur_actuel_index]
            
            if joueur_actuel.est_en_faillite:
                self.jeu.joueur_actuel_index = (self.jeu.joueur_actuel_index + 1) % len(self.jeu.joueurs)
                continue
            
            rejeu = True
            while rejeu:
                print(f"\n{'='*60}")
                print(f"Au tour de {joueur_actuel.nom}")
                print(f"Argent: {joueur_actuel.argent}€ | Position: {joueur_actuel.position}")
                print('='*60)
                
                commande = ""
                while commande != "jouer":
                    commande = input("\nQue veux-tu faire? (jouer/construire/hypothequer/infos/plateau/joueurs/quitter): ").lower().strip()
                    
                    if commande == "quitter":
                        print("\nPartie annulée!")
                        return
                    elif commande == "construire":
                        self.construire_maison(joueur_actuel)
                    elif commande == "hypothequer":
                        self.hypothequer_propriete(joueur_actuel)
                    elif commande == "infos":
                        self.afficher_infos_joueur(joueur_actuel)
                    elif commande == "plateau":
                        self.afficher_plateau()
                    elif commande == "joueurs":
                        self.afficher_tous_les_joueurs()
                    elif commande == "jouer":
                        break
                    else:
                        print("Commande inconnue!")
                
                print("\n🎲 Lancement des dés...")
                input("Appuie sur Entrée...")
                
                rejeu = self.jeu.jouer_tour(joueur_actuel)
                
                print("\n" + "-"*60)
                self.afficher_infos_joueur(joueur_actuel)
                print("-"*60)
            
            self.jeu.joueur_actuel_index = (self.jeu.joueur_actuel_index + 1) % len(self.jeu.joueurs)
            tour += 1
        
        gagnant = self.jeu.obtenir_gagnant()
        print(f"\n{'='*60}")
        if gagnant:
            print(f"🏆 {gagnant.nom} a GAGNÉ avec {gagnant.argent}€! 🏆")
        else:
            print(f"Partie terminée après {tour} tours")
        print('='*60)

if __name__ == "__main__":
    jeu_terminal = JeuTerminal()
    jeu_terminal.jouer_partie()
