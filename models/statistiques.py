from typing import Dict, List, TYPE_CHECKING
from ui.colors import Colors, Icons, colorize, bold

if TYPE_CHECKING:
    from models.case import Case, Propriete
    from models.joueur import Joueur

class StatistiquesPartie:
    def __init__(self):
        self.passages_par_case: Dict[int, int] = {}
        self.revenus_par_propriete: Dict[str, int] = {}
        self.nb_tours = 0
        self.gagnant = None
        self.historique_argent: Dict[str, List[int]] = {}
        self.depenses_par_joueur: Dict[str, int] = {}
        self.revenus_par_joueur: Dict[str, int] = {}
        self.cartes_tirees: Dict[str, int] = {'chance': 0, 'communaute': 0}
        self.proprietes_achetees: Dict[str, int] = {}
        self.constructions_totales: Dict[str, int] = {}
        self.passages_prison: Dict[str, int] = {}
        self.doubles_obtenus: Dict[str, int] = {}
        self.cases_noms: Dict[int, str] = {}
    
    def enregistrer_passage(self, case: 'Case'):
        if case.position not in self.passages_par_case:
            self.passages_par_case[case.position] = 0
            self.cases_noms[case.position] = case.nom
        self.passages_par_case[case.position] += 1
    
    def enregistrer_loyer(self, propriete: 'Propriete', montant: int):
        if propriete.nom not in self.revenus_par_propriete:
            self.revenus_par_propriete[propriete.nom] = 0
        self.revenus_par_propriete[propriete.nom] += montant
    
    def enregistrer_argent_joueur(self, joueur: 'Joueur'):
        if joueur.nom not in self.historique_argent:
            self.historique_argent[joueur.nom] = []
        self.historique_argent[joueur.nom].append(joueur.argent)
    
    def enregistrer_depense(self, joueur: 'Joueur', montant: int):
        if joueur.nom not in self.depenses_par_joueur:
            self.depenses_par_joueur[joueur.nom] = 0
        self.depenses_par_joueur[joueur.nom] += montant
    
    def enregistrer_revenu(self, joueur: 'Joueur', montant: int):
        if joueur.nom not in self.revenus_par_joueur:
            self.revenus_par_joueur[joueur.nom] = 0
        self.revenus_par_joueur[joueur.nom] += montant
    
    def enregistrer_carte(self, type_carte: str):
        if type_carte in self.cartes_tirees:
            self.cartes_tirees[type_carte] += 1
    
    def enregistrer_achat(self, joueur: 'Joueur'):
        if joueur.nom not in self.proprietes_achetees:
            self.proprietes_achetees[joueur.nom] = 0
        self.proprietes_achetees[joueur.nom] += 1
    
    def enregistrer_construction(self, joueur: 'Joueur'):
        if joueur.nom not in self.constructions_totales:
            self.constructions_totales[joueur.nom] = 0
        self.constructions_totales[joueur.nom] += 1
    
    def enregistrer_prison(self, joueur: 'Joueur'):
        if joueur.nom not in self.passages_prison:
            self.passages_prison[joueur.nom] = 0
        self.passages_prison[joueur.nom] += 1
    
    def enregistrer_double(self, joueur: 'Joueur'):
        if joueur.nom not in self.doubles_obtenus:
            self.doubles_obtenus[joueur.nom] = 0
        self.doubles_obtenus[joueur.nom] += 1
    
    def afficher_statistiques(self):
        print(f"\n{colorize(bold('╔═══════════════════════════════════════════════════════════╗'), Colors.MAGENTA)}")
        print(f"{colorize(bold(f'║          {Icons.TROPHY} STATISTIQUES DE LA PARTIE {Icons.TROPHY}          ║'), Colors.MAGENTA)}")
        print(f"{colorize(bold('╚═══════════════════════════════════════════════════════════╝'), Colors.MAGENTA)}")
        
        print(f"\n{Icons.INFO} {colorize(bold('Informations générales'), Colors.CYAN)}")
        print(f"  {Icons.DICE} Durée: {colorize(str(self.nb_tours), Colors.YELLOW)} tours")
        if self.gagnant:
            icon = Icons.ROBOT if self.gagnant.est_ia else Icons.PLAYER
            print(f"  {Icons.TROPHY} Gagnant: {icon} {colorize(self.gagnant.nom, Colors.GOLD)} ({Icons.MONEY}{colorize(str(self.gagnant.argent) + '€', Colors.GREEN)})")
        
        print(f"\n{Icons.CARD} {colorize(bold('Cartes tirées'), Colors.CYAN)}")
        print(f"  Chance: {colorize(str(self.cartes_tirees['chance']), Colors.YELLOW)}")
        print(f"  Communauté: {colorize(str(self.cartes_tirees['communaute']), Colors.YELLOW)}")
        
        print(f"\n{Icons.ARROW} {colorize(bold('Top 5 cases les plus visitées'), Colors.CYAN)}")
        top_cases = sorted(self.passages_par_case.items(), key=lambda x: x[1], reverse=True)[:5]
        for position, nb in top_cases:
            nom = self.cases_noms.get(position, f"Position {position}")
            print(f"  {colorize(f'{nom:30}', Colors.WHITE)} {colorize(str(nb), Colors.YELLOW)} passages")
        
        if self.revenus_par_propriete:
            print(f"\n{Icons.MONEY} {colorize(bold('Top 5 propriétés les plus rentables'), Colors.CYAN)}")
            top_props = sorted(self.revenus_par_propriete.items(), key=lambda x: x[1], reverse=True)[:5]
            for nom, revenus in top_props:
                print(f"  {colorize(f'{nom:30}', Colors.WHITE)} {colorize(str(revenus) + '€', Colors.GREEN)}")
        
        if self.proprietes_achetees:
            print(f"\n{Icons.BUILDING} {colorize(bold('Propriétés achetées par joueur'), Colors.CYAN)}")
            for joueur, nb in sorted(self.proprietes_achetees.items(), key=lambda x: x[1], reverse=True):
                print(f"  {colorize(f'{joueur:20}', Colors.WHITE)} {colorize(str(nb), Colors.YELLOW)} propriétés")
        
        if self.constructions_totales:
            print(f"\n{Icons.HOUSE} {colorize(bold('Constructions par joueur'), Colors.CYAN)}")
            for joueur, nb in sorted(self.constructions_totales.items(), key=lambda x: x[1], reverse=True):
                print(f"  {colorize(f'{joueur:20}', Colors.WHITE)} {colorize(str(nb), Colors.YELLOW)} constructions")
        
        if self.depenses_par_joueur:
            print(f"\n{Icons.BANK} {colorize(bold('Dépenses totales par joueur'), Colors.CYAN)}")
            for joueur, montant in sorted(self.depenses_par_joueur.items(), key=lambda x: x[1], reverse=True):
                print(f"  {colorize(f'{joueur:20}', Colors.WHITE)} {colorize(str(montant) + '€', Colors.RED)}")
        
        if self.revenus_par_joueur:
            print(f"\n{Icons.MONEY} {colorize(bold('Revenus totaux par joueur'), Colors.CYAN)}")
            for joueur, montant in sorted(self.revenus_par_joueur.items(), key=lambda x: x[1], reverse=True):
                print(f"  {colorize(f'{joueur:20}', Colors.WHITE)} {colorize(str(montant) + '€', Colors.GREEN)}")
        
        if self.passages_prison:
            print(f"\n{Icons.PRISON} {colorize(bold('Passages en prison'), Colors.CYAN)}")
            for joueur, nb in sorted(self.passages_prison.items(), key=lambda x: x[1], reverse=True):
                print(f"  {colorize(f'{joueur:20}', Colors.WHITE)} {colorize(str(nb), Colors.YELLOW)} fois")
        
        if self.doubles_obtenus:
            print(f"\n{Icons.DICE} {colorize(bold('Doubles obtenus'), Colors.CYAN)}")
            for joueur, nb in sorted(self.doubles_obtenus.items(), key=lambda x: x[1], reverse=True):
                print(f"  {colorize(f'{joueur:20}', Colors.WHITE)} {colorize(str(nb), Colors.YELLOW)} doubles")
        
        if self.historique_argent:
            print(f"\n{Icons.MONEY} {colorize(bold('Évolution de l\'argent'), Colors.CYAN)}")
            for joueur, historique in self.historique_argent.items():
                if historique:
                    debut = historique[0]
                    fin = historique[-1]
                    evolution = fin - debut
                    couleur = Colors.GREEN if evolution >= 0 else Colors.RED
                    signe = '+' if evolution >= 0 else ''
                    print(f"  {colorize(f'{joueur:20}', Colors.WHITE)} {debut}€ → {fin}€ ({colorize(f'{signe}{evolution}€', couleur)})")
        
        print(f"\n{colorize('═'*60, Colors.MAGENTA)}\n")