import random
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.joueur import Joueur
    from game.monopoly import Monopoly

class CarteCommunaute:
    def __init__(self, description: str, action=None):
        self.description = description
        self.action = action

    def execute(self, joueur: 'Joueur', jeu: 'Monopoly'):
        if callable(self.action):
            self.action(joueur, jeu)
        else:
            print(self.description)

class PaquetCartes:
    def __init__(self, type_paquet: str):
        self.type_paquet = type_paquet
        self.cartes: List[CarteCommunaute] = []
        self.index_courant = 0
        self._creer_cartes()
    
    def _creer_cartes(self):
        if self.type_paquet == "chance":
            self._creer_cartes_chance()
        else:
            self._creer_cartes_communaute()
    
    def _creer_cartes_chance(self):
        def avancez_depart(j, je):
            j.position = 0
            j.recevoir(200)
            print(f"✓ {j.nom} avance au Départ et reçoit 200€")

        def aller_gare_lyon(j, je):
            from models.case import Propriete
            idx = next(i for i,c in enumerate(je.plateau.cases) if isinstance(c, Propriete) and c.nom == 'Gare de Lyon')
            j.position = idx
            case = je.plateau.get_case(j.position)
            print(f"→ {j.nom} avance à {case.nom}")
            case.action(j, je)

        def aller_gare_saint_lazare(j, je):
            from models.case import Propriete
            idx = next(i for i,c in enumerate(je.plateau.cases) if isinstance(c, Propriete) and c.nom == 'Gare Saint-Lazare')
            j.position = idx
            case = je.plateau.get_case(j.position)
            print(f"→ {j.nom} avance à {case.nom}")
            case.action(j, je)

        def aller_electricite(j, je):
            from models.case import Propriete
            idx = next(i for i,c in enumerate(je.plateau.cases) if isinstance(c, Propriete) and c.nom == "Compagnie d'Électricité")
            j.position = idx
            case = je.plateau.get_case(j.position)
            print(f"→ {j.nom} avance à {case.nom}")
            if case.proprietaire and case.proprietaire != j and not case.proprietaire.en_prison:
                d1 = random.randint(1,6); d2 = random.randint(1,6)
                l = case.calculer_loyer_service(d1, d2)
                print(f"→ {j.nom} paie {l}€ à {case.proprietaire.nom} (service) (dés {d1}+{d2})")
                j.payer(l, case.proprietaire)
            else:
                case.action(j, je)

        def aller_eau(j, je):
            from models.case import Propriete
            idx = next(i for i,c in enumerate(je.plateau.cases) if isinstance(c, Propriete) and c.nom == 'Compagnie des Eaux')
            j.position = idx
            case = je.plateau.get_case(j.position)
            print(f"→ {j.nom} avance à {case.nom}")
            if case.proprietaire and case.proprietaire != j and not case.proprietaire.en_prison:
                d1 = random.randint(1,6); d2 = random.randint(1,6)
                l = case.calculer_loyer_service(d1, d2)
                print(f"→ {j.nom} paie {l}€ à {case.proprietaire.nom} (service) (dés {d1}+{d2})")
                j.payer(l, case.proprietaire)
            else:
                case.action(j, je)

        def vous_libere_prison(j, je):
            j.cartes_libertes = getattr(j, 'cartes_libertes', 0) + 1
            print(f"✓ {j.nom} reçoit une carte 'Vous êtes libéré de prison'")

        def reculez_3(j, je):
            j.deplacer(-3)
            case = je.plateau.get_case(j.position)
            print(f"→ {j.nom} recule de 3 cases et arrive à {case.nom}")
            case.action(j, je)

        def allez_en_prison(j, je):
            print(f"👮 {j.nom} va en prison !")
            j.aller_en_prison()

        def reparations(j, je):
            from models.case import Propriete
            total_houses = sum(p.nb_maisons for p in j.proprietes if isinstance(p, Propriete))
            total_hotels = sum(1 for p in j.proprietes if isinstance(p, Propriete) and p.a_hotel)
            montant = total_houses * 25 + total_hotels * 100
            print(f"💸 {j.nom} paie {montant}€ pour réparations")
            j.payer(montant, None)

        def payez_50(j, je):
            j.payer(50, None)

        def recevez_50(j, je):
            j.recevoir(50)

        def avancez_champs(j, je):
            idx = next(i for i,c in enumerate(je.plateau.cases) if c.nom == 'Avenue des Champs-Élysées')
            j.position = idx
            case = je.plateau.get_case(j.position)
            print(f"→ {j.nom} avance à {case.nom}")
            case.action(j, je)

        def gagnez_200(j, je):
            j.recevoir(200)
            print(f"✓ {j.nom} reçoit 200€")

        def payez_15(j, je):
            j.payer(15, None)

        self.cartes = [
            CarteCommunaute("Avancez au Départ (200€)", avancez_depart),
            CarteCommunaute("Aller à la Gare de Lyon", aller_gare_lyon),
            CarteCommunaute("Aller à la Gare Saint-Lazare", aller_gare_saint_lazare),
            CarteCommunaute("Aller à Électricité", aller_electricite),
            CarteCommunaute("Aller à l'Eau", aller_eau),
            CarteCommunaute("Vous êtes libéré de prison", vous_libere_prison),
            CarteCommunaute("Reculez de 3 cases", reculez_3),
            CarteCommunaute("Allez en Prison", allez_en_prison),
            CarteCommunaute("Faites des réparations: 25€ par maison, 100€ par hôtel", reparations),
            CarteCommunaute("Payez 50€ d'amende", payez_50),
            CarteCommunaute("Recevez 50€", recevez_50),
            CarteCommunaute("Avancez jusqu'aux Champs-Élysées", avancez_champs),
            CarteCommunaute("Vous avez gagné le gros lot: 200€", gagnez_200),
            CarteCommunaute("Payez 15€ pour frais scolaires", payez_15),
        ]
    
    def _creer_cartes_communaute(self):
        def avancez_depart(j, je):
            j.position = 0
            j.recevoir(200)
            print(f"✓ {j.nom} avance au Départ et reçoit 200€")

        def recevez_200(j, je):
            j.recevoir(200)
            print(f"✓ {j.nom} reçoit 200€")

        def payez_50_impots(j, je):
            j.payer(50, None)

        def vous_libere_prison(j, je):
            j.cartes_libertes = getattr(j, 'cartes_libertes', 0) + 1
            print(f"✓ {j.nom} reçoit une carte 'Vous êtes libéré de prison'")

        def erreur_banque(j, je):
            j.recevoir(100)

        def anniversaire(j, je):
            montant = 10
            for autre in je.joueurs:
                if autre != j and not autre.est_en_faillite:
                    autre.payer(montant, j)
            print(f"✓ {j.nom} reçoit 10€ de chaque joueur")

        def frais_medecin(j, je):
            j.payer(100, None)

        def allez_en_prison(j, je):
            j.aller_en_prison()

        def recevez_50(j, je):
            j.recevoir(50)

        def recevez_100(j, je):
            j.recevoir(100)

        def payez_50(j, je):
            j.payer(50, None)

        self.cartes = [
            CarteCommunaute("Avancez au Départ (200€)", avancez_depart),
            CarteCommunaute("Recevez 200€ d'une rente", recevez_200),
            CarteCommunaute("Payez 50€ d'impôts", payez_50_impots),
            CarteCommunaute("Vous êtes libéré de prison", vous_libere_prison),
            CarteCommunaute("Recevez 100€ pour erreur de la banque", erreur_banque),
            CarteCommunaute("C'est votre anniversaire: recevez 10€ de chaque joueur", anniversaire),
            CarteCommunaute("Payez 100€ pour frais de médecin", frais_medecin),
            CarteCommunaute("Allez en Prison", allez_en_prison),
            CarteCommunaute("Recevez 50€", recevez_50),
            CarteCommunaute("Recevez 100€ d'intérêts", recevez_100),
            CarteCommunaute("Payez 50€", payez_50),
        ]
    
    def piocher(self) -> CarteCommunaute:
        if self.index_courant >= len(self.cartes):
            self.index_courant = 0
        carte = self.cartes[self.index_courant]
        self.index_courant += 1
        return carte