from models.ia import IAAgressive, IAConservative, IAStrategique
from ui.colors import Colors, Icons, colorize, bold
import os

class Interface:
    
    @staticmethod
    def configurer_joueurs():
        os.system('cls')
        print(f"\n{colorize(bold('╔═══════════════════════════════════════════════════════════╗'), Colors.CYAN)}")
        print(f"{colorize(bold(f'║          {Icons.BANK} MONOPOLY - Configuration {Icons.BANK}          ║'), Colors.CYAN)}")
        print(f"{colorize(bold('╚═══════════════════════════════════════════════════════════╝'), Colors.CYAN)}\n")
        
        joueurs_config = []

        print(f"{colorize(f'┌─ {Icons.PLAYER} Joueur 1 (Humain) ──────────────────────────────────┐', Colors.GREEN)}")
        while True:
            nom = input(f"{colorize('Nom', Colors.WHITE)}: ").strip()
            if nom:
                break
            print(f"{colorize(f'{Icons.WARNING} Le nom est obligatoire!', Colors.RED)}")
        joueurs_config.append((nom, None))

        nb_supp = Interface._demander_nombre_joueurs()
        
        for i in range(nb_supp):
            print(f"\n{colorize(f'┌─ {Icons.PLAYER} Joueur {i+2} ──────────────────────────────────────────┐', Colors.YELLOW)}")
            print(f"  {colorize('1.', Colors.WHITE)} {Icons.PLAYER} Humain")
            print(f"  {colorize('2.', Colors.WHITE)} {Icons.ROBOT} IA Agressive")
            print(f"  {colorize('3.', Colors.WHITE)} {Icons.ROBOT} IA Conservative")
            print(f"  {colorize('4.', Colors.WHITE)} {Icons.ROBOT} IA Strategique")
            
            while True:
                choix = input(f"{colorize('Type (1-4)', Colors.WHITE)}: ").strip()
                if choix in ["1", "2", "3", "4"]:
                    break
                print(f"{colorize(f'{Icons.WARNING} Choix invalide, veuillez entrer 1, 2, 3 ou 4', Colors.RED)}")
            
            while True:
                nom = input(f"{colorize('Nom', Colors.WHITE)}: ").strip()
                if nom:
                    break
                print(f"{colorize(f'{Icons.WARNING} Le nom est obligatoire!', Colors.RED)}")
            
            if choix == "1":
                joueurs_config.append((nom, None))
            elif choix == "2":
                joueurs_config.append((nom, IAAgressive()))
            elif choix == "3":
                joueurs_config.append((nom, IAConservative()))
            else:
                joueurs_config.append((nom, IAStrategique()))
        
        Interface._afficher_configuration(joueurs_config)
        input(f"\n{colorize(f'{Icons.ARROW} Appuyez sur Entrée pour commencer...', Colors.GREEN)}")
        os.system('cls')
        return joueurs_config
    
    @staticmethod
    def _demander_nombre_joueurs():
        print(f"\n{colorize(f'{Icons.INFO} Combien de joueurs supplementaires (1-3)?', Colors.CYAN)}")
        while True:
            try:
                nb = int(input(f"{colorize('Nombre', Colors.WHITE)}: "))
                if 1 <= nb <= 3:
                    return nb
                print(f"{colorize(f'{Icons.WARNING} Veuillez entrer un nombre entre 1 et 3', Colors.RED)}")
            except ValueError:
                print(f"{colorize(f'{Icons.WARNING} Veuillez entrer un nombre valide', Colors.RED)}")
    
    @staticmethod
    def _afficher_configuration(joueurs_config):
        print(f"\n{colorize('╔═══════════════════════════════════════════════════════════╗', Colors.MAGENTA)}")
        print(f"{colorize(f'║          {Icons.TROPHY} JOUEURS CONFIGURES {Icons.TROPHY}          ║', Colors.MAGENTA)}")
        print(f"{colorize('╠═══════════════════════════════════════════════════════════╣', Colors.MAGENTA)}")
        for i, (nom, strat) in enumerate(joueurs_config, 1):
            icon = Icons.ROBOT if strat else Icons.PLAYER
            type_j = f"IA {strat.nom}" if strat else "Humain"
            color = Colors.CYAN if strat else Colors.GREEN
            print(f"{colorize('║', Colors.MAGENTA)} {icon} {colorize(f'{nom:18}', color)} {colorize(f'({type_j})', Colors.WHITE):30} {colorize('║', Colors.MAGENTA)}")
        print(f"{colorize('╚═══════════════════════════════════════════════════════════╝', Colors.MAGENTA)}\n")
