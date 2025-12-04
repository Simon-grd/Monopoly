import random
import time
from typing import List, Optional
from ui.colors import Colors, Icons, colorize, bold

from models.joueur import Joueur
from models.plateau import Plateau
from models.cartes import PaquetCartes
from models.case import Propriete
from models.compagnie import Compagnie
from models.ia import StrategieIA
from models.statistiques import StatistiquesPartie

class Monopoly:
    def __init__(self, joueurs_config: List[tuple]):
        self.plateau = Plateau()
        self.joueurs = [Joueur(nom, strategie=strat) for nom, strat in joueurs_config]
        self.joueur_actuel_index = 0
        self.cartes_chance = PaquetCartes("chance")
        self.cartes_communaute = PaquetCartes("communaute")
        self.tour_numero = 0
        self.houses_available = 32
        self.hotels_available = 12
        self.dernier_total_des = 0
        self.stats = StatistiquesPartie()
        self.plateau.jeu = self
        for j in self.joueurs:
            j.jeu = self
    
    def lancer_des(self) -> tuple:
        de1 = random.randint(1, 6)
        de2 = random.randint(1, 6)
        return de1, de2
    
    def faire_encheres(self, propriete: Propriete):
        print(f"\nENCHERES pour {propriete.nom}")
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
                        print(f"Encheres trop basses! Minimum: {prix_actuel + 10}€")
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
            print(f"OK {gagnant[0].nom} remporte les encheres pour {gagnant[1]}€!")
        else:
            print("Aucune enchere. La propriete reste libre.")
    
    def _gerer_prison(self, joueur: Joueur):
        print(f"\n{Icons.PRISON} {colorize(f'{joueur.nom} est en prison!', Colors.RED)}")
        print(f"{colorize(f'Tour en prison: {joueur.tours_en_prison + 1}/3', Colors.YELLOW)}")
        
        if joueur.est_ia:
            if joueur.cartes_liberte > 0:
                joueur.cartes_liberte -= 1
                joueur.sortir_de_prison()
                print(f"{Icons.CARD} {colorize(f'{joueur.nom} utilise une carte et sort de prison!', Colors.GREEN)}")
                return
            elif joueur.tours_en_prison < 2 and joueur.argent >= 50:
                joueur.payer(50, None)
                joueur.sortir_de_prison()
                print(f"{Icons.MONEY} {colorize(f'{joueur.nom} paie 50€ et sort de prison', Colors.GREEN)}")
                return
        else:
            if joueur.cartes_liberte > 0:
                response = input(f"{Icons.CARD} Utiliser une carte 'Sortir de prison'? (oui/non): ").lower().strip()
                if response == "oui":
                    joueur.cartes_liberte -= 1
                    joueur.sortir_de_prison()
                    print(f"{Icons.CHECK} {colorize(f'{joueur.nom} utilise une carte et sort de prison!', Colors.GREEN)}")
                    return
            
            if joueur.tours_en_prison < 2 and joueur.argent >= 50:
                response = input(f"{Icons.MONEY} Payer 50€ pour sortir? (oui/non): ").lower().strip()
                if response == "oui":
                    joueur.payer(50, None)
                    joueur.sortir_de_prison()
                    print(f"{Icons.CHECK} {colorize(f'{joueur.nom} paie 50€ et sort de prison', Colors.GREEN)}")
                    return
        
        de1, de2 = self.lancer_des()
        self.dernier_total_des = de1 + de2
        print(f"{Icons.DICE} {colorize('Tentative:', Colors.WHITE)} {colorize(str(de1), Colors.YELLOW)} et {colorize(str(de2), Colors.YELLOW)}")
        
        if de1 == de2:
            print(f"{Icons.CHECK} {colorize('Double! Sortie de prison!', Colors.GREEN)}")
            joueur.sortir_de_prison()
            joueur.deplacer(de1 + de2)
            case = self.plateau.get_case(joueur.position)
            print(f"{Icons.ARROW} {joueur.nom} arrive a: {colorize(case.nom, Colors.WHITE)}")
            self.stats.enregistrer_passage(case)
            case.action(joueur, self)
        elif joueur.tours_en_prison >= 2:
            print(f"{Icons.CHECK} {colorize('Sortie forcee (50€)', Colors.GREEN)}")
            joueur.payer(50, None)
            joueur.sortir_de_prison()
            joueur.deplacer(de1 + de2)
            case = self.plateau.get_case(joueur.position)
            print(f"{Icons.ARROW} {joueur.nom} arrive a: {colorize(case.nom, Colors.WHITE)}")
            self.stats.enregistrer_passage(case)
            case.action(joueur, self)
        else:
            print(f"{Icons.CROSS} {colorize('Reste en prison', Colors.RED)}")
            joueur.tours_en_prison += 1
    
    def _afficher_infos_joueur(self, joueur: Joueur):
        case = self.plateau.get_case(joueur.position)
        color = Colors.CYAN if joueur.est_ia else Colors.GREEN
        icon = Icons.ROBOT if joueur.est_ia else Icons.PLAYER
        print(f"  {icon} {colorize(joueur.nom, color)}: {Icons.MONEY} {colorize(f'{joueur.argent}€', Colors.YELLOW)} | {Icons.ARROW} {colorize(case.nom, Colors.WHITE)} | {Icons.BUILDING} {colorize(str(len(joueur.proprietes)), Colors.MAGENTA)}")
    
    def _menu_actions(self, joueur: Joueur) -> bool:
        while True:
            print(f"\n{colorize('┌─ ACTIONS ────────────────────────────────────────────────────┐', Colors.YELLOW)}")
            print(f"  {Icons.DICE} 1. Lancer les dés")
            print(f"  {Icons.BANK} 2. Hypothéquer une propriété")
            print(f"  {Icons.MONEY} 3. Lever une hypothèque")
            print(f"  {Icons.BUILDING} 4. Construire des maisons/hôtels")
            print(f"  {Icons.HOUSE} 5. Vendre des maisons/hôtels")
            print(f"  {Icons.CROSS} 6. Déclarer faillite")
            print(f"  {Icons.INFO} 7. Voir mes propriétés")
            print(f"{colorize('└──────────────────────────────────────────────────────────────┘', Colors.YELLOW)}")
            
            choix = input(f"{colorize('Choix', Colors.WHITE)}: ").strip()
            
            if choix == "1":
                return True
            elif choix == "2":
                self._hypothequer_propriete(joueur)
            elif choix == "3":
                self._lever_hypotheque(joueur)
            elif choix == "4":
                self._construire(joueur)
            elif choix == "5":
                self._vendre_constructions(joueur)
            elif choix == "6":
                joueur.declarer_faillite(None)
                print(f"FAILLITE {joueur.nom} a déclaré faillite")
                return False
            elif choix == "7":
                self._afficher_proprietes(joueur)
            else:
                print("Choix invalide!")
    
    def _afficher_proprietes(self, joueur: Joueur):
        if not joueur.proprietes:
            print(f"{colorize(f'{Icons.INFO} Tu n\'as aucune propriété', Colors.YELLOW)}")
            return
        print(f"\n{colorize(f'{Icons.BUILDING} Propriétés de {joueur.nom}', Colors.MAGENTA)}:")
        for i, prop in enumerate(joueur.proprietes, 1):
            info = f"  {i}. {prop.nom} ({Icons.MONEY}{prop.prix}€)"
            if hasattr(prop, 'hypothequee'):
                if prop.hypothequee:
                    info += f" {colorize('[HYPOTHÉQUÉE]', Colors.RED)}"
                elif prop.a_hotel:
                    info += f" {Icons.HOTEL}"
                elif prop.nb_maisons > 0:
                    info += f" {Icons.HOUSE}×{prop.nb_maisons}"
            print(info)
    
    def _hypothequer_propriete(self, joueur: Joueur):
        props_hypothecables = [p for p in joueur.proprietes if hasattr(p, 'hypothequee') and not p.hypothequee and p.nb_maisons == 0 and not p.a_hotel]
        if not props_hypothecables:
            print("Aucune propriété hypothécable (retire d'abord les constructions)")
            return
        print("\nPropriétés hypothécables:")
        for i, prop in enumerate(props_hypothecables, 1):
            print(f"{i}. {prop.nom} ({prop.prix // 2}€)")
        choix = input("Numéro (0 pour annuler): ").strip()
        if choix.isdigit() and 1 <= int(choix) <= len(props_hypothecables):
            props_hypothecables[int(choix) - 1].hypothequer(joueur)
    
    def _lever_hypotheque(self, joueur: Joueur):
        props_hypothequees = [p for p in joueur.proprietes if hasattr(p, 'hypothequee') and p.hypothequee]
        if not props_hypothequees:
            print("Aucune propriété hypothéquée")
            return
        print("\nPropriétés hypothéquées:")
        for i, prop in enumerate(props_hypothequees, 1):
            montant = int(prop.prix // 2 * 1.1)
            print(f"{i}. {prop.nom} ({montant}€)")
        choix = input("Numéro (0 pour annuler): ").strip()
        if choix.isdigit() and 1 <= int(choix) <= len(props_hypothequees):
            props_hypothequees[int(choix) - 1].lever_hypotheque(joueur)
    
    def _construire(self, joueur: Joueur):
        props_constructibles = [p for p in joueur.proprietes if hasattr(p, 'peut_construire_maison') and p.peut_construire_maison(joueur, self.plateau) and not p.a_hotel]
        if not props_constructibles:
            print("Aucune propriété constructible (monopole requis)")
            return
        print("\nPropriétés constructibles:")
        for i, prop in enumerate(props_constructibles, 1):
            prix = prop._get_prix_maison() if prop.nb_maisons < 4 else prop._get_prix_hotel()
            type_const = "maison" if prop.nb_maisons < 4 else "hôtel"
            print(f"{i}. {prop.nom} [{prop.nb_maisons} maison(s)] - {type_const}: {prix}€")
        choix = input("Numéro (0 pour annuler): ").strip()
        if choix.isdigit() and 1 <= int(choix) <= len(props_constructibles):
            prop = props_constructibles[int(choix) - 1]
            if prop.nb_maisons < 4:
                if prop.construire_maison(joueur, self.plateau):
                    print(f"✓ Maison construite sur {prop.nom}")
            else:
                if prop.construire_hotel(joueur, self.plateau):
                    print(f"✓ Hôtel construit sur {prop.nom}")
    
    def _vendre_constructions(self, joueur: Joueur):
        props_avec_constructions = [p for p in joueur.proprietes if hasattr(p, 'nb_maisons') and (p.nb_maisons > 0 or p.a_hotel)]
        if not props_avec_constructions:
            print("Aucune construction à vendre")
            return
        print("\nPropriétés avec constructions:")
        for i, prop in enumerate(props_avec_constructions, 1):
            if prop.a_hotel:
                prix = prop._get_prix_hotel() // 2
                print(f"{i}. {prop.nom} [HÔTEL] - vente: {prix}€")
            else:
                prix = prop._get_prix_maison() // 2
                print(f"{i}. {prop.nom} [{prop.nb_maisons} maison(s)] - vente: {prix}€")
        choix = input("Numéro (0 pour annuler): ").strip()
        if choix.isdigit() and 1 <= int(choix) <= len(props_avec_constructions):
            prop = props_avec_constructions[int(choix) - 1]
            if prop.a_hotel:
                prix = prop._get_prix_hotel() // 2
                prop.a_hotel = False
                prop.nb_maisons = 4
                joueur.recevoir(prix)
                self.hotels_available += 1
                self.houses_available -= 4
                print(f"✓ Hôtel vendu sur {prop.nom} (+{prix}€)")
            elif prop.nb_maisons > 0:
                prix = prop._get_prix_maison() // 2
                prop.nb_maisons -= 1
                joueur.recevoir(prix)
                self.houses_available += 1
                print(f"✓ Maison vendue sur {prop.nom} (+{prix}€)")
    
    def jouer_tour(self, joueur: Joueur):
        color = Colors.CYAN if joueur.est_ia else Colors.GREEN
        print(f"\n{colorize('╔═══════════════════════════════════════════════════════════╗', color)}")
        print(f"{colorize(f'║ AVANT - Tour de {joueur.nom:40} ║', color)}")
        print(f"{colorize('╠═══════════════════════════════════════════════════════════╣', color)}")
        self._afficher_infos_joueur(joueur)
        print(f"{colorize('╚═══════════════════════════════════════════════════════════╝', color)}")
        
        if not joueur.est_ia:
            if not self._menu_actions(joueur):
                color = Colors.CYAN if joueur.est_ia else Colors.GREEN
                print(f"\n{colorize('└─ APRES ─────────────────────────────────────────────────────┘', color)}")
                self._afficher_infos_joueur(joueur)
                return
        
        if joueur.en_prison:
            self._gerer_prison(joueur)
            color = Colors.CYAN if joueur.est_ia else Colors.GREEN
            print(f"\n{colorize('└─ APRES ─────────────────────────────────────────────────────┘', color)}")
            self._afficher_infos_joueur(joueur)
            return
        
        de1, de2 = self.lancer_des()
        total = de1 + de2
        self.dernier_total_des = total
        print(f"\n{Icons.DICE} {colorize('Dés:', Colors.WHITE)} {colorize(str(de1), Colors.YELLOW)} + {colorize(str(de2), Colors.YELLOW)} = {colorize(str(total), Colors.GREEN)}")
        
        a_un_double = de1 == de2
        
        if a_un_double:
            joueur.doubles_consecutifs += 1
            if joueur.doubles_consecutifs >= 3:
                print(f"{Icons.WARNING} {colorize(f'{joueur.nom} a 3 doubles consecutifs ! Va en prison !', Colors.RED)}")
                joueur.aller_en_prison()
                color = Colors.CYAN if joueur.est_ia else Colors.GREEN
                print(f"\n{colorize('└─ APRES ─────────────────────────────────────────────────────┘', color)}")
                self._afficher_infos_joueur(joueur)
                return
        else:
            joueur.doubles_consecutifs = 0
        
        passage_par_depart = joueur.deplacer(total)
        if passage_par_depart:
            print(f"{Icons.GO} {colorize(f'{joueur.nom} passe par la case Depart et recoit 200€', Colors.GREEN)}")
        
        case_actuelle = self.plateau.get_case(joueur.position)
        print(f"{Icons.ARROW} {joueur.nom} arrive a: {colorize(case_actuelle.nom, Colors.WHITE)}")

        self.stats.enregistrer_passage(case_actuelle)
        
        case_actuelle.action(joueur, self)
        
        if a_un_double and not joueur.en_prison:
            print(f"{Icons.DICE} {colorize(f'{joueur.nom} a un double ! Rejoue immediatement !', Colors.YELLOW)}")
            color = Colors.CYAN if joueur.est_ia else Colors.GREEN
            print(f"\n{colorize('└─ APRES ─────────────────────────────────────────────────────┘', color)}")
            self._afficher_infos_joueur(joueur)
            time.sleep(1.5)
            self.jouer_tour(joueur)
        else:
            color = Colors.CYAN if joueur.est_ia else Colors.GREEN
            print(f"\n{colorize('└─ APRES ─────────────────────────────────────────────────────┘', color)}")
            self._afficher_infos_joueur(joueur)
    
    def partie_terminee(self) -> bool:
        joueurs_actifs = [j for j in self.joueurs if not j.est_en_faillite]
        return len(joueurs_actifs) <= 1
    
    def obtenir_gagnant(self) -> Optional[Joueur]:
        joueurs_actifs = [j for j in self.joueurs if not j.est_en_faillite]
        return joueurs_actifs[0] if len(joueurs_actifs) == 1 else None
    
    def _afficher_resultat_final(self):
        gagnant = self.obtenir_gagnant()
        print(f"\n{colorize('═'*60, Colors.GOLD)}")
        if gagnant:
            print(f"{Icons.TROPHY} {colorize(bold(f'{gagnant.nom} a GAGNE avec {gagnant.argent}€!'), Colors.GOLD)}")
            print(f"{Icons.BUILDING} {colorize(f'Propriétés: {len(gagnant.proprietes)}', Colors.GREEN)}")
            for prop in gagnant.proprietes:
                print(f"  {Icons.CHECK} {prop.nom}")
        else:
            print(f"{Icons.INFO} {colorize(f'Limite de {self.tour_numero} tours atteinte', Colors.YELLOW)}")
            print(f"\n{Icons.TROPHY} {colorize('Classement par argent:', Colors.MAGENTA)}")
            classement = sorted(self.joueurs, key=lambda j: j.argent, reverse=True)
            for i, j in enumerate(classement, 1):
                statut = f"{Icons.CROSS} FAILLITE" if j.est_en_faillite else f"{Icons.CHECK} ACTIF"
                icon = Icons.ROBOT if j.est_ia else Icons.PLAYER
                print(f"  {i}. {icon} {j.nom}: {Icons.MONEY}{j.argent}€ ({Icons.BUILDING}{len(j.proprietes)}) - {statut}")
        print(f"{colorize('═'*60, Colors.GOLD)}")
    
    def jouer_partie(self, max_tours: int = 200, mode_interactif: bool = False):
        print(f"\n{colorize(bold('╔═══════════════════════════════════════════════════════════╗'), Colors.GREEN)}")
        print(f"{colorize(bold(f'║          {Icons.DICE} DEBUT DE LA PARTIE {Icons.DICE}          ║'), Colors.GREEN)}")
        print(f"{colorize(bold('╚═══════════════════════════════════════════════════════════╝'), Colors.GREEN)}\n")
        
        while not self.partie_terminee() and self.tour_numero < max_tours:
            joueur = self.joueurs[self.joueur_actuel_index]
            
            if not joueur.est_en_faillite:
                self.jouer_tour(joueur)
                
                if joueur.est_ia and joueur.strategie:
                    propriete_construction = joueur.strategie.decider_construction(joueur)
                    if propriete_construction and joueur.argent >= propriete_construction._get_prix_maison():
                        if propriete_construction.construire_maison(joueur, self.plateau):
                            print(f"{Icons.BUILDING} {colorize(f'IA {joueur.nom} construit sur {propriete_construction.nom}', Colors.CYAN)}")
                
                time.sleep(1.5)
            
            if mode_interactif:
                input("\n[Appuyez sur Entrée...]")
            
            self.joueur_actuel_index = (self.joueur_actuel_index + 1) % len(self.joueurs)
            
            if self.joueur_actuel_index == 0:
                self.tour_numero += 1
                if self.tour_numero % 10 == 0:
                    actifs = sum(1 for j in self.joueurs if not j.est_en_faillite)
                    faillites = len(self.joueurs) - actifs
                    print(f"\n{colorize(f'─── {Icons.INFO} Tour {self.tour_numero}: {actifs} actifs, {faillites} en faillite ───', Colors.CYAN)}")

        self.stats.nb_tours = self.tour_numero
        self.stats.gagnant = self.obtenir_gagnant()
        
        self._afficher_resultat_final()
        return self.obtenir_gagnant()