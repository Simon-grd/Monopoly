import mysql.connector
from typing import List, Optional
from models.case import Propriete
from models.gare import Gare
from models.compagnie import Compagnie

class DB:
    @classmethod
    def connexionBase(cls):
        mydb = mysql.connector.connect(
          host="localhost",
          user="mmaldo",
          password="aDHp8P6?2/6]",
          database = "monopoly"
        )
        return mydb
    
        except mysql.connector.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return False
    
    def disconnect(self):
        if MYSQL_AVAILABLE and self.connection and self.connection.is_connected():
            self.connection.close()
    
    def charger_proprietes(self) -> List:
        if not MYSQL_AVAILABLE:
            return []
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return []
        
        proprietes = []
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM v_proprietes ORDER BY position")
            
            for row in cursor.fetchall():
                type_prop = row['type_propriete']
                
                if type_prop == 'gare':
                    prop = Gare(row['nom'], row['position'])
                elif type_prop == 'compagnie':
                    prop = Compagnie(row['nom'], row['position'])
                else:
                    prop = Propriete(
                        row['nom'],
                        row['position'],
                        row['prix'],
                        row['loyer_base'],
                        row['couleur']
                    )
                proprietes.append(prop)
            
            cursor.close()
        except mysql.connector.Error as e:
            print(f"Erreur lors du chargement des propriétés: {e}")
        
        return proprietes