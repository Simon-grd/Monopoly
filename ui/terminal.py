from game.monopoly import Monopoly
from models.case import Propriete

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
                pos_case = self.jeu.plateau.get_case(joueur_actuel.position)
                print(f"Argent: {joueur_actuel.argent}€ | Position: {pos_case.nom}")
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