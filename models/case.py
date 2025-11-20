from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.joueur import Joueur
    from game.monopoly import Monopoly

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
    
    def peut_construire_maison(self, joueur: 'Joueur', plateau) -> bool:
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
    
    def construire_maison(self, joueur: 'Joueur', plateau) -> bool:
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

        jeu = getattr(plateau, 'jeu', None)
        if jeu and getattr(jeu, 'houses_available', None) is not None:
            if jeu.houses_available <= 0:
                print("Aucune maison disponible dans la banque.")
                return False

        joueur.payer(prix_maison, None)
        self.nb_maisons += 1

        if jeu and getattr(jeu, 'houses_available', None) is not None:
            jeu.houses_available -= 1

        return True
    
    def construire_hotel(self, joueur: 'Joueur', plateau) -> bool:
        prix_hotel = self._get_prix_hotel()
        
        if self.nb_maisons < 4:
            return False

        if joueur.argent < prix_hotel:
            return False

        jeu = getattr(plateau, 'jeu', None)
        if jeu and getattr(jeu, 'hotels_available', None) is not None:
            if jeu.hotels_available <= 0:
                print("Aucun hôtel disponible dans la banque.")
                return False

        joueur.payer(prix_hotel, None)
        if jeu and getattr(jeu, 'houses_available', None) is not None:
            jeu.houses_available += 4

        self.nb_maisons = 0
        self.a_hotel = True

        if jeu and getattr(jeu, 'hotels_available', None) is not None:
            jeu.hotels_available -= 1

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
            carte.execute(joueur, jeu)
        elif self.type_case == "caisse":
            carte = jeu.cartes_communaute.piocher()
            print(f"🎰 {joueur.nom} pioche une Caisse: {carte.description}")
            carte.execute(joueur, jeu)